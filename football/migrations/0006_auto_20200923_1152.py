# Generated by Django 3.1 on 2020-09-23 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0005_auto_20200923_1012'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ('city',)},
        ),
        migrations.RenameField(
            model_name='team',
            old_name='name',
            new_name='city',
        ),
    ]