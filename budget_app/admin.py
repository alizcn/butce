from django.contrib import admin
from .models import FiscalYear, GLAccount, BudgetLine, BudgetEntry, ForecastEntry, ActualExpense

@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('year',)

@admin.register(GLAccount)
class GLAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'account_name')
    search_fields = ('account_number', 'account_name')

@admin.register(BudgetLine)
class BudgetLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('gl_accounts',)

@admin.register(BudgetEntry)
class BudgetEntryAdmin(admin.ModelAdmin):
    list_display = ('budget_line', 'fiscal_year', 'annual_amount', 'created_at', 'updated_at')
    list_filter = ('fiscal_year',)
    search_fields = ('budget_line__name',)

@admin.register(ForecastEntry)
class ForecastEntryAdmin(admin.ModelAdmin):
    list_display = ('budget_entry', 'month', 'amount', 'updated_at')
    list_filter = ('month', 'budget_entry__fiscal_year')
    search_fields = ('budget_entry__budget_line__name',)

@admin.register(ActualExpense)
class ActualExpenseAdmin(admin.ModelAdmin):
    list_display = ('gl_account', 'fiscal_year', 'month', 'amount', 'import_date')
    list_filter = ('fiscal_year', 'month')
    search_fields = ('gl_account__account_number', 'gl_account__account_name')
