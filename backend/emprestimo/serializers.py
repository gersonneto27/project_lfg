from emprestimo.tasks import change_proposal_status
from rest_framework import serializers
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from .models import Proposal, ProposalConfig, ProposalData


class ProposalConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalConfig
        fields = '__all__'

    def create(self, validated_data):
        proposal_config = ProposalConfig.objects.create(**validated_data)

        return proposal_config


class ProposalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalData
        fields = '__all__'


@receiver(post_save, sender=Proposal)
def proposal_created(sender, instance, created, **kwargs):
    if created:
        change_proposal_status.delay(instance.id)


@transaction.atomic
class ProposalCreateSerializer(serializers.ModelSerializer):
    dados_proposta = ProposalDataSerializer(many=True, required=False)

    class Meta:
        model = Proposal
        fields = [
            'name',
            'birth_date',
            'proposal_value',
            'document',
            'status',
            'human_analysis',
            'dados_proposta'
        ]

    def create(self, validated_data):
        dados_proposta_data = validated_data.pop('dados_proposta', None)
        proposal = Proposal.objects.create(**validated_data)

        if dados_proposta_data:
            for dado_data in dados_proposta_data:
                field_data = dado_data.pop('field')
                field = ProposalConfig.objects.get(id=field_data.id)
                ProposalData.objects.create(
                    proposal=proposal,
                    field=field,
                    **dado_data
                )

        change_proposal_status.delay(proposal.id)
        return proposal

    def update(self, instance, validated_data):
        dados_proposta_data = validated_data.pop('dados_proposta', [])
        dados_proposta = instance.dados_proposta.all()
        dados_proposta = list(dados_proposta)

        instance.name = validated_data.get(
            'name',
            instance.name
        )
        instance.birth_date = validated_data.get(
            'birth_date',
            instance.birth_date
        )
        instance.proposal_value = validated_data.get(
            'proposal_value',
            instance.proposal_value
        )
        instance.status = validated_data.get(
            'status',
            instance.status
        )
        instance.human_analysis = validated_data.get(
            'human_analysis',
            instance.human_analysis
        )
        instance.save()

        for dado_proposta_data in dados_proposta_data:
            if len(dados_proposta) > 0:
                dado_proposta = dados_proposta.pop(0)
                dado_proposta.proposal = instance
                dado_proposta.some_field = dado_proposta_data.get(
                    'some_field',
                    dado_proposta.some_field
                )
                dado_proposta.save()
            else:
                ProposalData.objects.create(
                    proposal=instance, **dado_proposta_data
                )

        return instance


class ProposalSerializer(serializers.ModelSerializer):
    dados_proposta = serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        fields = [
            'name',
            'birth_date',
            'proposal_value',
            'status',
            'document',
            'human_analysis',
            'dados_proposta'
        ]

    def get_dados_proposta(self, obj):
        dados_proposta = obj.proposaldata_set.all()

        if dados_proposta:
            serialized_dados_proposta = ProposalDataSerializer(
                dados_proposta, many=True
            ).data
            return serialized_dados_proposta

        return []

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if 'dados_proposta' not in representation:
            representation['dados_proposta'] = []

        return representation


class UpdateProposalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ['status']
