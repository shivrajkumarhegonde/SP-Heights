# Generated by Django 5.1.5 on 2025-02-19 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0007_remove_member_user_member_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
