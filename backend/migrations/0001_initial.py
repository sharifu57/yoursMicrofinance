# Generated by Django 4.1.5 on 2023-05-03 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('identity', models.CharField(blank=True, max_length=10, null=True)),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('nida_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('nature_of_employment', models.IntegerField(blank=True, choices=[(1, 'Employed'), (2, 'Not Employed')], default=1, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='picture/%Y/%m/%d')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('interest_rate', models.DecimalField(blank=True, decimal_places=2, default=30, max_digits=10, null=True)),
                ('repayment_term', models.IntegerField(blank=True, choices=[(1, '1 Month'), (2, '3 Months'), (3, '6 Months'), (4, '1 Year')], default=1, null=True)),
                ('payment_frequency', models.IntegerField(blank=True, choices=[(1, 'Weekly'), (2, 'Bi-Weekly'), (3, 'Monthly')], default=1, null=True)),
                ('interest_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to='documents/%Y/%m/%d')),
                ('penalty_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('total_interest_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Active'), (2, 'Approved'), (3, 'Rejected'), (4, 'Waiting'), (5, 'Applying')], default=5, null=True)),
                ('borrower', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.borrower')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoanCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('category_name', models.CharField(blank=True, max_length=200, null=True)),
                ('interest', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('repayment_term_range', models.IntegerField(blank=True, choices=[(1, '1 Year')], default=1, null=True)),
                ('loan_amount_range_from', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('loan_amount_range_to', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('collateral', models.CharField(blank=True, max_length=300, null=True)),
                ('loan_purpose', models.CharField(blank=True, choices=[('education', 'Education Purpose'), ('small_business', 'Business Purpose'), ('Agriculture', 'Agriculture'), ('other', 'Other')], default=1, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoanPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('payment_number', models.CharField(blank=True, max_length=200, null=True)),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('principal_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_method', models.IntegerField(blank=True, null=True)),
                ('payment_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('late_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Paid'), (2, 'Pending'), (3, 'Late')], null=True)),
                ('loan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.loan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='loan',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.loancategory'),
        ),
        migrations.AddField(
            model_name='loan',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Approved'), (2, 'Rejected'), (3, 'Missing')], null=True)),
                ('loan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.loan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
