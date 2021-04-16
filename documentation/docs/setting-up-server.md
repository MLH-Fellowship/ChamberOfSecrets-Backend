---
title: Contribution Guide- Server 
---
---

Chamber of Secrets is an open-source project (licensed under MIT Open Source Licensing agreement), aimed at Data Security and Ethical Data. In order to make the system more robust and secure, we feel that the support and contributions from the community is very important.

This is guide that will help you get started with contributions to the Chamber of Secrets server, written in Python using the **Django RESTful Framework**. The place where all the magic happens!

## Setting Up Local Environment
---

### Instructions for CoS Server:

Assuming that you already have Python already installed and the project cloned from GitHub, run the following set of commands to set up the development environment locally.

1. Install pipenv:

```bash
pip install pipenv 
```

2. Installing dependencies:
```bash
pipenv install && pipenv shell
```

3. Set up your environment variables:
- Go to backend/settings.py and replace the default value of `APP_SECRET_KEY` to your app secret key. This will be used to hash the passwords at the time of authentication.

- Create a new app on [Dropbox Developers App Console](https://www.dropbox.com/lp/developers). Next, go to authenticate/dropbox_auth.py and replace `DROPBOX_APP_KEY` and `DROPBOX_APP_SECRET` with your app key and app secret respectively.

- Create a new project on [Google Cloud Console](https://console.cloud.google.com). Go to APIs and Services and enable the Google Drive API for your project. Next, in the code go to authenticate/google_auth.py and replace `GOOGLE_CLIENT_CONFIG` with the google client configurations of your Google Cloud Project. Make sure at the time of oauth config generation, select application type as desktop.


4. Running the database migrations:
```bash
python manage.py migrate
```

5. Creating superuser for Django Admin:
```bash
python manage.py runserver
```

6. Running the server locally. 
```bash
python manage.py runserver
```

This will get all the necessary dependencies installed in your Python virtual environment and get things up and running. 

### Instructions for Documentation Website

The documentation website (yes, this exact same one you are on right now) was built using Docusaurus.

Click [here](https://docusaurus.io/docs/installation) for a detailed official documentation on setting the local development environment for the documentation website.

## Contributing to Chamber of Secrets:
---

In order to contribute to the project, make sure you follow the below mentioned guidelines:

1. To suggest a bug fix/improvement/feature etc., first create an issue. Discuss the issue with the CoS project managers and get the issue assigned to yourself.

2. Once assigned, you can start working on the project. Fork and clone the repository and follow the local development guide to set up your local development environment. 

3. Once the issue is fixed, create a PR to the upstream repository's staging branch. Wait and hear back from the project managers on their response. Once your build is tested and approved, the PR will get merged. If any changes are required, you can continue coordinating with the project managers and work on the requirements.

## Resources:
---

1. Django REST Framework Documentation: [Click here!](https://www.django-rest-framework.org/)

2. Cryptography Python Module: [Click here!](https://pypi.org/project/cryptography/)

3. Docusaurus Documentation: [Click here!](https://docusaurus.io/)