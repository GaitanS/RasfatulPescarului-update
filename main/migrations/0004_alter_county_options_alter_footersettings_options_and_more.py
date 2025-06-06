# Generated by Django 5.1.6 on 2025-06-05 18:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_footersettings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='county',
            options={'ordering': ['name'], 'verbose_name': 'Județ', 'verbose_name_plural': 'Județe'},
        ),
        migrations.AlterModelOptions(
            name='footersettings',
            options={'verbose_name': 'Setări Footer', 'verbose_name_plural': 'Setări Footer'},
        ),
        migrations.AlterModelOptions(
            name='herosection',
            options={'verbose_name': 'Secțiune Hero', 'verbose_name_plural': 'Secțiune Hero'},
        ),
        migrations.AlterModelOptions(
            name='lake',
            options={'ordering': ['name'], 'verbose_name': 'Lac de pescuit', 'verbose_name_plural': 'Lacuri de pescuit'},
        ),
        migrations.AlterModelOptions(
            name='sitesettings',
            options={'verbose_name': 'Setări Site', 'verbose_name_plural': 'Setări Site'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-created_at'], 'verbose_name': 'Videoclip', 'verbose_name_plural': 'Videoclipuri'},
        ),
        migrations.AlterField(
            model_name='county',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data creării'),
        ),
        migrations.AlterField(
            model_name='county',
            name='name',
            field=models.CharField(help_text='Numele complet al județului (ex: Argeș, Brașov, Cluj)', max_length=100, verbose_name='Nume județ'),
        ),
        migrations.AlterField(
            model_name='county',
            name='region',
            field=models.CharField(choices=[('MOLDOVA', 'Moldova'), ('MUNTENIA', 'Muntenia'), ('OLTENIA', 'Oltenia'), ('BANAT', 'Banat'), ('CRISANA', 'Crișana'), ('MARAMURES', 'Maramureș'), ('TRANSILVANIA', 'Transilvania'), ('DOBROGEA', 'Dobrogea'), ('BUCURESTI', 'București')], help_text='Regiunea istorică din care face parte județul', max_length=50, verbose_name='Regiune'),
        ),
        migrations.AlterField(
            model_name='county',
            name='slug',
            field=models.SlugField(help_text='Se generează automat din nume. Folosit pentru URL-uri (ex: arges, brasov)', max_length=100, unique=True, verbose_name='URL slug'),
        ),
        migrations.AlterField(
            model_name='county',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Data actualizării'),
        ),
        migrations.AlterField(
            model_name='footersettings',
            name='address',
            field=models.TextField(default='Strada Exemplu, Nr. 123, București', help_text='Adresa fizică completă care apare în footer', verbose_name='Adresa completă'),
        ),
        migrations.AlterField(
            model_name='footersettings',
            name='contact_info',
            field=models.CharField(default='Contact', help_text='Titlul secțiunii de contact din footer', max_length=200, verbose_name='Informații contact'),
        ),
        migrations.AlterField(
            model_name='footersettings',
            name='email',
            field=models.EmailField(default='contact@rasfatulpescarului.ro', help_text='Adresa de email care apare în footer', max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='footersettings',
            name='phone',
            field=models.CharField(default='+40 123 456 789', help_text='Numărul de telefon cu prefixul țării (ex: +40 123 456 789)', max_length=20, verbose_name='Telefon'),
        ),
        migrations.AlterField(
            model_name='footersettings',
            name='working_hours',
            field=models.CharField(default='Luni - Vineri: 09:00 - 18:00', help_text='Programul de lucru (ex: Luni - Vineri: 09:00 - 18:00)', max_length=100, verbose_name='Program de lucru'),
        ),
        migrations.AlterField(
            model_name='herosection',
            name='facebook_url',
            field=models.URLField(default='https://www.facebook.com/rasfatulpescarului', help_text='URL-ul complet către pagina de Facebook', verbose_name='Link Facebook'),
        ),
        migrations.AlterField(
            model_name='herosection',
            name='main_button_text',
            field=models.CharField(default='Alătură-te grupului', help_text='Textul care apare pe butonul principal din secțiunea hero (ex: Alătură-te grupului)', max_length=100, verbose_name='Textul butonului principal'),
        ),
        migrations.AlterField(
            model_name='herosection',
            name='main_button_url',
            field=models.URLField(default='https://www.facebook.com/rasfatulpescarului', help_text='URL-ul către care duce butonul principal (ex: pagina de Facebook)', verbose_name='Link buton principal'),
        ),
        migrations.AlterField(
            model_name='herosection',
            name='tiktok_url',
            field=models.URLField(default='https://www.tiktok.com/@rasfatulpescarului', help_text='URL-ul complet către contul de TikTok', verbose_name='Link TikTok'),
        ),
        migrations.AlterField(
            model_name='herosection',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Data actualizării'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='address',
            field=models.CharField(help_text='Adresa completă a lacului (ex: Comuna X, Județul Y)', max_length=255, verbose_name='Adresa'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='county',
            field=models.ForeignKey(help_text='Județul în care se află lacul', on_delete=django.db.models.deletion.CASCADE, related_name='lakes', to='main.county', verbose_name='Județul'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data creării'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='description',
            field=models.TextField(blank=True, help_text='Descrierea detaliată a lacului, facilităților și condițiilor de pescuit', verbose_name='Descriere'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='facilities',
            field=models.CharField(help_text='Facilitățile disponibile, separate prin spații (ex: parcare cazare restaurant toalete)', max_length=500, verbose_name='Facilități'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='fish_types',
            field=models.CharField(help_text='Tipurile de pești disponibile, separate prin virgulă (ex: Crap, Șalău, Știucă, Caras)', max_length=500, verbose_name='Tipuri de pești'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='image',
            field=models.ImageField(blank=True, help_text='Imaginea principală a lacului (format recomandat: JPG, PNG, max 2MB)', null=True, upload_to='lakes/', verbose_name='Imagine'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Bifează pentru a afișa lacul pe site. Debifează pentru a-l ascunde temporar', verbose_name='Activ'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='latitude',
            field=models.DecimalField(decimal_places=6, help_text='Coordonata latitudine (ex: 44.123456). Folosește Google Maps pentru a găsi coordonatele', max_digits=9, verbose_name='Latitudine'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='longitude',
            field=models.DecimalField(decimal_places=6, help_text='Coordonata longitudine (ex: 26.123456). Folosește Google Maps pentru a găsi coordonatele', max_digits=9, verbose_name='Longitudine'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='name',
            field=models.CharField(help_text='Numele complet al lacului sau bălții de pescuit', max_length=200, verbose_name='Numele lacului'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='price_per_day',
            field=models.DecimalField(decimal_places=2, help_text='Prețul pentru o zi de pescuit în lei românești (ex: 50.00)', max_digits=10, verbose_name='Preț pe zi (RON)'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Data actualizării'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='about_text',
            field=models.TextField(default='Despre noi', help_text='Descrierea scurtă a companiei care apare în footer', verbose_name='Text despre noi'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='address',
            field=models.TextField(default='România', help_text='Adresa completă a companiei', verbose_name='Adresa'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='contact_email',
            field=models.EmailField(default='contact@rasfatulpescarului.ro', help_text='Adresa de email principală pentru contact (ex: contact@site.ro)', max_length=254, verbose_name='Email de contact'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='facebook_url',
            field=models.URLField(blank=True, help_text='URL-ul complet către pagina de Facebook (ex: https://facebook.com/pagina)', verbose_name='Link Facebook'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='instagram_url',
            field=models.URLField(blank=True, help_text='URL-ul complet către pagina de Instagram', verbose_name='Link Instagram'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='phone',
            field=models.CharField(default='0700000000', help_text='Numărul de telefon pentru contact (ex: 0700 123 456)', max_length=20, verbose_name='Număr de telefon'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='site_name',
            field=models.CharField(default='Răsfățul Pescarului', help_text='Numele principal al site-ului care apare în titlu și logo', max_length=100, verbose_name='Numele site-ului'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='youtube_url',
            field=models.URLField(blank=True, help_text='URL-ul complet către canalul de YouTube', verbose_name='Link YouTube'),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data creării'),
        ),
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(blank=True, help_text='Descrierea detaliată a videoclipului și conținutului acestuia', verbose_name='Descriere'),
        ),
        migrations.AlterField(
            model_name='video',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Bifează pentru a afișa videoclipul pe site', verbose_name='Activ'),
        ),
        migrations.AlterField(
            model_name='video',
            name='is_featured',
            field=models.BooleanField(default=False, help_text='Bifează pentru a afișa videoclipul în secțiunea de recomandări', verbose_name='Video recomandat'),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(blank=True, help_text='Imaginea care apare înainte de redarea videoclipului (opțional, se poate genera automat)', null=True, upload_to='videos/thumbnails/', verbose_name='Imagine de previzualizare'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(help_text='Titlul descriptiv al videoclipului (ex: Pescuit la crap pe lacul X)', max_length=200, verbose_name='Titlul videoclipului'),
        ),
        migrations.AlterField(
            model_name='video',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Data actualizării'),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(help_text='URL-ul complet către videoclip (YouTube, Vimeo, etc.) - ex: https://youtube.com/watch?v=...', verbose_name='Link video'),
        ),
    ]
