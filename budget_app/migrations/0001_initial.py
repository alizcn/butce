# Generated by Django 5.0.2 on 2025-02-28 20:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FiscalYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GLAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=20, unique=True)),
                ('account_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annual_amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('budget_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_app.budgetline')),
                ('fiscal_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_app.fiscalyear')),
            ],
            options={
                'unique_together': {('fiscal_year', 'budget_line')},
            },
        ),
        migrations.AddField(
            model_name='budgetline',
            name='gl_accounts',
            field=models.ManyToManyField(related_name='budget_lines', to='budget_app.glaccount'),
        ),
        migrations.CreateModel(
            name='ForecastEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('budget_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecasts', to='budget_app.budgetentry')),
            ],
            options={
                'unique_together': {('budget_entry', 'month')},
            },
        ),
        migrations.CreateModel(
            name='ActualExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('import_date', models.DateTimeField(auto_now_add=True)),
                ('fiscal_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_app.fiscalyear')),
                ('gl_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget_app.glaccount')),
            ],
            options={
                'unique_together': {('gl_account', 'fiscal_year', 'month')},
            },
        ),
    ]
