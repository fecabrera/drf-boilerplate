# DRF Boilerplate

## Introduction

Includes:

* [Pipfile](Pipfile) for dependencies
* [Dockerfile](Dockerfile) for deployment
* [docker-compose.yml](docker-compose.yml) for development database
* Support for CORS and CSRF
* Support for S3/DigitalOcean storage
* Popular libraries (complete list in [Pipfile](Pipfile), you can always comment the ones you don't need 🙃)
* Coverage reports

## Quickstart

### Set up
```bash
git clone https://github.com/fecabrera/drf-boilerplate.git
cd drf-boilerplate
pipenv install --dev
pipenv shell
```

### Preparing the environment
```bash
cp .env.example .env  # uses an example local environment file
docker-compose up -d  # starts the development database
```

### Running the server
```bash
python manage.py runserver
``` 

## Testing

### Unit tests

```bash
python manage.py test
```
### Coverage report

See [.coveragerc](.coveragerc) for the configuration.

```bash
coverage run manage.py test
coverage report  # will fail if coverage < 90%, can be changed in .coveragerc
```

## Environment variables

There's two ways to set environment variables:

* Using a `.env` file (see [.env.example](.env.example))
* Adding them to the shell environment

### List of variables

| Variable                | Description                                 | Values                                               | Default    |
|-------------------------|---------------------------------------------|------------------------------------------------------|------------|
| DEBUG                   | Whether Django should show debug messages   | `True` or `False`                                    | `True`     |
| ENVIRONMENT             | The environment to work on                  | `unittest`, `development`, `staging` or `production` | `unittest` |
| AWS_ACCESS_KEY_ID       |                                             | String                                               | `None`     |
| AWS_SECRET_ACCESS_KEY   |                                             | String                                               | `None`     |
| AWS_STORAGE_BUCKET_NAME |                                             | String                                               | `None`     |
| AWS_S3_REGION_NAME      |                                             | String                                               | `None`     |
| DATABASE_URL            | The URL to the database                     | URL                                                  |            |
| POSTGRES_DB             | The name of the database                    | String                                               |            |
| POSTGRES_USER           | The name of the database user               | String                                               |            |
| POSTGRES_PASSWORD       | The password of the database user           | String                                               |            |
| POSTGRES_HOST           | The host of the database                    | String                                               |            |
| POSTGRES_PORT           | The port of the database                    | String                                               |            |
| POSTGRES_TEST_DB        | The name of the test database               | String                                               | `test`     |
| DISABLE_S3_DO_STORAGE   | Explicitly disables S3/DigitalOcean storage | `True` or `False`                                    |            |
| DISABLE_CORS            | Explicitly disables CORS                    | `True` or `False`                                    |            |
| DISABLE_CSRF            | Explicitly disables CSRF                    | `True` or `False`                                    |            |
| ALLOWED_HOSTS           | A list of allowed domains                   | Comma separated hosts                                |            |
| CORS_ALLOWED_ORIGINS    | A list of trusted origins for CORS requests | Comma separated URLs                                 |            |
| CSRF_TRUSTED_ORIGINS    | A list of trusted origins for CSRF requests | Comma separated URLs                                 |            |
| SESSION_COOKIE_DOMAIN   | The domain for the session cookie           | String                                               | `None`     |
| CSRF_COOKIE_DOMAIN      | The domain for the CSRF cookie              | String                                               | `None`     |

### Examples

#### Local development environment

Suitable for unit testing. Disables S3/DO storage, CSRF and CORS.

```bash
# .env
DEBUG=True
ENVIRONMENT=unittest

# You must use these variables when using the development database in docker-compose.yml.
POSTGRES_USER=admin
POSTGRES_PASSWORD=1234
POSTGRES_DB=data
POSTGRES_HOST=0.0.0.0
POSTGRES_PORT=5432
```

#### Local environment

Suitable for local development/testing. Disables CSRF and CORS.

```bash
# .env
DEBUG=True
ENVIRONMENT=development

AWS_ACCESS_KEY_ID=<aws_access_key>
AWS_SECRET_ACCESS_KEY=<aws_secret_access_key>
AWS_STORAGE_BUCKET_NAME=<aws_bucket_name>
AWS_S3_REGION_NAME=<aws_region_name>

# You can use this instead of the POSTGRES_* variables when using an external DB.
DATABASE_URL=<postgres://user:password@host:port/dbname>
```

#### Staging environment

Suitable for staging and product testing.

```bash
# .env
DEBUG=True
ENVIRONMENT=staging

AWS_ACCESS_KEY_ID=<aws_access_key>
AWS_SECRET_ACCESS_KEY=<aws_secret_access_key>
AWS_STORAGE_BUCKET_NAME=<aws_bucket_name>
AWS_S3_REGION_NAME=<aws_region_name>

DATABASE_URL=<postgres://user:password@host:port/dbname>

ALLOWED_HOSTS=.example.com

CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com

SESSION_COOKIE_DOMAIN=.example.com
CSRF_COOKIE_DOMAIN=.example.com
```

#### Production environment

Suitable for production.

```bash
# .env
DEBUG=False
ENVIRONMENT=production

AWS_ACCESS_KEY_ID=<aws_access_key>
AWS_SECRET_ACCESS_KEY=<aws_secret_access_key>
AWS_STORAGE_BUCKET_NAME=<aws_bucket_name>
AWS_S3_REGION_NAME=<aws_region_name>

DATABASE_URL=<postgres://user:password@host:port/dbname>

ALLOWED_HOSTS=.example.com

CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com

SESSION_COOKIE_DOMAIN=.example.com
CSRF_COOKIE_DOMAIN=.example.com
```

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.
