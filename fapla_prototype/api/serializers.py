from rest_framework import serializers
from .models import Household, Membership, Task, Responsibility, ShoppingItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'last_login',
        )

# for user search in case of household invitation
class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer_short(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )

class MembershipSerializer(serializers.ModelSerializer):
    #member = UserSerializer_short(read_only=True)
    member_name = serializers.CharField(source='member.username')
    member_id = serializers.IntegerField(source='member.id')
    class Meta:
        model = Membership
        fields = (
            'member_id',
            'member_name',
            'joined_at',
            'inviter',
            )

class HouseholdSerializer(serializers.ModelSerializer):
    members = MembershipSerializer(source='memberships', many=True, read_only=True)
    class Meta:
        model = Household
        fields = (
            'id',
            'name',
            'created_at',
            'creator',
            'members',
        )

    
    def create(self, validated_data):
        user = self.context["request"].user

        household = Household.objects.create(
            creator=user,
            **validated_data
        )

        # Add creator as member
        Membership.objects.create(
            household=household,
            member=user,
            inviter=user,
        )

        return household

# Serializer for Household Post Reqs
class HouseholdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = (
            'name',
        )


# basic serializer for tasks
class TaskSerializer(serializers.ModelSerializer):
    executors = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "finished",
            "due_by",
            "type",
            "scope",
            "created_at",
            "created_by",
            "executors",
        ]
        read_only_fields = ["created_by", "created_at", "executors"]

    # gets the relevant info on executors
    def get_executors(self, obj):
        return [
            {
                "id": r.executor.id,
                "username": r.executor.username,
                "accepted_at": r.accepted_at,
            }
            for r in obj.responsibilities.select_related("executor")
        ]

    # Checks if the task's scope is a household, that the user is member of(scope=blank ok => personal task)
    def validate_scope(self, scope):
        user = self.context["request"].user

        if scope is None:
            return scope

        is_member = scope.members.filter(id=user.id).exists()
        if not is_member:
            raise serializers.ValidationError(
                "You are not a member of this household."
            )

        return scope
    
    # if its a POST req, add user for created_by
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
    
# serializer for responsibility
class ResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = ["id", "task", "executor", "accepted_at"]
        read_only_fields = ["executor", "accepted_at"]

# basic serializer for ShoppingItems
class ShoppingItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingItem
        fields = [
            "id",
            "name",
            "description",
            "bought",
            "scope",
            "created_at",
            "created_by",
            "amount",
            "preferred_brand",
            "store",
        ]
        read_only_fields = ["created_by", "created_at"]


    # Checks if the task's scope is a household, that the user is member of(scope=blank ok => personal task)
    def validate_scope(self, scope):
        user = self.context["request"].user

        if scope is None:
            return scope

        is_member = scope.members.filter(id=user.id).exists()
        if not is_member:
            raise serializers.ValidationError(
                "You are not a member of this household."
            )

        return scope
    
    # if its a POST req, add user for created_by
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

# for the frontend to query about a logged in user's info
class MeSerializer(serializers.ModelSerializer):
    households = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "households",
        ]

    def get_households(self, obj):
        memberships = Membership.objects.select_related("household").filter(member=obj)

        return [
            {
                "id": m.household.id,
                "name": m.household.name,
                "joined_at": m.joined_at,
            }
            for m in memberships
        ]