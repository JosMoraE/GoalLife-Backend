from rest_framework import serializers
from .models import Meta as MetaModelo, Gasto, Categoria, Consejo

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
        read_only_fields = ['usuario']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ConsejoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consejo
        fields = '__all__'