# Luxury Store ERP System

A comprehensive Enterprise Resource Planning (ERP) system designed for luxury goods stores. This system helps manage inventory, sales, customers, and financial operations efficiently.

## Features

- Inventory Management
- Sales Processing
- Customer Relationship Management
- Financial Management
- Supplier Management
- Employee Management
- Reporting and Analytics

## Technical Stack

- Python 3.9+
- Django 5.0.2
- Django REST Framework
- PostgreSQL
- Bootstrap 5

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the root directory with:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
luxury_store_erp/
├── apps/
│   ├── inventory/     # Inventory management
│   ├── sales/        # Sales and orders
│   ├── finance/      # Financial operations
│   └── users/        # User management
├── config/           # Project configuration
├── static/           # Static files
└── templates/        # HTML templates
```

## License

MIT License
#   R a d w a n -  
 #   R a d w a n -  
 "# Radwan-" 
