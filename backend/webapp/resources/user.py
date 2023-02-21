from http import HTTPStatus

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models.user import UserModel
from schemas.user import UserSchema, LoginResponseSchema, RefreshResponseSchema


blp = Blueprint("Users", __name__,  url_prefix='/api',
                description="User related operations")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(HTTPStatus.CREATED.value, UserSchema)
    def post(self, user_data):
        user = UserModel(
            email=user_data["email"], pass_hash=pbkdf2_sha256.hash(user_data["password"]))
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(HTTPStatus.CONFLICT.value,
                  message="A user with that email already exists.")
        except SQLAlchemyError:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                  message="An error occurred while adding the user.")

        return user


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(HTTPStatus.OK.value, LoginResponseSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.pass_hash):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(HTTPStatus.UNAUTHORIZED.value, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRfresh(MethodView):
    @jwt_required(refresh=True)
    @blp.response(HTTPStatus.OK.value, RefreshResponseSchema)
    def post(self):
        new_token = create_access_token(
            identity=get_jwt_identity(), fresh=False)
        # todo: add a limit to using refresh tokens
        return {"access_token": new_token}


# todo: implement logout

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(HTTPStatus.OK.value, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required(fresh=True)
    @blp.response(HTTPStatus.OK.value)
    def delete(self, user_id):
        user = UserModel.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
