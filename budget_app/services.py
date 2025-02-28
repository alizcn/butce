import pandas as pd
from decimal import Decimal
from django.db import transaction
from .models import FiscalYear, GLAccount, BudgetLine, BudgetEntry, ForecastEntry, ActualExpense

class BudgetService:
    @staticmethod
    def initialize_forecasts(budget_entry):
        """Create initial forecast entries based on budget (equal distribution across months)"""
        monthly_amount = budget_entry.annual_amount / 12
        
        for month in range(1, 13):
            ForecastEntry.objects.create(
                budget_entry=budget_entry,
                month=month,
                amount=monthly_amount
            )
    
    @staticmethod
    def recalculate_forecast(budget_line, fiscal_year, month):
        """Implement your forecast calculation logic here"""
        # This is a simple example - you would replace this with your actual formula
        # For example, you might use previous months' actuals to adjust forecasts
        
        budget_entry = BudgetEntry.objects.get(budget_line=budget_line, fiscal_year=fiscal_year)
        forecast_entry = ForecastEntry.objects.get(budget_entry=budget_entry, month=month)
        
        # Get actuals for this budget line from previous months in this fiscal year
        gl_accounts = budget_line.gl_accounts.all()
        actuals = ActualExpense.objects.filter(
            gl_account__in=gl_accounts, 
            fiscal_year=fiscal_year, 
            month__lt=month
        )
        
        # Example formula: if we have actuals, use their average trend, otherwise use budget/12
        if actuals.exists():
            avg_actual = sum(a.amount for a in actuals) / actuals.count()
            forecast_entry.amount = avg_actual
        else:
            forecast_entry.amount = budget_entry.annual_amount / 12
        
        forecast_entry.save()
        return forecast_entry
    
    @staticmethod
    @transaction.atomic
    def import_actuals_from_excel(file, fiscal_year, month):
        """Import actual expenses from Excel file"""
        df = pd.read_excel(file)
        
        # Validate Excel structure - this will depend on your file format
        required_columns = ['account_number', 'amount']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Excel file missing required columns")
        
        # Clear existing actuals for this month and year
        ActualExpense.objects.filter(fiscal_year=fiscal_year, month=month).delete()
        
        # Import new actuals
        actuals_created = 0
        accounts_not_found = []
        
        for _, row in df.iterrows():
            account_number = str(row['account_number'])
            amount = Decimal(str(row['amount']))
            
            try:
                gl_account = GLAccount.objects.get(account_number=account_number)
                ActualExpense.objects.create(
                    gl_account=gl_account,
                    fiscal_year=fiscal_year,
                    month=month,
                    amount=amount
                )
                actuals_created += 1
                
                # Update forecasts for budget lines associated with this GL account
                budget_lines = gl_account.budget_lines.all()
                for budget_line in budget_lines:
                    BudgetService.recalculate_forecast(budget_line, fiscal_year, month)
                    
            except GLAccount.DoesNotExist:
                accounts_not_found.append(account_number)
        
        return {
            'actuals_created': actuals_created,
            'accounts_not_found': accounts_not_found
        }
    
    @staticmethod
    def generate_budget_report(fiscal_year, month=None):
        """Generate a report comparing budget, forecast, and actuals"""
        budget_entries = BudgetEntry.objects.filter(fiscal_year=fiscal_year)
        report_data = []
        
        for entry in budget_entries:
            budget_line = entry.budget_line
            budget_amount = entry.annual_amount
            
            # Get forecasts for this budget line
            if month:
                forecasts = ForecastEntry.objects.filter(
                    budget_entry=entry,
                    month=month
                )
                forecast_amount = sum(f.amount for f in forecasts) if forecasts else 0
            else:
                forecasts = ForecastEntry.objects.filter(budget_entry=entry)
                forecast_amount = sum(f.amount for f in forecasts) if forecasts else 0
            
            # Get actuals for this budget line
            gl_accounts = budget_line.gl_accounts.all()
            if month:
                actuals = ActualExpense.objects.filter(
                    gl_account__in=gl_accounts,
                    fiscal_year=fiscal_year,
                    month=month
                )
                actual_amount = sum(a.amount for a in actuals) if actuals else 0
            else:
                actuals = ActualExpense.objects.filter(
                    gl_account__in=gl_accounts,
                    fiscal_year=fiscal_year
                )
                actual_amount = sum(a.amount for a in actuals) if actuals else 0
            
            # Calculate variances
            budget_forecast_variance = forecast_amount - budget_amount
            budget_actual_variance = actual_amount - budget_amount
            
            # Variance percentages
            if budget_amount:
                budget_forecast_variance_pct = (budget_forecast_variance / budget_amount) * 100
                budget_actual_variance_pct = (budget_actual_variance / budget_amount) * 100
            else:
                budget_forecast_variance_pct = 0
                budget_actual_variance_pct = 0
            
            report_data.append({
                'budget_line': budget_line.name,
                'budget_amount': budget_amount,
                'forecast_amount': forecast_amount,
                'actual_amount': actual_amount,
                'budget_forecast_variance': budget_forecast_variance,
                'budget_forecast_variance_pct': budget_forecast_variance_pct,
                'budget_actual_variance': budget_actual_variance,
                'budget_actual_variance_pct': budget_actual_variance_pct,
            })
        
        return report_data 