# Generated by Django 3.2.13 on 2023-04-20 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20230419_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='user_type',
            field=models.CharField(choices=[('Administrator', 'Administrator'), ('Employee', 'Employee')], default='Employee', max_length=20),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='passphrase',
            field=models.TextField(),
        ),
    ]