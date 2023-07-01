from django.db import models


class ProposalConfig(models.Model):
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50)
    required = models.BooleanField(default=False)
    max_length = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Proposal(models.Model):
    STATUS_CHOICES = [
        ('Aprovada', 'Aprovada'),
        ('Negada', 'Negada'),
        ('Em análise', 'Em análise'),
    ]
    config = models.ManyToManyField(ProposalConfig, blank=True, null=True)
    name = models.CharField(max_length=100)
    document = models.CharField(max_length=50, default="999999")
    birth_date = models.DateField()
    proposal_value = models.DecimalField(max_digits=60, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default="Em análise")
    human_analysis = models.BooleanField(default=False)

    def __str__(self):
        return f"Proposta #{self.pk}"


class ProposalData(models.Model):
    proposal = models.ForeignKey(
        Proposal, on_delete=models.CASCADE, null=True, blank=True
    )
    field = models.ForeignKey(
        ProposalConfig, on_delete=models.CASCADE, null=True, blank=True
    )
    value = models.CharField(
        max_length=200, null=True, blank=True
    )

    def __str__(self):
        return f"DadoProposta #{self.pk}"
