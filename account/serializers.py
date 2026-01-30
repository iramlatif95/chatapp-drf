from rest_framework import serializers 
from.models import User 
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id','username','email','password']

    def create(self,validated_data):
        password=validated_data.pop('password')
        user=User.objects.create_user(password=password,**validated_data)
        return user


class Loginserializer(serializers.Serializer):
    username=serializers.CharField(max_length=50)
    password=serializers.CharField()



    



