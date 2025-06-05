from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import Lake


class Command(BaseCommand):
    help = 'Populate slugs for existing lakes'

    def handle(self, *args, **options):
        lakes = Lake.objects.filter(slug__isnull=True) | Lake.objects.filter(slug='')
        
        for lake in lakes:
            base_slug = slugify(lake.name)
            slug = base_slug
            counter = 1
            
            # Ensure unique slug
            while Lake.objects.filter(slug=slug).exclude(id=lake.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            lake.slug = slug
            lake.save()
            
            self.stdout.write(f'Updated slug for "{lake.name}": {slug}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated slugs for {lakes.count()} lakes')
        )
