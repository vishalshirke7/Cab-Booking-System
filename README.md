# Cab-Booking-System

### _Tech stack used_
```
- python/django/django-restframework
- SQlite 3
```

#### Installation

##### clone or download and extract the project directory 
1. Create a virtualenv (better to work in virtualenv)  
```
a. virtualenv env
b. cd env
```
2. Place the downloaded project inside env
```
a. cd Cab-Booking-System
b. pip install requirements.txt
```

### Running the APIs. There are two apps in this project (Driver, Passenger)

Base URL :  http:127.0.0.1:8000/api/v1/
 
##### Driver Endpoints  (http:127.0.0.1:8000/api/v1/driver/)
```
1. Register a new driver with information -  http:127.0.0.1:8000/api/v1/driver/register/
2. Login using credentials entered during registration -  http:127.0.0.1:8000/api/v1/driver/login/
3. Sending Location of driver -  http:127.0.0.1:8000/api/v1/driver/send_location/
4. Get Travel history - http:127.0.0.1:8000/api/v1/driver/travelhistory/
5. Logout -  http:127.0.0.1:8000/api/v1/driver/logout/
```
#### NOTE : while signing up with new driver, logout if you are already logged in, same for passenger

##### Passenger Endpoints  (http:127.0.0.1:8000/api/v1/passenger/)
```
1. Register a new passenger with information -  http:127.0.0.1:8000/api/v1/passenger/register/
2. Login using credentials entered during registration -  http:127.0.0.1:8000/api/v1/passenger/login/
3. See all available cabs by entering source and destination address - http:127.0.0.1:8000/api/v1/passenger/available_cabs/
4. Requesting a cab from list of available cabs by entering the car no - http:127.0.0.1:8000/api/v1/passenger/bookcab/
5. Get Travel history - http:127.0.0.1:8000/api/v1/passenger/travelhistory/
6. Logout -  http:127.0.0.1:8000/api/v1/passenger/logout/
```

