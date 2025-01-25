Fridge inventory management system/
├── mysite/
│ ├── _init_.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
├── src/
│ ├── controllers/
│ ├── ├── fridgeController.js
| ├── routes/
| ├── ├── api.js
├── polls/
│ ├── _init_.py
│ ├── admin.py
│ ├── api_config.py
│ ├── apps.py
│ ├── auth.py
│ ├── middleware.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ ├── views.py
| ├── static/polls/js/
| ├── ├── api.js
| ├── templates/
| ├── ├── base.html
| ├── ├── polls/
| ├── ├── ├── add_to_inventory.html
| ├── ├── ├── grid_view.html
| ├── ├── ├── index.html
| ├── ├── ├── inventory_list.html
| ├── ├── ├── shopping_list.html
├── manage.py
└── README.md

## Prerequisites
- Python 3.12 or higher
- pip (Python package installer)
- SQLite3

## Installation
1. Clone the repository:

git clone https://github.com/yourusername/fridge-inventory.git
cd fridge-inventory

2. Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

## Usage
### Running the Application
1. Start the application:
