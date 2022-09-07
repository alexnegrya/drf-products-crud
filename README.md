# DRF Products CRUD
Test app for make virtual products **CRUD** using **Django REST Framework** abilities.

## Installation

- Install PostgreSQL and create database "**testproject**"
- Clone repo - `git clone https://github.com/alexnegrya/drf-products-crud`
- Enter into "**drf-products-crud**" folder
- With already installed Python with Pip:
  - Install requirements - `pip install -r requirements.txt`
  - Enter into "**testproject**" folder
  - Migrate DRF models - `python manage.py migrate`
  - Make migrations for Products model - `python manage.py makemigrations testapp`
  - Migrate Products model - `python manage.py migrate`

## Usage

This works in folder "**testproject**".
- To run server execute default Django command for this - `python manage.py runserver`.
- Extra feature - manage Products models for test. Execute `python test_products.py <action>` for this. Supported actions:
  - `create` - Create test Products models
  - `delete` - Delete test Products models
