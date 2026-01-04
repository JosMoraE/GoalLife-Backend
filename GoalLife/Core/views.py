from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Meta, Gasto, Categoria
from .serializers import MetaSerializer, GastoSerializer, CategoriaSerializer
from django.db.models import Sum
from decimal import Decimal

from rest_framework.permissions import AllowAny #Esto es solo para las pruebas
from django.contrib.auth import get_user_model

# GET = Obtener informacion, POST = Mostrar o Enviar

#Mostramos la informacion general
@api_view(['GET'])
def api_home(request):
    metas = Meta.objects.all()
    gastos = Gasto.objects.all()

    #CALCULOS
    #Logica de suma
    #Sumamos todo el dinero de los objetivos
    total_objetivo = Meta.objects.aggregate(Sum('monto_objetivo'))['monto_objetivo__sum'] or 0
    #Sumamos todo lo gastado
    total_gasto = Gasto.objects.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    #Todo lo ahorrado
    total_ahorrado = Meta.objects.aggregate(Sum('monto_actual'))['monto_actual__sum'] or 0
    

    metas_serializer = MetaSerializer(metas, many=True)
    gastos_serializer = GastoSerializer(gastos, many=True)

    return Response({
        'resumen': {
            'total_objetivo': total_objetivo,
            'total_gastado': total_gasto,
            'total_ahorrado': total_ahorrado,
            'conteo_metas': metas.count()
        },
        'metas': metas_serializer.data,
        'gastos': gastos_serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def api_crear_meta(request): #Se crea una meta sobre el apartado de la app donde dice agregar. Creo que de nombre en vez de agregar le pondria "Meta" de nombre
    # 'request.data' son los datos que vienen del celular (JSON)
    print("Datos recibidos del celular:", request.data)

    #Usuarios
    # User = get_user_model()
    # user = User.objects.first()

    user = request.user

    #Pasar datos al serializador
    serializer = MetaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(usuario = user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Si hay error (ej: falta nombre), devolvemos el error
    print("ERROR DE VALIDACIÓN:", serializer.errors)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_crear_gasto(request):
    print("Gasto recibido del celular", request.data)

    #Usuarios
    User = get_user_model()
    user = User.objects.first()

    #Pasar datos al serializador

    serializer = GastoSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(usuario = user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print("ERROR DE VALIDACION: ", serializer.errors)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def api_sumar_ahorro(request):
    meta_id = request.data.get('meta_id')
    monto_a_sumar = request.data.get('monto')

    try:
        #Buscamos meta especifica
        meta = Meta.objects.get(id=meta_id)

        #LOGICA DE AHORRO
        #Se convierte a float para sumar decimales

        meta.monto_actual += Decimal(monto_a_sumar)

        #Validamos que no se pase del objetivo
        if meta.monto_actual >= meta.monto_objetivo:
            meta.finalizada = True

        meta.save()

        return Response({'mensaje' : 'Ahorro registrado', 'nuevo_monto': meta.monto_actual })
    except Meta.DoesNotExist:
        return Response({'ERROR' : 'Meta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

class UserProfileSummaryView(APIView):
    #Habilitar la autenticacion
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Usamo el usuario autenticado
        user = request.user
        
        # 1. Calcular Ahorro Total
        total_ahorrado = Meta.objects.filter(
            usuario=user
        ).aggregate(Sum('monto_actual'))['monto_actual__sum'] or 0

        # 2. Calcular Valor en Metas Activas
        valor_metas_activas = Meta.objects.filter(
            usuario=user, 
            finalizada=False
        ).aggregate(Sum('monto_objetivo'))['monto_objetivo__sum'] or 0

        # Datos del usuario
        nombre_completo = f"{user.first_name} {user.last_name}".strip()
        if not nombre_completo:
            nombre_completo = user.username

        data = {
            "full_name": nombre_completo,
            "role_description": "Estudiante & Ahorrador", 
            "total_savings": total_ahorrado,
            "active_goals_value": valor_metas_activas
        }
        
        return Response(data)
    
#Funciones para eliminar los registros
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_eliminar_meta(request, meta_id):
    try:
        # Solo borra si la meta pertenece al usuario logueado
        meta = Meta.objects.get(id=meta_id, usuario = request.user)
        meta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Meta.DoesNotExist:
        return Response({"Error" : "No encontrada"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_eliminar_gasto(request, gasto_id):
    try:
        gasto = Gasto.objects.get(id=gasto_id, usuario=request.user)
        gasto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Gasto.DoesNotExist:
        return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)


#Categorias
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_categorias(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)