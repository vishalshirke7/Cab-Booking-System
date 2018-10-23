# Cab-Booking-System

### _Tech stack used_
```
- python/django/django-restframework
- SQlite 3
```

#### Installation

##### clone or download and extract the project directory 
1. Create a virtualenv (better to work in virtualenv)  
`virtualenv env`
`cd env`
2. Place the downloaded project inside env
2. cd into Cab-Booking-System
3. pip install requirements.txt

### Running the APIs. There are two apps in this project (Driver, Passenger)

Base URL :  http:127.0.0.1:8000/api/v1/
 
##### Driver Endpoints  (http:127.0.0.1:8000/api/v1/driver)
```
1. Register a new driver with information -  http:127.0.0.1:8000/api/v1/driver/register/
2. Login using credentials entered during registration -  http:127.0.0.1:8000/api/v1/driver/login/
```
