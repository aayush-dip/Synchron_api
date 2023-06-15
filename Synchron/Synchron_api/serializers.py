from rest_framework import serializers
from django.contrib.auth.models import User
from Synchron_api.models import Profile, Team, StandupCard, MemberAndRemarks

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):    
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'occupation', 'phone',  'address', 'city', 'country', 'position']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile



class TeamSerializer(serializers.ModelSerializer):
    query = '''SELECT * from auth_user'''
    members = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=User.objects.raw(query))
    class Meta:
        model = Team
        fields = ['team_name','members']

            
    def get_members(self, obj):
        usernames = [member.username for member in obj.members.all()]
        return usernames

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        team_members = User.objects.filter(team__id=instance.id)
        usernames = [member.username for member in team_members]
        representation['members'] = usernames
        return representation


class StandUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = StandupCard
        fields = ['created_by', 'topic', 'release_cycle', 
                  'sprint_id', 'created', 'updated', 'remarks', 'teamname']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        teamname = representation['teamname']
        team = Team.objects.filter(pk=teamname).first()
        representation['teamname'] = team.team_name
        return representation

        
class MemberAndRemarksSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberAndRemarks
        fields = ['individual_remarks', 'standup', 'member']

    def to_representation(self, instance):
        
        representation = super().to_representation(instance)
        standup = representation['standup']
        standup_card = StandupCard.objects.filter(pk=standup).first()
        representation['standup'] = standup_card.sprint_id
        member = representation['member']
        member_info = User.objects.filter(pk=member).first()
        representation['member'] = member_info.username
        return representation


