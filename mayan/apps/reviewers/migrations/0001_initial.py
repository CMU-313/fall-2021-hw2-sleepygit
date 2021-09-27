from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'label', models.CharField(
                        unique=True, max_length=128, verbose_name='Label',
                        db_index=True
                    )
                ),
                (
                    'color', models.CharField(
                        max_length=3, verbose_name='Color', choices=[
                            ('blu', 'Blue'), ('cya', 'Cyan'), ('crl', 'Coral'),
                            ('gry', 'Green-Yellow'), ('kki', 'Khaki'),
                            ('lig', 'LightGrey'), ('mag', 'Magenta'),
                            ('red', 'Red'), ('org', 'Orange'),
                            ('yel', 'Yellow')
                        ]
                    )
                ),
                (
                    'documents', models.ManyToManyField(
                        related_name='reviewers', verbose_name='Documents',
                        to='documents.Document'
                    )
                ),
            ],
            options={
                'verbose_name': 'Reviewer',
                'verbose_name_plural': 'Reviewers',
            },
            bases=(models.Model,),
        ),
    ]
