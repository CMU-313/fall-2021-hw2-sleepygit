from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('reviewers', '0006_documentreviewer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviewer',
            options={
                'ordering': ('label',), 'verbose_name': 'Reviewer',
                'verbose_name_plural': 'Reviewers'
            },
        ),
    ]
