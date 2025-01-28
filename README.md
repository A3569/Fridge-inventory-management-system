# Fridge Inventory Management System
The **Fridge Inventory Management System** is a Python-based application designed to help users efficiently manage their fridge inventory. This system tracks items in the fridge, monitors their quantities, and notifies users about upcoming expirations. It is ideal for personal use, meal planning, or reducing food waste.

# File structures
~~~
Fridge inventory management system/
├── mysite/
│   ├── _init_.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── src/
│   ├── controllers/
│       ├── fridgeController.js
|   ├── routes/
|       ├── api.js
├── polls/
│   ├── _init_.py
│   ├── admin.py
│   ├── api_config.py
│   ├── apps.py
│   ├── auth.py
│   ├── middleware.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
|   ├── static/polls/js/
|       ├── api.js
|       ├── templates/
|       ├── base.html
|       ├── polls/
|       ├── add_to_inventory.html
|       ├── grid_view.html
|       ├── index.html
|       ├── inventory_list.html
|       ├── shopping_list.html
├── manage.py
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

## How to run the Application
~~~
python manage.py runserver
~~~

## How to test the system
~~~
python manage.py test polls.tests
~~~
