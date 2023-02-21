# Flask Vue Boilerplate
This repo is under development. It's meant to serve as a boilerplate for Flask+Vue webapps providing the following:

- build with Docker Compose
- REST structure using flask_smorest
- DB management using flask_sqlalchemy and flask_migrate with Postgres
- Authentication using flask_jwt_extended
- Caching with Redis
- NGINX and GUNICORN for Production
- API testing


## For Development
1. clone the repo.
2. add `.env.dev.db` file to the root of the repo and define the environment variables found in `.env.sample.db`.
3. add `.env.dev` file to the root of the repo and define the environment variables found in `.env.sample`.
4. at the root of the repo, execute following docker compose command:
  ```
  docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
  ```
5. browse to `http://localhost:5000/api/swagger-ui` to view the swagger documentation of the API.
6. on the created 'web' container, execute the DB migration commands (won't be required for prod):
  ```
  flask db init  # executed only once to initialize the migrations folder
  flask db migrate # executed on db changes
  flask db upgrade # executed after vetting the migration script
  ```


## For Production
to be added

## Next Steps
1. expand and vet swagger documentation.
2. add authentication tests.
3. add caching.
4. add Vue frontend client.
5. prepare for production.