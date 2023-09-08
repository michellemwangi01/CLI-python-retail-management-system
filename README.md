# Restaurant Retail Management System (RetailPro)
![python version](https://img.shields.io/badge/python-3.10.12+-blue.svg)
![faker version](https://img.shields.io/badge/faker-1.12.0-mint.svg)
![alembic version](https://img.shields.io/badge/alembic-1.12.0-orange.svg)
![platforms](https://img.shields.io/badge/Platforms-Linux%20|%20Windows%20|%20Mac%20-purple.svg)
![SQLAlchemy version](https://img.shields.io/badge/SQLAlchemy-2.0.20-cyan.svg)


## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Database Setup](#database-setup)
- [Command Line Interface (CLI)](#command-line-interface-cli)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This Retail Management System is a comprehensive software solution designed to streamline and automate various aspects of managing a retail business. It offers a range of features and tools to help retailers manage inventory, track sales, handle customers, and more.

## Features
### 1. User Management
- **Login:** Allows users to login to the app
- **User authorization:** Checks user authorization to allow access to specific commands

### 1. Customer Management
- **Add Customer:** Add a new customer to customer table
- **Delete Customer:** Delete an existing customer record and its related purchase records
- **View purchase history:** View purchase history for specific customer
- **Update Customer:** Update a customer record
- **View-customer-details :** View full customer details, all customers or a filtered customer
- **Loyalty-points:** Keep track of customer loyalty points calculated based on purchase 

### 2. Inventory Management
- **New Category:** Delete a product category
- **Update Category:** Update existing category details
- **Delete Category:** Delete a product category and update its related records
- **View-customer-details :** View full customer details
- **Maintain Inventory:** Update product count everytime a purchase is made 

### 3. Product Management
- **Add-product:** Add a new product
- **Update-product:** Update an existing product
- **Delete-product:** Delete a product and it's related records
- **View-category-products :** View the all the products of specific category
- **View-product-details :** View full product details 
- **View-supplier-products :** View the all the products of specific supplier

### 1. Sales Management
- **Customer-purchase-history:** View customer purchase history
- **Make-purchase:** Customers can make purchases
- **View-product-purchase-details:** View product purchases

### 1. Supplier Management

- **Delete-supplier:** Allows user to delete existing suppliers
- **New-supplier:** Can add new suppliers
- **Update-supplier :** Update details for an existing supplier
- **View-suppliers:** View supplier details


## Getting Started

### Prerequisites

Before you can run the Retail Management System, ensure you have the following prerequisites installed:

- Python3 v3.10 +

- SQLAlchemy v2.0.20

- Alembic v1.12.0

- Faker v19.3.1

- click

- Virtual environment (optional but recommended)

### Installation

1. Clone the repository:
   ```sh
   git clone git@github.com:michellemwangi01/CLI-python-retail-management-system.git

### Packages

- alembic: 1.8.1
- Faker: 14.2.0
- importlib-metadata: 6.0.0
- importlib-resources: 5.10.0
- ipdb: 0.13.9
- SQLAlchemy: 1.4.41
- importlib-metadata = "6.0.0"
- importlib-resources = "5.10.0"

### Requires

- Python Version: 3.10.12

## Project Setup

### 1. Clone the repository

```

git clone https://github.com/michellemwangi01/CLI-python-retail-management-system/

```

### 2. Navigate to the project directory

```

cd CLI-python-retail-management-system

```

### 3. Install required dependencies

In the project directory, install the required dependencies

```

pipenv install

```

### 4. Enter the virtual enviroment

```

pipenv shell

```

### 6. Testing methods

all the testing methods are in the app.py file, uncomment them and run the file
`python3 app.py`

## Usage
1. Configure the application settings and database connection.
2. Initialize the database and create necessary tables.
3. Run the application using the command-line interface (CLI).

## Database Setup
![DatabaseStructure.png](Images%2FDatabaseStructure.png)
Run the following command to initialize the database and create necessary tables:
```
python3 seed.py

```
## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and commit them with clear commit messages.
Push your changes to your fork.
Create a pull request to the main repository.

## Authors & License

Authored by:

[Michelle Mwangi](https://github.com/Michellemwangi01)

Licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
