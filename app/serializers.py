from rest_framework import serializers

from app.models import User, Product, Insurance


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}


class UserInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'address', 'phone')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price')


class InsuranceSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['user'] = {
            'username': instance.user.username,
            'phone': instance.user.phone,
            'address': instance.user.address
        }
        data['product'] = {
            'name': instance.product.name,
            'price': instance.product.price
        }

        return data

    class Meta:
        model = Insurance
        fields = ('product', 'warranty_period')

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return Insurance.objects.create(**validated_data)
