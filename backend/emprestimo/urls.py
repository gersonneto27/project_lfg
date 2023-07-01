from django.urls import path
from .views import (
                        ProposalConfigCreateAPIView,
                        ProposalConfigListView,
                        ProposalCreateAPIView,
                        ProposalDataListView,
                        ProposalListView,
                        ProposalStatusUpdateView
                    )

app_name = 'proposalapp'

urlpatterns = [
     path(
          'proposals/',
          ProposalListView.as_view(),
          name='proposal-list'
     ),
     path(
         'proposals/create',
         ProposalCreateAPIView.as_view(),
         name='create_proposal'
     ),
     path(
         'proposal-config/create',
         ProposalConfigCreateAPIView.as_view(),
         name='create_proposal_data'
     ),
     path(
          'proposal-configs/',
          ProposalConfigListView.as_view(),
          name='proposal-config-list'
     ),
     path(
         'proposal-data/',
         ProposalDataListView.as_view(),
         name='proposal-data-list'
     ),
     path(
         'proposals/status-change/<int:proposal_id>',
         ProposalStatusUpdateView.as_view(),
         name='proposal-data-list'
     ),
]
