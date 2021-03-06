# Generated by Django 3.2 on 2022-03-29 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0008_alter_email_body'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='reply_to',
            new_name='reply',
        ),
        migrations.AddField(
            model_name='email',
            name='is_filter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='filter',
            name='filter_both',
            field=models.BooleanField(default=False),
        ),
    ]
