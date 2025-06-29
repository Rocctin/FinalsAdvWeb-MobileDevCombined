import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from website.models import Title

class Command(BaseCommand):
    help = 'Loads data from netflix_titles.csv into the Title model'

    def handle(self, *args, **options):
        # Path to the CSV file
        csv_file_path = 'data/netflix_titles.csv'
        
        self.stdout.write(self.style.SUCCESS('Starting to load data...'))

        # Use update_or_create to avoid creating duplicate entries if the command is run multiple times.
        # It tries to find an object with the given 'show_id'. If it finds one, it updates it.
        # If not, it creates a new one.
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # The 'date_added' field needs special handling to convert it from a string to a Date object.
                date_added_obj = None
                date_str = row.get('date_added', '').strip()
                if date_str:
                    try:
                        date_added_obj = datetime.strptime(date_str, '%B %d, %Y').date()
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"Could not parse date '{date_str}' for show_id {row['show_id']}. Skipping date."))

                Title.objects.update_or_create(
                    show_id=row['show_id'],
                    defaults={
                        'type': row['type'],
                        'title': row['title'],
                        'director': row['director'] if row['director'] else None,
                        'cast': row['cast'] if row['cast'] else None,
                        'country': row['country'] if row['country'] else None,
                        'date_added': date_added_obj,
                        'release_year': int(row['release_year']),
                        'rating': row['rating'] if row['rating'] else None,
                        'duration': row['duration'] if row['duration'] else None,
                        'listed_in': row['listed_in'],
                        'description': row['description'],
                    }
                )

        self.stdout.write(self.style.SUCCESS('Data loading complete!'))