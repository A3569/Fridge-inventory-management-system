# Fridge Inventory Management System
The **Fridge Inventory Management System** is a Python-based application designed to help users efficiently manage their fridge inventory. This system tracks items in the fridge, monitors their quantities, and notifies users about upcoming expirations. It is ideal for personal use, meal planning, or reducing food waste.

# File structures
~~~
Fridge inventory management system/
├── fridge/
│   ├── api/
│       ├── urls.py
│       ├── views.py
│   ├── migrations/
│       ├── __init__.py/
│   ├── templates/
│      ├── fridge/
│          ├── add_to_inventory.html
│          ├── dashboard.html
│          ├── grid_view.html
│          ├── inventory_list.html
│          ├── shopping_list.html
│      ├── registration/
|          ├── login.html
|          ├── register.html
|      ├── base.html
│   ├── admin.py
│   ├── asgi.py
│   ├── forms.py
│   ├── models.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
├── manage.py
├── LICENSE
└── README.md
~~~

## Features
The system provides the following functionalities:
- **Add Items**: Add new items to the fridge with details such as name, quantity, and expiration date.
- **Remove Items**: Remove items from the fridge after usage.
- **Update Items**: Update the quantity or expiration date of existing items.
- **View Inventory**: View the list of items currently in the fridge.
- **Expiration Notifications**: Notify users of items nearing their expiration date.

## Prerequisites
- Python 3.12 or higher
- pip (Python package installer)
- Django

## How to access the application
~~~
# Reset the database if needed
# Delete the database file and all migration files except __init__.py
rm db.sqlite3
rm fridge/migrations/0*.py

# Create the database and migrations
python manage.py makemigrations
python manage.py migrate

# Create a new superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
~~~

## Run the test
~~~
# create the migrations
python manage.py makemigrations fridge

# apply the migrations
python manage.py migrate

# run the test.py
python manage.py test fridge
~~~
