# DRF Products CRUD
Django web app for virtual products **CRUD** using **Django REST Framework**.

## Installation

- Install PostgreSQL and create database "**drf_products_crud**" - `sudo -u postgres psql -c 'create database drf_products_crud owner postgres'`
- Clone repo - `git clone https://github.com/alexnegrya/drf-products-crud`
- Enter into project folder ("**drf-products-crud**")
- With already installed Python with Pip:
  - Install requirements - `pip install -r requirements.txt`
  - Enter into "**project**" folder
  - Apply Django migrations - `python manage.py migrate`

## Usage

This works in folder "**project**" only.
- To run server execute default Django command for this - `python manage.py runserver`.
- Extra feature - manage Products models for test. Execute `python test_products.py <action>` for this. Supported actions:
  - `create` - Create test Products models
  - `delete` - Delete test Products models
