from django import forms
from .models import FiscalYear, BudgetLine, BudgetEntry, ForecastEntry, GLAccount

class FiscalYearForm(forms.ModelForm):
    class Meta:
        model = FiscalYear
        fields = ['year', 'is_active']

class BudgetLineForm(forms.ModelForm):
    class Meta:
        model = BudgetLine
        fields = ['name', 'description', 'gl_accounts']
        widgets = {
            'gl_accounts': forms.CheckboxSelectMultiple(),
        }

class BudgetEntryForm(forms.ModelForm):
    class Meta:
        model = BudgetEntry
        fields = ['budget_line', 'annual_amount']
    
    def __init__(self, *args, **kwargs):
        fiscal_year = kwargs.pop('fiscal_year', None)
        super().__init__(*args, **kwargs)
        if fiscal_year:
            self.instance.fiscal_year = fiscal_year

class ForecastEntryForm(forms.ModelForm):
    class Meta:
        model = ForecastEntry
        fields = ['month', 'amount']

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='Select Excel File')
    fiscal_year = forms.ModelChoiceField(queryset=FiscalYear.objects.all())
    month = forms.ChoiceField(choices=ForecastEntry.MONTHS) 