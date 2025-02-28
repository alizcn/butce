from django.db import models
from django.utils import timezone

class FiscalYear(models.Model):
    year = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Fiscal Year {self.year}"

class GLAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    account_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.account_number} - {self.account_name}"

class BudgetLine(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    gl_accounts = models.ManyToManyField(GLAccount, related_name='budget_lines')
    
    def __str__(self):
        return self.name

class BudgetEntry(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    budget_line = models.ForeignKey(BudgetLine, on_delete=models.CASCADE)
    annual_amount = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('fiscal_year', 'budget_line')
    
    def __str__(self):
        return f"{self.budget_line} - {self.fiscal_year}"

class ForecastEntry(models.Model):
    MONTHS = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    budget_entry = models.ForeignKey(BudgetEntry, on_delete=models.CASCADE, related_name='forecasts')
    month = models.IntegerField(choices=MONTHS)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('budget_entry', 'month')
    
    def __str__(self):
        return f"{self.budget_entry.budget_line} - {self.get_month_display()} {self.budget_entry.fiscal_year.year}"

class ActualExpense(models.Model):
    gl_account = models.ForeignKey(GLAccount, on_delete=models.CASCADE)
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    month = models.IntegerField(choices=ForecastEntry.MONTHS)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    import_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('gl_account', 'fiscal_year', 'month')
    
    def __str__(self):
        return f"{self.gl_account} - {self.get_month_display()} {self.fiscal_year.year}"
