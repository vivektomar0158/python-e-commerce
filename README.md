# South Side Shopping - E-commerce Platform

<img width="500" height="500" alt="Screenshot 2026-02-09 231804" src="https://github.com/user-attachments/assets/695f08d9-c152-4454-acbf-15c9db89517f" />
<img width="500" height="500" alt="Screenshot 2026-02-09 231901" src="https://github.com/user-attachments/assets/d0c44325-e738-49d8-ba3f-c1e8b66164e8" />
<img width="500" height="500" alt="Screenshot 2026-02-09 231815" src="https://github.com/user-attachments/assets/551e6df8-11b5-4ebb-9e15-2ccfaacdaa75" />
<img width="500" height="500" alt="Screenshot 2026-02-09 232352" src="https://github.com/user-attachments/assets/ac3c8977-ad44-47d9-ae73-68bef89301a5" />


**Tagline:** *If it's not South Side, it's not the best!*

A complete Django-based e-commerce platform with Stripe payment integration, built for local development.

## Features

✅ User authentication (Register, Login, Profile)  
✅ Product catalog with 6 categories  
✅ Shopping cart functionality  
✅ Stripe payment integration (test mode)  
✅ Order management and history  
✅ Responsive design (Mobile, Tablet, Desktop)  
✅ Admin panel for product management  
✅ Email notifications (console backend)  
✅ Search functionality  

## Tech Stack

- **Backend:** Django 5.0.1, Python 3.12
- **Database:** SQLite
- **Frontend:** Bootstrap 5, Alpine.js
- **Payments:** Stripe (test mode)
- **Images:** Pillow

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Populate Database

```bash
python manage.py populate_db
```

This command creates:
- 6 product categories (Electronics, Fashion, Home & Living, Sports & Fitness, Books & Media, Beauty & Health)
- 19 products with images and descriptions

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

## Admin Panel

Access the admin panel at: **http://localhost:8000/admin/**

Use the superuser credentials you created to login.

### Admin Features:
- Add/Edit/Delete products
- Manage categories
- View and update orders
- Manage users

## Project Structure

```
e-commerce/
├── config/              # Project settings
├── shop/                # Main e-commerce app
│   ├── models.py        # Category, Product, Cart, Order models
│   ├── views.py         # All shop views
│   ├── admin.py         # Admin configuration
│   └── management/      # Custom commands
├── accounts/            # User management
│   ├── models.py        # UserProfile model
│   └── views.py         # Auth views
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── shop/            # Shop templates
│   └── accounts/        # Auth templates
├── static/              # CSS, JS files
│   └── css/style.css    # Custom styles
├── media/               # Uploaded images
│   ├── categories/      # Category images
│   └── products/        # Product images
└── db.sqlite3           # SQLite database
```

## Usage Guide

### For Customers:

1. **Browse Products**
   - Visit homepage to see all categories
   - Click on a category to view products
   - Use search bar to find specific products

2. **Shopping**
   - Click on a product to view details
   - Add products to cart
   - Update quantities or remove items in cart

3. **Checkout**
   - Click "Proceed to Checkout"
   - Fill in delivery information
   - Use test card: `4242 4242 4242 4242` (any future date, any CVV)
   - Place order

4. **Account**
   - Register for an account
   - View order history
   - Update profile information

### For Admins:

1. **Login to Admin Panel**
   - Go to http://localhost:8000/admin/
   - Login with superuser credentials

2. **Manage Products**
   - Add new products with images
   - Edit existing products
   - Update stock quantities
   - Activate/deactivate products

3. **Manage Orders**
   - View all orders
   - Update order status
   - View customer details

## Stripe Test Cards

Use these test cards for payment testing:

- **Success:** 4242 4242 4242 4242
- **Declined:** 4000 0000 0000 0002
- **Insufficient Funds:** 4000 0000 0000 9995

Any future expiry date and any 3-digit CVV will work.

## Configuration

### Environment Variables

The following settings are configured in `config/settings.py`:

```python
STRIPE_PUBLIC_KEY = 'pk_test_51ExamplePublicKey123456789'
STRIPE_SECRET_KEY = 'sk_test_51ExampleSecretKey123456789'
```

**Note:** These are example keys. Replace with your actual Stripe test keys if needed.

### Email Settings

Emails are configured to print to console (development mode):

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'orders@southside.com'
```

## Contact Information

- **Phone:** +91-8882152077
- **Email:** orders@southside.com
- **Website:** South Side Shopping

## Database Schema

### Models:

- **Category:** Product categories with images
- **Product:** Products with price, stock, images
- **Cart/CartItem:** Shopping cart for logged-in users
- **Order/OrderItem:** Order history and details
- **UserProfile:** Extended user information

## Troubleshooting

### Issue: Images not showing

**Solution:** Make sure you've copied images to the media folder:
```bash
xcopy /E /I "images" "media"
```

### Issue: Stripe payment fails

**Solution:** Verify you're using test card `4242 4242 4242 4242`

### Issue: Can't login to admin

**Solution:** Create a superuser:
```bash
python manage.py createsuperuser
```

## Development Notes

- This is a **development/demo** project running on localhost
- SQLite database is used for simplicity
- Stripe is in **test mode** - no real payments are processed
- Email notifications print to console instead of sending actual emails

## Future Enhancements (Not in v1.0)

- Guest checkout
- Product reviews and ratings
- Wishlist functionality
- Multiple payment methods
- Coupon/discount system
- Advanced analytics
- Mobile app

---

**Built with ❤️ for South Side Shopping**

*If it's not South Side, it's not the best!*
