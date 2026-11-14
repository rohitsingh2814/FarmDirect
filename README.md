# FarmDirect — Django + Bootstrap + SQLite

A starter farmer-to-consumer marketplace MVP.

## Features
- Customer and farmer registration/login
- Farmer product CRUD dashboard
- Product marketplace with search/category filter and pagination
- Session-based shopping cart
- Checkout with cash-on-delivery demo flow
- Customer order history
- Django admin

## Requirements
- Python 3.10+
- Internet connection for Bootstrap CDN and optional Unsplash hero background

## Setup (Windows PowerShell)
```powershell
py -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations marketplace
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Setup (macOS/Linux)
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations marketplace
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Test the app
1. Register a user and choose Farmer. Add farm name and location.
2. Open Farmer dashboard and add a product.
3. Log out and register a second user as Customer.
4. Browse products, add a quantity to cart, and place a demo COD order.
5. Log in to `/admin/` to inspect users, products and orders.

## Notes / next improvements
- This is an educational MVP. Checkout is cash-on-delivery only; no payment gateway is integrated.
- Farmer verification is an admin-managed flag.
- Demand forecasting is intentionally not included in this first working version. Add it after collecting sales history; do not train a model on fabricated data.
- Before production: set a strong SECRET_KEY via environment variables, set DEBUG=False, configure ALLOWED_HOSTS, HTTPS, secure cookies, email verification, upload validation, rate limiting, and proper payment/delivery integrations.
- For production-grade inventory, consider reservation/locking and a payment/order state workflow. SQLite is suitable for learning and local demos; use PostgreSQL for concurrent production traffic.
