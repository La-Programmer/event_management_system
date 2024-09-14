# EVENT MANAGEMENT SYSTEM

## AUTHORS

Justin Ebedi - [Github](https://github.com/La-Programmer)  
Ahmed Issa - [Github](https://github.com/Ahmed-Is3a)

## DESCRIPTION

An event management system that allows users to create events and send out invitation links to invitees. Invitees will have the capability to generate an invitation card which contains a unique QR code which will be used to verify the user when he/she goes for the event.

## SETUP

1. Clone the github repository using the following command

For HTTP: 
```
git clone https://github.com/La-Programmer/event_management_system.git
```    
For SSH: 
```
git clone git@github.com:La-Programmer/event_management_system.git
```

After cloning the repository, continue with the following steps.

### Environment Setup

1. Start a virtual environment using python in the src directory `venv`;  
   ```
   python -m venv my_env
   ```

2. Install the project requirments using the following command;  
   ```
   pip install -r requirements.txt
   ```

### DB Setup

In this project, there is a test database and a development database

The following steps assume that you have mysql installed on your local system. If you do not find the installation steps here, https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

Once you have installed and setup of mysql database, follow the steps below

1. Using mysql bench or mysql shell create a database called "event_planner" (you can use any database name you want but you will have to put that database name in your environment variable as DB)  
   ```
   create database if not exists event_planner
   ```   

2. Using mysql bench or mysql shell create a database called "event_planner_test" (you can use any database name you want but you will have to put that database name in your environment variable as TEST_DB)  
   ```
   create database if not exists <event_planner_test>
   ```

3. Setup your environment credentials using the .env.example file

## Start the project using the following steps

1. Start redis in a different shell using the command below  
   ```
   redis-server
   ```

2. Start celery in a different shell using the command below  
   ```
   celery -A v1.api.celery_app worker --loglevel INFO
   ```

3. Start the application by running the bash script 'run_flask_app' using the following command  
   ```
   ./run_flask_app
   ```

## Run unit tests using the following steps

The project contains using unit tests, and they can be ran using the following steps

1. Start redis and celery using the commands in the previous steps above

2. Run tests using the bash script 'run_test' using the following command  
   ```
   ./run_test
   ```

There are 53 test and all tests should pass.
