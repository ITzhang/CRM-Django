# Generated by Django 2.1.3 on 2018-11-20 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_customer_deal_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='deal_date',
            field=models.DateField(null=True),
        ),
    ]
