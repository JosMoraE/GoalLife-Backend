from rest_framework import serializers
from .models import Meta as MetaModelo, Gasto, Categoria, Consejo
from django.contrib.auth import get_user_model

# Obtenemos el modelo de usuario activo (User)
User = get_user_model()

#Para el registro del usuario nuevo
class RegistroSerializer(serializers.ModelSerializer):
    # La contraseña solo se escribe, nunca se devuelve por seguridad
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        # Usamos create_user para que la contraseña se encripte correctamente (Hash)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaModelo
        fields = '__all__'
        read_only_fields = ['usuario']

class GastoSerializer(serializers.ModelSerializer):
    nombre_categoria = serializers.CharField(source='categoria_asociada.nombre', read_only=True)
    icono_categoria = serializers.CharField(source='categoria_asociada.icono', read_only=True)
    class Meta:
        model = Gasto
        fields = '__all__'
        read_only_fields = ['usuario', 'es_hormiga'] # es_hormiga ahora es read_only porque lo calcula el sistema


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ConsejoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consejo
        fields = '__all__'