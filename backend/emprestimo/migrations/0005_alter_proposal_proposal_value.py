# Generated by Django 3.2.19 on 2023-07-01 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprestimo', '0004_alter_proposal_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='proposal_value',
            field=models.DecimalField(decimal_places=2, max_digits=60),
        ),
    ]
