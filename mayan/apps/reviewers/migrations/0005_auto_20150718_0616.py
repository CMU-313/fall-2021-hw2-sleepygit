from django.db import migrations

import colorful.fields


class Migration(migrations.Migration):
    dependencies = [
        ('reviewers', '0004_auto_20150717_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewer',
            name='color',
            field=colorful.fields.RGBColorField(verbose_name='Color'),
            preserve_default=True,
        ),
    ]
