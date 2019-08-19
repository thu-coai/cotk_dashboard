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

All configuration files are under the `config` folder.

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
