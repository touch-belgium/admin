# Generated by Django 3.0.2 on 2020-01-13 13:37

from django.db import migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20200112_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='picture',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=500, null=True),
        ),
    ]