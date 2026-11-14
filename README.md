# 🌱 FarmDirect --- Farmer-to-Consumer Marketplace

**FarmDirect** is a Django-based web application that connects farmers
directly with customers, helping reduce dependence on multiple
intermediaries in the agricultural supply chain. Farmers can publish
agricultural products, manage their listings and available stock, while
customers can discover fresh produce, search and filter listings, add
products to a cart, and place orders.


## 📚 Table of Contents

-   [Overview](#-project-overview)
-   [Problem Statement](#-problem-statement)
-   [Objectives](#-objectives)
-   [Features](#-features)
-   [User Roles and Workflows](#-user-roles-and-workflows)
-   [Technology Stack](#-technology-stack)
-   [Project Structure](#-project-structure)
-   [Installation and Setup](#-installation-and-setup)
-   [How to Use](#-how-to-use)
-   [Database Design](#-database-design)
-   [Application URLs](#-application-urls)
-   [Screenshots](#-screenshots)
-   [Current Limitations](#-current-limitations)
-   [Future Enhancements](#-future-enhancements)
-   [Troubleshooting](#-troubleshooting)
-   [Production Checklist](#-production-readiness-checklist)
-   [Contributing](#-contributing)
-   [License](#-license)

------------------------------------------------------------------------

## 🌾 Project Overview

Traditional agricultural supply chains can involve several
intermediaries between farmers and consumers. This can reduce the share
of the final selling price received by farmers and increase the price
paid by customers.

FarmDirect provides a simple digital marketplace where farmers can
create accounts and list agricultural products with prices,
descriptions, available quantities, and optional product images.
Customers can browse the marketplace, search and filter products, add
items to a session-based cart, and place orders by providing delivery
details.

The application provides separate farmer and customer experiences, along
with Django's built-in administration interface for managing marketplace
data.

## ❗ Problem Statement

Farmers may have limited direct access to customers and may depend on
multiple intermediaries to sell their produce. Customers may also find
it difficult to discover local agricultural products and identify the
sellers.

FarmDirect addresses this problem by creating a direct digital
connection between farmers and customers.

## 🎯 Objectives

-   Give farmers a simple way to publish and manage product listings.
-   Help customers discover agricultural products in one place.
-   Support product search and category-based filtering.
-   Provide a basic cart and order placement workflow.
-   Update product stock when an order is successfully placed.
-   Demonstrate a multi-role marketplace built with Django.

------------------------------------------------------------------------

## ✨ Features

### 👨‍🌾 Farmer Features

-   **Farmer registration:** Create an account by selecting the Farmer
    role and providing farm details.
-   **Farmer dashboard:** View the farmer's own product listings.
-   **Product management (CRUD):** Add, view, edit, and delete products.
-   **Product information:** Store product name, category, description,
    price, available quantity, and optional image.
-   **Availability management:** Mark products as available or
    unavailable.
-   **Stock visibility:** Display the remaining quantity for each
    listing.

### 🛒 Customer Features

-   **Customer registration and login:** Create and access a customer
    account.
-   **Marketplace browsing:** Explore available agricultural products.
-   **Search:** Search product names, descriptions, and farmer names.
-   **Category filtering:** Filter listings by product category.
-   **Product details:** View product information, farmer name,
    location, price, and available quantity.
-   **Session-based cart:** Add products, update quantities, and remove
    cart items.
-   **Checkout:** Submit customer name, phone number, and delivery
    address.
-   **Order history:** View placed orders and their current status.

### 🛠️ Admin Features

-   Manage farmer profiles, customer profiles, products, and orders
    through Django Admin.
-   Review marketplace records from the administration interface.
-   Manage the farmer verification flag through the admin interface.
-   Inspect order items and order statuses.

### 📦 Order and Inventory Workflow

1.  Customers add available products to their cart.
2.  The application validates requested quantities against available
    stock.
3.  At checkout, stock is checked again before an order is created.
4.  Order items retain the product price at the time of ordering.
5.  Product quantities are reduced after a successful order.
6.  A product is marked unavailable when its remaining quantity reaches
    zero.

------------------------------------------------------------------------

## 👥 User Roles and Workflows

  -----------------------------------------------------------------------
  Role                                Main capabilities
  ----------------------------------- -----------------------------------
  Farmer                              Register, manage farm details, list
                                      products, update listings and stock

  Customer                            Register, browse products, search,
                                      filter, manage cart and place
                                      orders

  Admin                               Manage marketplace records and
                                      inspect orders through Django Admin
  -----------------------------------------------------------------------

### Farmer workflow

1.  Open `/signup/`.
2.  Select **Farmer** as the account type.
3.  Enter a username, email, password, farm name, and farm location.
4.  Complete registration and open the Farmer Dashboard.
5.  Add a product with its price, quantity, category, description, and
    optional image.
6.  Edit or delete the listing when required.

### Customer workflow

1.  Register with the **Customer** account type.
2.  Browse the marketplace.
3.  Search for a product or filter by category.
4.  Open a product's detail page.
5.  Add the required quantity to the cart.
6.  Review or update cart quantities.
7.  Enter delivery details and place the demo Cash on Delivery order.
8.  Open **My Orders** to review the order.

------------------------------------------------------------------------

## 🧰 Technology Stack

  -----------------------------------------------------------------------
  Layer                   Technology              Purpose
  ----------------------- ----------------------- -----------------------
  Programming language    Python                  Application logic

  Backend framework       Django 5.2              Routing, views,
                                                  authentication, ORM,
                                                  admin

  Frontend                HTML5                   Page structure

  Styling                 CSS3                    Custom styling

  UI framework            Bootstrap 5.3           Responsive layout and
                                                  components

  Client-side scripting   JavaScript              Interface interactions

  Database                SQLite                  Local development
                                                  database

  Image handling          Django `ImageField`     Optional product image
                                                  uploads

  Pagination              Django Paginator        Paginated product
                                                  listings

  Version control         Git and GitHub          Source code management
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 📁 Project Structure

``` text
FarmDirect/
│
├── farmdirect/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── marketplace/
│   ├── migrations/
│   │   └── __init__.py
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── form_tags.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── marketplace/
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── farmer_dashboard.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── my_orders.html
│   │   ├── product_detail.html
│   │   ├── product_form.html
│   │   └── signup.html
│   └── base.html
│
├── static/
│   └── css/
│       └── style.css
│
├── media/
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

> `db.sqlite3` and uploaded media are created or populated while running
> the application. They should not normally be committed as part of the
> source code repository.

------------------------------------------------------------------------

## 🚀 Installation and Setup

### 1. Prerequisites

Make sure you have installed:

-   Python 3.10 or later
-   pip (Python package installer)
-   Git (optional, for cloning)
-   A code editor such as Visual Studio Code

Check your Python installation:

``` bash
python --version
```

On Windows, you can also use:

``` powershell
py --version
```

### 2. Clone the repository

Replace the placeholders with your GitHub username and repository name:

``` bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

Alternatively, download and extract the repository ZIP.

### 3. Create a virtual environment

**Windows PowerShell:**

``` powershell
py -m venv venv
```

**macOS / Linux:**

``` bash
python3 -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

``` powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

``` cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**

``` bash
source venv/bin/activate
```

### 5. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Create and apply database migrations

Generate migration files for the marketplace app:

``` bash
python manage.py makemigrations marketplace
```

Apply migrations and create the SQLite database tables:

``` bash
python manage.py migrate
```

### 7. Create an administrator account

``` bash
python manage.py createsuperuser
```

Follow the prompts to create your administrator username and password.

### 8. Start the development server

``` bash
python manage.py runserver
```

Open the application:

-   **Marketplace:** http://127.0.0.1:8000/
-   **Django Admin:** http://127.0.0.1:8000/admin/

To stop the server, press `Ctrl + C` in the terminal.

------------------------------------------------------------------------

## 🧪 How to Use

A quick way to test the marketplace is to create one farmer account and
one customer account.

### Test as a farmer

1.  Go to `/signup/`.
2.  Select the Farmer account type.
3.  Fill in the farm name and location.
4.  Complete registration.
5.  Open the Farmer Dashboard.
6.  Select **Add Product** and enter sample product information.
7.  Save the listing.

### Test as a customer

1.  Log out of the farmer account.
2.  Register a new account as a Customer.
3.  Return to the marketplace homepage.
4.  Find a product added by the farmer.
5.  Open the product and add a quantity to the cart.
6.  Update the cart if needed.
7.  Proceed to checkout and submit delivery information.
8.  Open **My Orders** to view the placed order.

### Test as an administrator

1.  Visit `/admin/`.
2.  Sign in using the superuser credentials.
3.  Inspect farmer profiles, customer profiles, products, orders, and
    order items.
4.  Update the farmer verification flag or order status when
    appropriate.

------------------------------------------------------------------------

## 🗄️ Database Design

The application uses Django ORM models to store marketplace data.

  -----------------------------------------------------------------------
  Model                               Purpose
  ----------------------------------- -----------------------------------
  `FarmerProfile`                     Farm name, farmer contact number,
                                      location, and verification status

  `CustomerProfile`                   Customer contact number and address

  `Product`                           Product details, category, price,
                                      available quantity, image, and
                                      farmer

  `Order`                             Customer details, delivery
                                      information, total amount, status,
                                      and creation time

  `OrderItem`                         Product, quantity, farmer
                                      reference, and price per kg for
                                      each order
  -----------------------------------------------------------------------

### Main relationships

-   Each farmer profile is linked to one Django user.
-   Each customer profile is linked to one Django user.
-   A farmer can publish multiple products.
-   A customer can place multiple orders.
-   An order can contain multiple order items.
-   Each order item references the product and farmer associated with
    that purchase.

------------------------------------------------------------------------

## 🔗 Application URLs

  URL                              Description
  -------------------------------- ---------------------------
  `/`                              Marketplace homepage
  `/signup/`                       User registration
  `/login/`                        User login
  `/logout/`                       User logout
  `/product/<id>/`                 Product details
  `/farmer/dashboard/`             Farmer dashboard
  `/farmer/product/add/`           Add a product
  `/farmer/product/<id>/edit/`     Edit a product
  `/farmer/product/<id>/delete/`   Delete a product
  `/cart/`                         Shopping cart
  `/cart/add/<id>/`                Add a product to the cart
  `/checkout/`                     Checkout
  `/orders/`                       Customer order history
  `/admin/`                        Django administration

------------------------------------------------------------------------

## 🖼️ Screenshots

Add screenshots of your running application to help visitors understand
the project.

Create a `screenshots/` directory and save your actual application
screenshots there. Then add them to this section.

``` markdown
### Marketplace Homepage
![FarmDirect Marketplace](screenshots/homepage.png)

### Farmer Dashboard
![Farmer Dashboard](screenshots/farmer-dashboard.png)

### Product Details
![Product Details](screenshots/product-details.png)

### Shopping Cart
![Shopping Cart](screenshots/cart.png)

### Checkout
![Checkout](screenshots/checkout.png)
```

Only add images after capturing them from your working application.

------------------------------------------------------------------------

## ⚠️ Current Limitations

FarmDirect is an educational MVP. The following features are not
implemented or need further work before real-world deployment:

-   **Payment processing:** Checkout currently demonstrates a Cash on
    Delivery flow. No online payment gateway is connected.
-   **Demand forecasting:** AI/ML-based forecasting is not included in
    the current version.
-   **Farmer verification:** The verification flag is managed through
    Django Admin; no automated verification workflow exists.
-   **Delivery tracking:** Live delivery or courier tracking is not
    provided.
-   **Notifications:** Email, SMS, and push notifications are not
    integrated.
-   **Production database:** SQLite is used for local development. A
    production deployment with concurrent users should use a
    production-ready database such as PostgreSQL.
-   **Production security:** Development settings must be hardened
    before public deployment.

------------------------------------------------------------------------

## 🔮 Future Enhancements

These are potential next steps for the project, not features currently
available.

### 🤖 AI-Based Demand Forecasting

Use historical order and sales data to estimate future demand for
agricultural products. A forecasting module could help farmers make more
informed decisions about stock and harvest planning.

Potential tools:

-   Pandas for data preparation
-   NumPy for numerical operations
-   Scikit-learn for baseline forecasting models
-   Matplotlib for analysis and visualizations

Forecasting should be trained and evaluated using real or responsibly
collected historical data. It is not part of the current MVP.

### 💰 Market Price Insights

-   Show market price information from reliable data sources.
-   Compare listed prices with available market reference prices.
-   Provide transparent price information to farmers and customers.

### 📍 Location-Based Discovery

-   Help customers discover nearby farmers.
-   Add map-based farm locations.
-   Explore delivery distance and service-area information.

### 🚚 Delivery Management

-   Add delivery partner accounts.
-   Track order fulfilment stages.
-   Provide delivery status updates.

### 💳 Online Payments

-   Integrate a suitable payment gateway.
-   Add payment status tracking.
-   Handle failed, pending, and successful transactions safely.

### 📊 Analytics Dashboards

-   Show farmer sales summaries.
-   Visualize popular products.
-   Display order and inventory trends.
-   Provide administrative marketplace statistics.

### 🔔 Notifications and Communication

-   Send email order confirmations.
-   Notify farmers about new orders.
-   Notify customers about order status changes.

------------------------------------------------------------------------

## 🧯 Troubleshooting

### Error: `no such table: marketplace_product`

This means the marketplace database table has not been created. Run:

``` bash
python manage.py makemigrations marketplace
python manage.py migrate
```

Then verify:

``` bash
python manage.py showmigrations marketplace
```

The initial marketplace migration should be marked with `[X]` after it
has been applied.

### Error: `No changes detected`

Check that:

1.  `marketplace` is included in `INSTALLED_APPS` in
    `farmdirect/settings.py`.
2.  Your model classes are saved in `marketplace/models.py`.
3.  The `marketplace/migrations/` directory exists.
4.  The migrations directory contains an `__init__.py` file.
5.  You are running commands from the directory containing `manage.py`.

### Error: `ModuleNotFoundError`

Activate your virtual environment and reinstall dependencies:

``` bash
pip install -r requirements.txt
```

### Product images are not displayed

Check that:

-   The product was saved with an image.
-   `MEDIA_URL` and `MEDIA_ROOT` are configured in `settings.py`.
-   Media URL routing is enabled for local development.
-   The uploaded image exists under the configured media directory.

------------------------------------------------------------------------

## 🔐 Production Readiness Checklist

Before deploying this application publicly:

-   [ ] Move `SECRET_KEY` into an environment variable.
-   [ ] Set `DEBUG = False`.
-   [ ] Configure `ALLOWED_HOSTS`.
-   [ ] Configure HTTPS and secure cookie settings.
-   [ ] Use PostgreSQL or another appropriate production database.
-   [ ] Configure static and media file hosting.
-   [ ] Validate uploaded files and restrict file types and sizes.
-   [ ] Add email verification and password recovery workflows.
-   [ ] Add appropriate authorization checks and rate limiting.
-   [ ] Review checkout, inventory concurrency, and order cancellation
    logic.
-   [ ] Integrate and test a payment provider if online payments are
    required.
-   [ ] Add automated tests, logging, backups, and error monitoring.

Do not use Django's development server as a production server.

------------------------------------------------------------------------

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1.  Fork the repository.

2.  Create a feature branch:

    ``` bash
    git checkout -b feature/your-feature-name
    ```

3.  Make your changes and test them.

4.  Commit your changes:

    ``` bash
    git commit -m "Add: describe your changes"
    ```

5.  Push your branch:

    ``` bash
    git push origin feature/your-feature-name
    ```

6.  Open a Pull Request describing your changes.

------------------------------------------------------------------------

## 📄 License

No license has been selected for this repository yet. Add a `LICENSE`
file before describing the project as open source or permitting reuse.

------------------------------------------------------------------------

## 👨‍💻 Author

**FarmDirect --- Farmer-to-Consumer Marketplace**

Built as a learning project to explore Python, Django, database design,
authentication, CRUD operations, and full-stack web application
development.

If you find this project useful, consider giving the repository a ⭐ on
GitHub.

------------------------------------------------------------------------

```{=html}
<p align="center">
```
`<strong>`{=html}🌱 FarmDirect --- Connecting Farmers Directly with
Customers.`</strong>`{=html}`<br>`{=html} Fresh produce. Fair prices. A
better-connected marketplace.
```{=html}
</p>
```
