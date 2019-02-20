# Generated by Django 2.1.5 on 2019-02-13 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.IntegerField(choices=[(0, 'Public'), (1, 'Only certain friends'), (2, 'Only friends'), (3, 'Friend of a friend'), (4, 'Server wide'), (5, 'Only me')], default=0),
        ),
    ]