# Generated by Django 3.2 on 2022-03-01 11:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0006_auto_20220225_1921'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='to',
            new_name='recipients',
        ),
        migrations.RemoveField(
            model_name='email',
            name='user',
        ),
        migrations.AlterField(
            model_name='email',
            name='bcc',
            field=models.ManyToManyField(blank=True, null=True, related_name='bcc', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='email',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='categories', to='mail.Category'),
        ),
        migrations.AlterField(
            model_name='email',
            name='cc',
            field=models.ManyToManyField(blank=True, null=True, related_name='cc', to=settings.AUTH_USER_MODEL),
        ),
    ]