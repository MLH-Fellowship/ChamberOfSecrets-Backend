# DigiCrux-Backend
---

## Getting Started with Development
---
To develop or run the server locally, run the following commands after cloning the repo:

1. Activate the virtual environment and cd into the project:
```shell
$ pipenv shell && cd backend
```

2. Run the model migrations:
```shell
$ python manage.py migrate
```

3. Create the superuser:
```shell
$ python manage.py createsuperuser
```
Fill in the desired info to the promts for creating the superuser, that will be required for accessing the Django Admin interface.

4. Run the server locally:
```shell
$ python manage.py runserver
```
