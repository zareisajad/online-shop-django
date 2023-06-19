# Simple Online Shop: Manage Products and Orders with Django
![Screenshot 2022-01-09 at 17-04-55 Django Online Shop](https://user-images.githubusercontent.com/71011395/148684469-79bfdb07-efa0-4dde-ad76-1f3277f833e6.png)


This project is a simple but usable online shop written with Django. The app provides a custom dashboard to manage products and orders. Users can like a product, add it to the cart, and proceed to checkout. Order processing is supported, but the payment is handled using a fake pay system.

[Preview](#app-preview)

## Features

There are two types of users in this app: regular users and managers.

### Available to the Users:

- **Cart**: Users can manage items in their cart.
- **Edit Personal Information**: Users can update their personal details.
- **Orders**: Users can view their order history.
- **Favorites**: Users can like and save their favorite products.
- **Reset Password**: Users can reset their password using their registered email.

### Available to the Managers:

Managers can access all the features available to regular users, along with additional capabilities, through the custom dashboard accessible at [http://127.0.0.1:8000/accounts/login/manager](http://127.0.0.1:8000/accounts/login/manager).

- **Add Product**: Managers can add new products to the shop.
- **Edit and Delete Product**: Managers can modify or remove existing products.
- **Add New Category**: Managers have the ability to create new categories for products.
- **Access to Orders**: Managers can view and manage all orders and order items.

## Technologies Used

- Python 3
- Django
- Bootstrap
- SQLite3 database

## How to Run the Application

1. Clone or download the project to your local machine.
2. Change directory to the "online-shop-django" folder.
3. Ensure that you have Python 3, pip, and virtualenv installed on your machine.
4. Create a virtual environment using the following command:
   - For Mac and Linux: `python3 -m venv venv`
   - For Windows: `python -m venv venv`
5. Activate the virtual environment:
   - For Mac and Linux: `source venv/bin/activate`
   - For Windows: `venv\scripts\activate`
6. Install the application requirements by running: `pip install -r requirements.txt`
7. Migrate the database by executing: `python manage.py migrate`
8. Start the server: `python manage.py runserver`
9. You should now be able to access the application by visiting: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Manager Dashboard Access

To access the custom dashboard for managers, please use the following credentials:

- Email: manager@example.com
- Password: managerpass1234

## How to Contribute

I welcome contributions to enhance and customize this project. If you would like to contribute, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name for your feature or bug fix.
3. Make the necessary changes in your branch.
4. Test your changes thoroughly.
5. Commit your changes and push them to your forked repository.
6. Submit a pull request, clearly describing the changes you have made.

## License

released under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the terms of the license.

Feel free to explore, contribute, and customize this according to your needs!


## App Preview
![Peek 2022-01-09 19-15](https://user-images.githubusercontent.com/71011395/148689722-6ceacc8f-81b7-48e0-a258-9d4e543d1e7c.gif)
