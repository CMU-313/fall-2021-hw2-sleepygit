from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('reviewers', '0002_reviewer_selection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewer',
            name='color',
        ),
    ]
