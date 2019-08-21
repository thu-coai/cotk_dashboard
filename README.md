# Conversational Toolkits Dashboard

## Environment

* Docker

## Installation

* Install Docker
* Run
```
docker-compose up
```

* If at the first time, run
```
docker exec -it cotk_dashboard_django_1 bash
```

then run
```
./manage.py migrate &&
./manage.py collectstatic
```

* You can access the web by http://127.0.0.1/

## Configuration

For production use, you should edit the `.env` file under the root directory.

Other configuration files are under the `config` directory.

### ENV

When in production mode,

* change the password for database and the secret key (to some random generated string)
* set your domain to DASHBOARD_HOST
* delete `DEBUG=TRUE` and `PYTHONBUFFERED=TRUE`

### Nginx

* edit `nginx/cotk_dashboard.conf`, set the `server_name` to your domain

### Columns for dataloaders

* edit `columns.json`

## Administrator

* The user who registered first will automatically become a superuser.
* Others can be set by the admin panel at `/admin`

## Others

Main repo is at https://github.com/thu-coai/cotk

## License

Apache License 2.0
