# Generated by Django 2.1.5 on 2019-03-24 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='url',
            new_name='host',
        ),
        migrations.RemoveField(
            model_name='nodesetting',
            name='node_limit',
        ),
        migrations.AddField(
            model_name='nodesetting',
            name='host',
            field=models.CharField(default='a', max_length=500),
            preserve_default=False,
        ),
    ]
