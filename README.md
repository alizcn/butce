# Budget Management System

A Django-based budget management system that helps organizations track and manage their budgets, forecasts, and actual expenses.

## Features

- Fiscal Year Management
- Budget Line and GL Account Management
- Budget Entry with Automatic Monthly Forecast Distribution
- Monthly Forecast Updates
- Actual Expense Import from Excel
- Comprehensive Budget vs Forecast vs Actual Reports
- Export Options for Reports

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd budget_project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the admin interface at `/admin` to:
   - Create Fiscal Years
   - Set up GL Accounts
   - Create Budget Lines
   - Link GL Accounts to Budget Lines

2. Use the main application to:
   - Create Budget Entries
   - Update Monthly Forecasts
   - Import Actual Expenses
   - View Reports

## Excel Import Format

The system expects Excel files for actual expense imports to have the following columns:
- `account_number`: The GL Account number
- `amount`: The expense amount

Example:
```
account_number | amount
1001          | 1000.00
1002          | 2500.50
```

## Development

### Project Structure
```
budget_project/
├── manage.py
├── budget_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── budget_app/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── forms.py
    ├── services.py
    ├── urls.py
    ├── views.py
    └── templates/
        └── budget_app/
            ├── base.html
            ├── dashboard.html
            ├── budget_entry.html
            ├── forecast_update.html
            ├── actual_import.html
            └── reports.html
```

### Key Components

- **Models**: Define the database structure for fiscal years, GL accounts, budget lines, etc.
- **Forms**: Handle data input and validation
- **Services**: Contain business logic for forecasting and importing data
- **Views**: Handle HTTP requests and render templates
- **Templates**: Define the UI using Bootstrap for responsive design

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. # butce
