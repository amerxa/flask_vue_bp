from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class LoginResponseSchema(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


class RefreshResponseSchema(Schema):
    access_token = fields.Str(required=True)
