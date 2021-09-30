from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('reviewers', '0003_remove_reviewer_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewer',
            old_name='selection',
            new_name='color',
        ),
    ]
