# DRF Boilerplate

## Introduction

Includes:

* [Pipfile](Pipfile) for dependencies
* [Dockerfile](Dockerfile) for deployment
* [docker-compose.yml](docker-compose.yml) for development database
* Support for CORS and CSRF
* Support for S3/DigitalOcean storage
* Popular libraries (complete list in [Pipfile](Pipfile), you can always comment the ones you don't need 🙃)

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

## Documentation

### Environment variables
| Variable                | Description                                 | Values                             | Default |
|-------------------------|---------------------------------------------|------------------------------------|---------|
| DEBUG                   | Whether Django should show debug messages   | `True` or `False`                  | `True`  |
| ENVIRONMENT             | The environment to work on                  | `test`, `dev`, `staging` or `prod` | `test`  |
| AWS_ACCESS_KEY_ID       |                                             | String                             | `None`  |
| AWS_SECRET_ACCESS_KEY   |                                             | String                             | `None`  |
| AWS_STORAGE_BUCKET_NAME |                                             | String                             | `None`  |
| AWS_S3_REGION_NAME      |                                             | String                             | `None`  |
| DATABASE_URL            | The URL to the database                     | URL                                |         |
| ALLOWED_HOSTS           | A list of allowed domains                   | Comma separated hosts              |         |
| CORS_ALLOWED_ORIGINS    | A list of trusted origins for CORS requests | Comma separated URLs               |         |
| CSRF_TRUSTED_ORIGINS    | A list of trusted origins for CSRF requests | Comma separated URLs               |         |
| SESSION_COOKIE_DOMAIN   | The domain for the session cookie           | String                             | `None`  |
| CSRF_COOKIE_DOMAIN      | The domain for the CSRF cookie              | String                             | `None`  |

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.
