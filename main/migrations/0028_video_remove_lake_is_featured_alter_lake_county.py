# Generated by Django 5.0.1 on 2025-02-23 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_merge_20250223_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='videos/thumbnails/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
                'ordering': ['-created_at'],
            },
        ),
        migrations.RemoveField(
            model_name='lake',
            name='is_featured',
        ),
        migrations.AlterField(
            model_name='lake',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lakes', to='main.county'),
        ),
    ]
