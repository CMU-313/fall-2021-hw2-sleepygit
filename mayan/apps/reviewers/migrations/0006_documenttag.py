from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('reviewers', '0005_auto_20150718_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentReviewer',
            fields=[
            ],
            options={
                'verbose_name': 'Document reviewer',
                'proxy': True,
                'verbose_name_plural': 'Document reviewers',
            },
            bases=('reviewers.reviewer',),
        ),
    ]
