# Generated by Django 4.0.4 on 2022-08-03 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_reimbursementrequest_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reimbursementrequest',
            name='receipt',
            field=models.ImageField(upload_to='receipts/'),
        ),
    ]
