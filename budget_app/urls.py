from django.urls import path
from . import views

app_name = 'budget_app'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('fiscal-years/', views.FiscalYearListView.as_view(), name='fiscal_year_list'),
    path('fiscal-years/create/', views.FiscalYearCreateView.as_view(), name='fiscal_year_create'),
    path('fiscal-years/<int:pk>/update/', views.FiscalYearUpdateView.as_view(), name='fiscal_year_update'),
    path('budget/', views.BudgetEntryView.as_view(), name='budget_entry'),
    path('forecast/', views.ForecastUpdateView.as_view(), name='forecast_update'),
    path('actual/import/', views.ActualImportView.as_view(), name='actual_import'),
    path('reports/', views.ReportView.as_view(), name='report_view'),
] 