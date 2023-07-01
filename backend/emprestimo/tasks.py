from .models import Proposal
from celery import shared_task
import requests
import json


@shared_task
def change_proposal_status(proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)
    url = "https://loan-processor.digitalsys.com.br/api/v1/loan/"

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "document": proposal.document,
        "name": proposal.name
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()

    if response.status_code == 200:
        result = response.json()
        if result['approved']:
            proposal.status = 'Aprovada'
            print("Proposta de "+proposal.name+" Aprovada")
        else:
            proposal.status = 'Negada'
            print("Proposta de "+proposal.name+" Negada")
        proposal.human_analysis = True
    else:
        proposal.status = 'Em análise'

    proposal.save()
