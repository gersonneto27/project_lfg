# Generated by Django 3.2.19 on 2023-07-01 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprestimo', '0003_proposal_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='config',
            field=models.ManyToManyField(blank=True, null=True, to='emprestimo.ProposalConfig'),
        ),
    ]
