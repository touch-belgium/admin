# Generated by Django 3.1.2 on 2020-10-14 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20201014_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected'), ('M', 'Manual review required')], default='P', max_length=1),
        ),
    ]
