from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0023_remove_lake_county_remove_order_county_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('address', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('fish_types', models.CharField(max_length=500)),
                ('facilities', models.CharField(max_length=500)),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='lakes/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('county', models.ForeignKey(on_delete=models.deletion.CASCADE, to='main.county')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]