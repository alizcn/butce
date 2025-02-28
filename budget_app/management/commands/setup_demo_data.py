from django.core.management.base import BaseCommand
from django.utils import timezone
from budget_app.models import FiscalYear, GLAccount, BudgetLine, BudgetEntry, ForecastEntry

class Command(BaseCommand):
    help = 'Sets up demo data for the budget management system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating demo data...')

        # Create Fiscal Years
        self.create_fiscal_years()
        
        # Create GL Accounts
        self.create_gl_accounts()
        
        # Create Budget Lines
        self.create_budget_lines()
        
        # Create Budget Entries and Forecasts
        self.create_budget_entries()

        self.stdout.write(self.style.SUCCESS('Successfully created demo data'))

    def create_fiscal_years(self):
        current_year = timezone.now().year
        
        # Create fiscal years for current and next year
        FiscalYear.objects.get_or_create(
            year=current_year,
            defaults={'is_active': True}
        )
        FiscalYear.objects.get_or_create(
            year=current_year + 1,
            defaults={'is_active': False}
        )
        
        self.stdout.write('Created fiscal years')

    def create_gl_accounts(self):
        # Sample GL accounts
        accounts = [
            {'account_number': '5100', 'account_name': 'Salaries and Wages'},
            {'account_number': '5200', 'account_name': 'Employee Benefits'},
            {'account_number': '5300', 'account_name': 'Office Supplies'},
            {'account_number': '5400', 'account_name': 'Professional Services'},
            {'account_number': '5500', 'account_name': 'Utilities'},
            {'account_number': '5600', 'account_name': 'Rent'},
            {'account_number': '5700', 'account_name': 'Travel'},
            {'account_number': '5800', 'account_name': 'Training'},
            {'account_number': '5900', 'account_name': 'Marketing'},
            {'account_number': '6000', 'account_name': 'IT Equipment'},
        ]
        
        for account in accounts:
            GLAccount.objects.get_or_create(
                account_number=account['account_number'],
                defaults={'account_name': account['account_name']}
            )
        
        self.stdout.write('Created GL accounts')

    def create_budget_lines(self):
        # Sample budget lines
        budget_lines = [
            {'name': 'HR Department', 'description': 'Human Resources budget'},
            {'name': 'IT Department', 'description': 'Information Technology budget'},
            {'name': 'Marketing', 'description': 'Marketing and advertising budget'},
            {'name': 'Operations', 'description': 'General operations budget'},
            {'name': 'Finance', 'description': 'Finance department budget'},
        ]
        
        for line in budget_lines:
            BudgetLine.objects.get_or_create(
                name=line['name'],
                defaults={'description': line['description']}
            )
        
        self.stdout.write('Created budget lines')

    def create_budget_entries(self):
        active_year = FiscalYear.objects.get(is_active=True)
        budget_lines = BudgetLine.objects.all()
        
        # Create budget entries for each budget line
        for budget_line in budget_lines:
            # Generate a random annual amount between 10000 and 100000
            import random
            annual_amount = random.randint(10000, 100000)
            
            entry, created = BudgetEntry.objects.get_or_create(
                fiscal_year=active_year,
                budget_line=budget_line,
                defaults={'annual_amount': annual_amount}
            )
            
            if created:
                # Create monthly forecasts
                monthly_amount = annual_amount / 12
                for month in range(1, 13):
                    # Add some variation to monthly forecasts
                    variation = random.uniform(0.8, 1.2)
                    ForecastEntry.objects.get_or_create(
                        budget_entry=entry,
                        month=month,
                        defaults={'amount': monthly_amount * variation}
                    )
        
        self.stdout.write('Created budget entries and forecasts') 