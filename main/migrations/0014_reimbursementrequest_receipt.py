# Generated by Django 4.0.4 on 2022-08-03 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_reimbursementrequest_declined'),
    ]

    operations = [
        migrations.AddField(
            model_name='reimbursementrequest',
            name='receipt',
            field=models.ImageField(default=False, upload_to=''),
        ),
    ]