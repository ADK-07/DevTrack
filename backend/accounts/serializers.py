from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={
            "input_type: password"
        },
    )
    
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "password"]
        read_only_field = ['id']
        
    def validate_email(self, value):
        return value.strip().lower()
    
    #View calls serializer.save(). This is what triggers the serializer’s create().
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)