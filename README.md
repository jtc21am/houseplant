# houseplant

A plant watering schedule web application built using Django, hosted on Render.

## About this application
I took the opportunity to my hands dirty (all puns intended) in the world of physical electronics and micro-controllers as well as take plant nurturing to the next level. This is a topic that is entirely new to me.

It is my goal to utilize the data to build an automatic watering system as well as implement ML so the plant health is optimized.  For light, the abstract metric of “sun exposure” that every package of seeds and every plant purchased is readily availavble to the consumer.

The thing about this metric is that it is surprisingly subjective and unscientific, at least for consumer-facing products. Generally speaking, we’d want to look at W/sqm of solar irradiance, but we’ll get to why that is not straightforward in a second.

Architecture

I am seeking data - data on sun exposure, soil moisture, and eventually temperature although these metrics are hyper-localized and can be entirely different only a foot away.

So we’ll be collecting metrics like soil moisture, sun exposure UV, plus metadata like device ID and timestamp, send it to a server on the network using a REST API, store it in a database, and analyze it using Grafana.


I love plants and gardening. 

The app is a reminder of when to water my plants, as well as keep a log on each plant to record things like fertilization, repotting, pest control, etc. 



Set up my Django project with Postgres, Nginx and Gunicorn:  I utilized Class based views, signaling, caching and built unit tests.

# Usage

To use **HousePlant** 

## _Clone the repository from Github_

Clone the repository from Github into a directory.

```bash
  git clone <repository> <path>
```

---

### _Setting up the Virtual Environment_

Now create a new virtual environment.

Run the following command:

```bash
  python -m venv venv  # you may have to use python3 instead of python
```

Activate the virtual environment.

Run one of the following commands depending on the type of operating system you are using:

> MacOS, Linux, ChromeOS:  
> `source venv/bin/activate`  
> Windows:  
> `venv\Scripts\activate.bat`

---

### _Install Project Dependencies_

Install the project dependencies.

Navigate to the project root directory.

Run the following commands:

```bash
  pip install django
```

```bash
  pip freeze install
```

```bash
  pip freeze > requirements.txt
```

---

### _Running the Application_

Navigate to the `mirror-mirror` directory.

Run the following command:

```bash
  python manage.py runserver
  # you may have to replace python with python3
```

Point your browser to use the app:
[http://localhost:8000](http://localhost:8000)

---

### _Stopping the Application_

Shut down the server.

Run the following command in the terminal:

```bash
  Ctrl+C
```

---

### _Exiting the Virtual Environment_

Run the following command:

```bash
  deactivate
```

## Technology used

- Bootstrap5
- Javascript
- HTML
- CSS
- Visual Studio Code
- GitHub for version control, Issues and Projects
- Miro for Wireframe
- Figma for Er Diagram
- Raspberry Pi, Soil Moisture Sensor, Light Sensor
- Grafana
- Adafruit library


**Additionally:**

- [Python](https://docs.python.org/3/tutorial/datastructures.html) data structures such as Lists, Dictionaries and their associated methods
- [Python Classes and Inheritance](https://docs.python.org/3/tutorial/classes.html)
- [Django URLs](https://docs.djangoproject.com/en/3.2/topics/http/urls/) to understand how to capture parameters in views
- [Django Templates](https://docs.djangoproject.com/en/3.2/ref/templates/language/)
- [Django Migrations](https://docs.djangoproject.com/en/4.0/topics/migrations/)
- [Django Models](https://docs.djangoproject.com/en/4.0/topics/db/models/)
- [Django Shell](https://docs.djangoproject.com/en/4.0/ref/django-admin/)
- [Django Post Create Content](https://docs.djangoproject.com/en/4.0/ref/request-response/)
- [Django Static CSS](https://learndjango.com/tutorials/django-static-files)
- [Django HTML](https://docs.djangoproject.com/en/4.0/topics/templates/)
- [Python Signal](https://docs.python.org/3/library/signal.html)

