from django.db import migrations, models

import colorful.fields


class Migration(migrations.Migration):
    dependencies = [
        ('reviewers', '0007_auto_20170118_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewer',
            name='color',
            field=colorful.fields.RGBColorField(
                help_text='The RGB color values for the reviewer.',
                verbose_name='Color'
            ),
        ),
        migrations.AlterField(
            model_name='reviewer',
            name='label',
            field=models.CharField(
                db_index=True, help_text='A short text used as the reviewer name.',
                max_length=128, unique=True, verbose_name='Label'
            ),
        ),
    ]
