# Generated by Django 5.1.5 on 2025-02-04 18:29

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_orderitem_quantity_alter_orderitem_unit_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Categorie', 'verbose_name_plural': 'Categorii'},
        ),
        migrations.AlterModelOptions(
            name='county',
            options={'ordering': ['name'], 'verbose_name': 'Județ', 'verbose_name_plural': 'Județe'},
        ),
        migrations.AlterModelOptions(
            name='lake',
            options={'ordering': ['name'], 'verbose_name': 'Baltă', 'verbose_name_plural': 'Bălți'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name': 'Comandă', 'verbose_name_plural': 'Comenzi'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Produs comandat', 'verbose_name_plural': 'Produse comandate'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-created_at'], 'verbose_name': 'Plată', 'verbose_name_plural': 'Plăți'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at'], 'verbose_name': 'Produs', 'verbose_name_plural': 'Produse'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profil', 'verbose_name_plural': 'Profiluri'},
        ),
        migrations.AlterModelOptions(
            name='sitesettings',
            options={'verbose_name': 'Setări site', 'verbose_name_plural': 'Setări site'},
        ),
        migrations.AlterModelOptions(
            name='testimonial',
            options={'ordering': ['-created_at'], 'verbose_name': 'Testimonial', 'verbose_name_plural': 'Testimoniale'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-created_at'], 'verbose_name': 'Video', 'verbose_name_plural': 'Videouri'},
        ),
        migrations.RemoveField(
            model_name='county',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='county',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='lake',
            name='address',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email_verification_token',
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='rating',
        ),
        migrations.AddField(
            model_name='lake',
            name='contact_info',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lake',
            name='facilities',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lake',
            name='fish_species',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='lake',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lake',
            name='rules',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='company_name',
            field=models.CharField(default='Răsfățul Pescarului SRL', max_length=100),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='facebook_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='instagram_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='youtube_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='role',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='county',
            name='region',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='lake',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='lake',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='lake',
            name='location',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='lake',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.county'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='full_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('card', 'Card'), ('bank_transfer', 'Transfer bancar')], max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('card', 'Card'), ('bank_transfer', 'Transfer bancar')], max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'În așteptare'), ('completed', 'Finalizată'), ('failed', 'Eșuată')], max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='company_address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='company_email',
            field=models.EmailField(default='contact@rasfatulpescarului.ro', max_length=254),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='company_phone',
            field=models.CharField(default='+40 123 456 789', max_length=20),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='contact_email',
            field=models.EmailField(default='contact@rasfatulpescarului.ro', max_length=254),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-created_at'], name='main_order_created_49eb22_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status'], name='main_order_status_4d3738_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user', '-created_at'], name='main_order_user_id_3f17b3_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['order', '-created_at'], name='main_paymen_order_i_29ae0d_idx'),
        ),
    ]
