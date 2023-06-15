from Synchron_api.models import Profile, Team, StandupCard, MemberAndRemarks
from Synchron_api.serializers import UserProfileSerializer, TeamSerializer, StandUpSerializer, MemberAndRemarksSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Team
from Synchron_api.permissions import IsScrumMasterOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Create your views here.

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:

            # Check if user is a superuser
            profile = user.profile
            if profile.position == 'SM':
                is_scrummaster = True
            else:
                is_scrummaster = False
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'is_scrummaster': is_scrummaster
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileList(APIView):
    def get(self, request, format=None):
        query = '''SELECT * from auth_user as u
        FULL JOIN Synchron_api_profile AS p ON u.id = p.id'''
        profile = Profile.objects.all()
        serializer = UserProfileSerializer(profile, many=True)
        return Response(serializer.data)
    
    def post(self, request, fromat=None):
        serializer = UserProfileSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsScrumMasterOrReadOnly]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    

class TeamRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsScrumMasterOrReadOnly]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class StandUpListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsScrumMasterOrReadOnly]

    queryset = StandupCard.objects.all()
    serializer_class = StandUpSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data

        # Update the teamname field with the actual team name
        team_id = response_data.get('teamname')
        team = Team.objects.filter(pk=team_id).first()
        if team:
            print(team.team_name)
            response_data['teamname'] = team.team_name

        return Response(response_data)


class StandUpRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsScrumMasterOrReadOnly]
    queryset = StandupCard.objects.all()
    serializer_class = StandUpSerializer
    
class MemberAndRemarksListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsScrumMasterOrReadOnly]
    queryset = MemberAndRemarks.objects.all()
    serializer_class = MemberAndRemarksSerializer
    

class MemberAndRemarksRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsScrumMasterOrReadOnly]
    queryset = MemberAndRemarks.objects.all()
    serializer_class = MemberAndRemarksSerializer

class AllTeams(APIView):
    def get(self, request, format=None):
        query = '''SELECT * from Synchron_api_team '''
        teams = Team.objects.raw(query)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
class StandUpTeamList(APIView):
    def get(self, request, team_name, format=None):
        team = Team.objects.get(team_name=team_name)
        standups = StandupCard.objects.filter(teamname=team).order_by("created").reverse()
        serializer = StandUpSerializer(standups,many=True)
        return Response(serializer.data)

class SameTeamList(APIView):
    def get(self, request, pk, format=None):
        member = StandupCard.objects.get(sprint_id=pk)
        members = MemberAndRemarks.objects.filter(standup=member)
        serializer = MemberAndRemarksSerializer(members,many=True)
        return Response(serializer.data)