
# Tasty Bites - Flask Application

Tasty Bites is a web application built with Flask that allows users to browse a menu, add dishes, place orders, and review orders. It provides features such as adding and removing dishes from the menu, updating dish availability, calculating total order prices, and filtering orders by status.

## Features

- **Menu Display:** Users can view the available dishes on the menu.
- **Add Dish:** Admin users can add new dishes to the menu, providing the dish name and price.
- **Remove Dish:** Admin users can remove existing dishes from the menu.
- **Update Availability:** Admin users can update the availability of a dish on the menu.
- **Place Order:** Users can place orders by selecting dishes from the menu and providing their name.
- **Review Orders:** Users can review all orders placed, including order details and status.
- **Update Order Status:** Admin users can update the status of an order.

## Additional Features
The project includes additional features that enhance the functionality of the web application:

**Price Calculation**: The web application calculates and displays the total price of each order based on the price of each ordered dish.

**Status Filter**: The order review page provides an option to filter orders by status, allowing users to view only orders with a specific status.

## Prerequisites

Make sure you have the following installed on your machine:

- Python (version 3.x)
- Flask (version 2.x)
- Other dependencies as specified in `requirements.txt`

## Getting Started

1. Clone the repository: `git clone https://github.com/DishaGup/tasty-bites-flask-application.git`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the application: `python zomato.py`
5. Access the application in your web browser at: `http://localhost:5000`

## Configuration

You can customize the application behavior by modifying the following files:

- `zomato.py`: This file contains the main Flask application code.
- `templates/`: This directory contains HTML templates for different pages.
- `static/css/styles.css`: This file contains the CSS styles for the application.

## Data Persistence

The application automatically saves the menu and order data to a `data.json` file in the project directory. This ensures that the data persists across multiple usages of the application.

## Contributing

Contributions to this project are welcome. If you find any issues or would like to suggest improvements, please create a new issue or submit a pull request.
