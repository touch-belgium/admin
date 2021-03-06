# Generated by Django 3.1.1 on 2020-09-19 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20200919_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbmember',
            name='media_consent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registration',
            name='dob',
            field=models.DateField(verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='tbmember',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='Date of birth'),
        ),
    ]
