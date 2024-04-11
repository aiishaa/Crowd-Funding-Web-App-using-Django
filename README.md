# Crowd-Funding

CrowdFunding Web App using Python "Django Framework"
## About the web-App:

CrowdFunding Web App that allow user to:

- Signup and login
- Create and modify his profile data or delete his account
- Create or Delete funding projects
- show all projects details
- Donate, Rate, Report, and Comment other projects


## Built With:

- [Django Framwork](https://docs.djangoproject.com/en/)
- [MySql Database](https://pypi.org/project/mysql-connector-python/)
- [HTML, CSS, JS, Bootstrap....](https://getbootstrap.com/)

## Installation and Run project:

1- Download or Clone the project

2- Install python on your machine

- [Download from here](https://www.python.org/downloads/windows/)
- [check your version]

  ```bash
  python --version
  ```

  \*\* must be v.3 or up

- [install and upgrade pip]

  ````bash
  python3 -m pip install --upgrade pip

3- run your mysql server and create new Schema in your DBMS with name "crowdfunding" or change the name at (setting.py) and set your DB Server information [ host name and password ]

4- Open the project in vs Code

5- In a Terminal window run the following >>

- [install VirtualEnvironment]
  ```bash
  pip3 install virtualenv
  ```
- [Create and Activate VirtualEnvironment]

  ```bash
  virtualenv .venv
  ```

  for win

  ```bash
  .venv\Scripts\activate
  ```

  for linux

  ```bash 
  source .venv/bin/activate
  ```

- [Install requirments]
  ```bash
  pip3 install -r requirements.txt
  ```

6- Set The Values in ".env" file to test Verification using email

DB_USER="your db user"<br>
DB_PASSWORD="your db user password"<br>
DB_HOST="127.0.0.1 or localhost"<br>
EMAIL_HOST = 'smtp.gmail.com'<br>
EMAIL_HOST_USER = 'your email address'<br> 
EMAIL_HOST_PASSWORD = 'your app password you created in your google account'<br>

\*\* Add your [gmail] but make sure that the two factor authentication is activated in the account and that you created an app password to use it as a value for the env variable 'EMAIL_HOST_PASSWORD' :D


7- Run the following to load Data base

```bash
python3 manage.py makemigrations
```

```bash
python3 manage.py migrate
```

8- create your superuser [admin] to access [Admin Dashboard]

```bash
python3 manage.py createsuperuser
    > enter user name
    > enter user email
    > enter password
```

9- After All is Finished run server

```bash
	python3 manage.py runserver
```

\*\* take the link (http://127.0.0.1:8000/) and put it on your browser

## Notes

1- you can access the [Admin Dashboard] by :

- in your broswer use (http://127.0.0.1:8000/admin)
- enter admin email and password created
- add some categories
- you can featured projects from here

2- if you create any account in site you need to activate it from the activation link sent to the email you signed up with

## Authors

- Aisha Fathy
- Mohamed Tharwat
- Sara Eldwiny
- Jasmine walid
- Nadine Abdelazeem
