# houseplant

A plant watering schedule web application built using Django, hosted on Render.

I love plants and gardening. 

The app is a reminder of when to water my plants, as well as keep a log on each plant to record things like fertilization, repotting, pest control, etc. 


## About this application
To explore the world of physical electronics and microcontrollers while enhancing plant nurturing, I embarked on a new and exciting journey. My objective is to create an automatic watering system using collected data and implement machine learning for optimized plant health. When it comes to light, the widely available metric of "sun exposure" found on seed packages and plant purchases is subjective and unscientific for consumer products. I am interested in obtaining data on sun exposure, soil moisture, and temperature, acknowledging their hyper-localized nature. By collecting metrics like soil moisture and sun exposure UV, along with device ID and timestamp, I will send the data to a server using a REST API, store it in a database, and analyze it. To accomplish this, I set up my Django project with Postgres, Nginx, and Gunicorn, utilizing class-based views, signaling, caching, and building unit tests.

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

Navigate to the `myhouseplant` directory.

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
- Figma for ER Diagram
- Raspberry Pi Pico W 
- SparkFun Qwiic Soil Moisture Sensor
- Light Sensor using an LDR (Photoresistors)
- Sanity Content Cloud


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
- [Gunicorn](https://www.google.com/search?client=safari&rls=en&q=gunicorn&ie=UTF-8&oe=UTF-8)
- [NGINX](https://www.nginx.com)
- [PyCharm with MicroPython](https://www.jetbrains.com/pycharm/)
