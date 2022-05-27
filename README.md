# Django Online Shop
![Screenshot 2022-01-09 at 17-04-55 Django Online Shop](https://user-images.githubusercontent.com/71011395/148684469-79bfdb07-efa0-4dde-ad76-1f3277f833e6.png)
a really simple but usable online shop written with django. this app provides a custom dashboard to manage the products and orders,
users can like a product and add it to the cart, checkout and order is supported but the payment handled with a fake pay.  

[Preview](#app-preview)

## Features:
there is two kind of user in this app: user and manager.

available to the user:
- cart
- edit personal information
- orders
- favorites
- reset password using email

manager can access all these features  
in the custom dashboard in this address: http://127.0.0.1:8000/accounts/login/manager  
email: manager@example.com  
password: managerpass1234  

- add product
- edit and delete a product
- add new category
- access to all orders and order items


## Used in this app:
- python3
- django 
- bootstrap
- sqlite3 database


## How To Run it:
1. clone or download the project.
2. change directory to ``` online-shop-django```
3. make sure you have ``python3``, ```pip``` and ```virtualenv``` installed in your machine.
4. create virtualenv: ```python3 -m venv venv```
5. active virtualenv: Mac & Linux os: ```source venv/bin/activate```, Windows os: ```venv\scripts\activate```
6. install app requirements: ```pip install -r requirements.txt```
7. databse migrate: ```python manage.py migrate```
8. run the server: ```python manage.py runserver```
9. you should be able to open this address now: http://127.0.0.1:8000/

## App Preview
![Peek 2022-01-09 19-15](https://user-images.githubusercontent.com/71011395/148689722-6ceacc8f-81b7-48e0-a258-9d4e543d1e7c.gif)
