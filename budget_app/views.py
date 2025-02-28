from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q

from .models import FiscalYear, BudgetLine, BudgetEntry, ForecastEntry, GLAccount, ActualExpense
from .forms import FiscalYearForm, BudgetLineForm, BudgetEntryForm, ForecastEntryForm, ExcelImportForm
from .services import BudgetService

class FiscalYearListView(ListView):
    model = FiscalYear
    template_name = 'budget_app/fiscal_year_list.html'
    context_object_name = 'fiscal_years'

class FiscalYearCreateView(CreateView):
    model = FiscalYear
    form_class = FiscalYearForm
    template_name = 'budget_app/fiscal_year_form.html'
    success_url = reverse_lazy('budget_app:fiscal_year_list')

    def form_valid(self, form):
        # If this fiscal year is set as active, deactivate all others
        if form.cleaned_data.get('is_active'):
            FiscalYear.objects.filter(is_active=True).update(is_active=False)
        response = super().form_valid(form)
        messages.success(self.request, f"Fiscal Year {form.instance.year} created successfully.")
        return response

class FiscalYearUpdateView(UpdateView):
    model = FiscalYear
    form_class = FiscalYearForm
    template_name = 'budget_app/fiscal_year_form.html'
    success_url = reverse_lazy('budget_app:fiscal_year_list')

    def form_valid(self, form):
        # If this fiscal year is set as active, deactivate all others
        if form.cleaned_data.get('is_active'):
            FiscalYear.objects.filter(~Q(id=self.object.id), is_active=True).update(is_active=False)
        response = super().form_valid(form)
        messages.success(self.request, f"Fiscal Year {form.instance.year} updated successfully.")
        return response

class DashboardView(View):
    def get(self, request):
        try:
            active_year = FiscalYear.objects.get(is_active=True)
        except FiscalYear.DoesNotExist:
            active_year = None
        
        context = {
            'active_year': active_year,
            'budget_lines_count': BudgetLine.objects.count(),
            'gl_accounts_count': GLAccount.objects.count(),
        }
        
        if active_year:
            context.update({
                'budget_entries_count': BudgetEntry.objects.filter(fiscal_year=active_year).count(),
                'forecast_months': ForecastEntry.MONTHS,
            })
        
        return render(request, 'budget_app/dashboard.html', context)

class BudgetEntryView(View):
    def get(self, request):
        try:
            active_year = FiscalYear.objects.get(is_active=True)
        except FiscalYear.DoesNotExist:
            messages.error(request, "No active fiscal year found. Please create one first.")
            return redirect('budget_app:fiscal_year_create')
        
        budget_entries = BudgetEntry.objects.filter(fiscal_year=active_year)
        form = BudgetEntryForm(fiscal_year=active_year)
        
        return render(request, 'budget_app/budget_entry.html', {
            'active_year': active_year,
            'budget_entries': budget_entries,
            'form': form,
        })
    
    def post(self, request):
        try:
            active_year = FiscalYear.objects.get(is_active=True)
        except FiscalYear.DoesNotExist:
            messages.error(request, "No active fiscal year found. Please create one first.")
            return redirect('budget_app:fiscal_year_create')
        
        form = BudgetEntryForm(request.POST, fiscal_year=active_year)
        
        if form.is_valid():
            budget_entry = form.save()
            # Initialize forecasts with equal distribution
            BudgetService.initialize_forecasts(budget_entry)
            messages.success(request, "Budget entry created successfully.")
            return redirect('budget_entry')
        
        budget_entries = BudgetEntry.objects.filter(fiscal_year=active_year)
        return render(request, 'budget_app/budget_entry.html', {
            'active_year': active_year,
            'budget_entries': budget_entries,
            'form': form,
        })

class ForecastUpdateView(View):
    def get(self, request):
        try:
            active_year = FiscalYear.objects.get(is_active=True)
        except FiscalYear.DoesNotExist:
            messages.error(request, "No active fiscal year found. Please create one first.")
            return redirect('budget_app:fiscal_year_create')
        
        month = request.GET.get('month', timezone.now().month)
        month = int(month)
        
        budget_entries = BudgetEntry.objects.filter(fiscal_year=active_year)
        forecasts = []
        
        for entry in budget_entries:
            try:
                forecast = ForecastEntry.objects.get(budget_entry=entry, month=month)
            except ForecastEntry.DoesNotExist:
                # Create forecast if it doesn't exist
                forecast = ForecastEntry.objects.create(
                    budget_entry=entry,
                    month=month,
                    amount=entry.annual_amount / 12
                )
            
            forecasts.append({
                'budget_line': entry.budget_line.name,
                'budget_amount': entry.annual_amount,
                'forecast': forecast,
                'form': ForecastEntryForm(instance=forecast)
            })
        
        return render(request, 'budget_app/forecast_update.html', {
            'active_year': active_year,
            'current_month': month,
            'months': ForecastEntry.MONTHS,
            'forecasts': forecasts,
        })
    
    def post(self, request):
        try:
            active_year = FiscalYear.objects.get(is_active=True)
        except FiscalYear.DoesNotExist:
            messages.error(request, "No active fiscal year found. Please create one first.")
            return redirect('budget_app:fiscal_year_create')
        
        month = int(request.GET.get('month', timezone.now().month))
        forecast_id = request.POST.get('forecast_id')
        
        if forecast_id:
            forecast = get_object_or_404(ForecastEntry, id=forecast_id)
            form = ForecastEntryForm(request.POST, instance=forecast)
            
            if form.is_valid():
                form.save()
                messages.success(request, "Forecast updated successfully.")
        
        return redirect(f'{reverse_lazy("budget_app:forecast_update")}?month={month}')

class ActualImportView(View):
    def get(self, request):
        form = ExcelImportForm()
        
        return render(request, 'budget_app/actual_import.html', {
            'form': form,
        })
    
    def post(self, request):
        form = ExcelImportForm(request.POST, request.FILES)
        
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            fiscal_year = form.cleaned_data['fiscal_year']
            month = int(form.cleaned_data['month'])
            
            try:
                result = BudgetService.import_actuals_from_excel(excel_file, fiscal_year, month)
                messages.success(
                    request, 
                    f"Successfully imported {result['actuals_created']} actual expense entries."
                )
                
                if result['accounts_not_found']:
                    messages.warning(
                        request,
                        f"Could not find GL accounts: {', '.join(result['accounts_not_found'])}"
                    )
                
                return redirect('budget_app:report_view')
            
            except Exception as e:
                messages.error(request, f"Error importing data: {str(e)}")
        
        return render(request, 'budget_app/actual_import.html', {
            'form': form,
        })

class ReportView(View):
    def get(self, request):
        try:
            active_year = FiscalYear.objects.get(is_active=True)
        except FiscalYear.DoesNotExist:
            messages.error(request, "No active fiscal year found. Please create one first.")
            return redirect('budget_app:fiscal_year_create')
        
        month = request.GET.get('month')
        month = int(month) if month else None
        
        if month:
            report_data = BudgetService.generate_budget_report(active_year, month)
            month_name = dict(ForecastEntry.MONTHS).get(month)
            report_title = f"Budget Report for {month_name} {active_year.year}"
        else:
            report_data = BudgetService.generate_budget_report(active_year)
            report_title = f"Annual Budget Report for {active_year.year}"
        
        return render(request, 'budget_app/reports.html', {
            'active_year': active_year,
            'report_title': report_title,
            'report_data': report_data,
            'current_month': month,
            'months': ForecastEntry.MONTHS,
        })
