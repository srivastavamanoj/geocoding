# Geocoding Service
A geocoding service which takes an adress of a location and provides lattitude and longitude of that place. Our service uses third party libraries - Google and Here - with Google being primary and Here as the backup service for our API. Service accepts RESTful HTTP protocol and produces output in JSON format.

# Prerequisites
1. Django(v2.1.7), a python web framework, for running the webserver.
2. Python(v2.7.14)

# Starting the Server
Please go to the base of geocoding directory where you will find "manage.py" file, then launch the following command- 

```python3 manage.py runserver```

This will present to you the following output on the command window

```
Performing system checks...

System check identified no issues (0 silenced).

You have 15 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

March 04, 2019 - 06:47:37
Django version 2.1.7, using settings 'geoCodingService.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
This means your server has started at http://127.0.0.1:8000/. You can go to a web-browser and you should see the following confirmation message

```Welcome to the GeoCoding Service!```

Please ignore the warning message " You have 15 unapplied migration(s)..." It's not relevant to our current task.

# API Calls
To add an address, add ```?q=<address>``` to ```http://127.0.0.1:8000/```. For example, to get lattitude/longitude of "1721 Marco Polo Way, Burlingame, CA, 94010", launch the following command from your browser - 

```http://127.0.0.1:8000/?q=1721+marco+polo_way+burlingame+ca```

Output will be produced in the browser as

```{'lat': 37.5895752}{'lng': -122.3844471}```


## Limitation
As of now the service only accepts free-form addresses. Advanced features such as specific viewport, intersection address, etc are not implemented.
