# Catalog Web Application

This is project 3 for the Udacity course ["Full Stack Web Developer Nanodegree"](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

This project implements a catalog web application. Utilizing Python, SQLite, SQLAlchemy, and the Flask framework; it provides CRUD functionality to a database of categories and related items.

User authentication is provided by Google Plus or Facebook OAuth providers. Login buttons provided at top-left of screen.

Front-end template is from ["Get Bootstrap"](http://getbootstrap.com/).

## How To Use

Install Vagrant and VirtualBox.

Clone the ["fullstack-nanodegree-vm"](http://github.com/udacity/fullstack-nanodegree-vm).

Launch the Vagrant VM (vagrant up).

Create database with the command python /vagrant/catalog/database_setup.py.

Load a sample database with the command python /vagrant/catalog/catalogData.py.

Run the application within the VM (python /vagrant/catalog/project.py).

Access and test your application by visiting http://localhost:5000 locally.

## Dependancies

The following extra Python packages are required for this application.

(pip install xxx)

Flask, SQLAlchemy, requests, httplib2, oauth2client.
