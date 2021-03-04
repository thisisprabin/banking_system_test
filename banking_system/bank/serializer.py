from rest_framework.serializers import ModelSerializer
from bank.models import User

__all__ = ["UserSerializer"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email_id")
