from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import Proposal, ProposalConfig, ProposalData
from .serializers import (
                            ProposalConfigSerializer,
                            ProposalCreateSerializer,
                            ProposalDataSerializer,
                            ProposalSerializer,
                            UpdateProposalStatusSerializer
                        )


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalCreateAPIView(generics.CreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalCreateSerializer

    def post(self, request, format=None):
        serializer = ProposalCreateSerializer(data=request.data)
        if serializer.is_valid():
            proposal = serializer.save()
            return Response(
                {
                    'message': 'Proposta salva com sucesso.',
                    'proposal_id': proposal.id
                }
            )
        return Response(serializer.errors, status=400)


class ProposalConfigCreateAPIView(generics.CreateAPIView):
    queryset = ProposalConfig.objects.all()
    serializer_class = ProposalConfigSerializer

    def post(self, request, format=None):
        serializer = ProposalConfigSerializer(data=request.data)
        if serializer.is_valid():
            proposal_config = serializer.save()
            return Response(
                {
                    'message': 'Proposta salva com sucesso.',
                    'proposal_data_id': proposal_config.id
                }
            )
        return Response(serializer.errors, status=400)


class ProposalConfigListView(generics.ListAPIView):
    queryset = ProposalConfig.objects.all()
    serializer_class = ProposalConfigSerializer


class ProposalListView(generics.ListAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalDataListView(generics.ListAPIView):
    queryset = ProposalData.objects.all()
    serializer_class = ProposalDataSerializer


class ProposalStatusUpdateView(APIView):
    def put(self, request, proposal_id):
        try:
            proposal = Proposal.objects.get(id=proposal_id)
        except Proposal.DoesNotExist:
            return Response(status=404)

        serializer = UpdateProposalStatusSerializer(
            proposal, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
