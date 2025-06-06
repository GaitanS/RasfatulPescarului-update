# Generated by Django 5.1.6 on 2025-06-05 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_lake_rules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lake',
            name='latitude',
            field=models.DecimalField(decimal_places=15, help_text='Coordonata latitudine cu precizie mare (ex: 45.39189813235069). Folosește Google Maps pentru a găsi coordonatele', max_digits=18, verbose_name='Latitudine'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='longitude',
            field=models.DecimalField(decimal_places=15, help_text='Coordonata longitudine cu precizie mare (ex: 24.62707585690222). Folosește Google Maps pentru a găsi coordonatele', max_digits=18, verbose_name='Longitudine'),
        ),
    ]
