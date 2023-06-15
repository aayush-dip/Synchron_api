from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Synchron_api.views import (ProfileList,StandUpTeamList,SameTeamList,
                                TeamListCreateView,TeamRetrieveUpdateDestroyView,
                                LoginAPIView, StandUpListCreateView,
                                StandUpRetrieveUpdateDestroyView,MemberAndRemarksListCreateView, 
                                MemberAndRemarksRetrieveUpdateDestroyView)

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profiles/',ProfileList.as_view(), name='profiles'),
    path('teams/', TeamListCreateView.as_view(), name='team-list-create'),
    path('teams/<int:pk>/', TeamRetrieveUpdateDestroyView.as_view(), name='team-retrieve-update-destroy'),
    path('standup/', StandUpListCreateView.as_view(), name='standup-list-create'),
    path('standup/<str:team_name>/', StandUpTeamList.as_view(), name='standup-team-list'),
    path('standup/<int:pk>/', StandUpRetrieveUpdateDestroyView.as_view(), name='standup-retrieve-update-destroy'),
    path('memberandremarks/', MemberAndRemarksListCreateView.as_view(), name='memberandremarks-list-create'),
    path('memberandremarks/<int:pk>/', MemberAndRemarksRetrieveUpdateDestroyView.as_view(), name='membersandremarks-retrieve-update-destroy'),
    path('sprintid/<int:pk>/', SameTeamList.as_view(), name='sameteam'),

]
urlpatterns = format_suffix_patterns(urlpatterns)