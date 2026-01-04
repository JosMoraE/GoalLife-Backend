from django.db import models
from django.utils import timezone
from django.conf import settings #Sirve para acceder a variables globales de tu proyecto.
#NOTA: USAMOS CONVENCION SNAKE CASE
#En este caso, lo necesitas para 
# decirle a tus modelos: "Oye, usa el Usuario que definí en settings.py (AUTH_USER_MODEL)", sin tener que importar el archivo directamente.

#from Users import Users || Esto es peligroso. 
# Hacer importaciones directas de modelos de usuarios suele causar errores de "dependencia circular" (el huevo y la gallina).

# Utilidades para React Native

# --- MODELOS DE SOPORTE ---


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50, blank=True) #Nombre del icono para react native
    
    def __str__(self):
        return self.nombre
    
#Para evitar que los usuarios tengan que actualizar este apartado siempre que se agregue un consejo desde react
#Entonces seria mas facil hacerlo parte de la tabla para que se actualice automaticamente sin necesidad de actualizaciones

class Consejo(models.Model):
    texto = models.TextField()
    categoria = models.CharField(max_length=50, default="General")
    
    def __str__(self):
        return self.texto[:50]



# --- MODELOS PRINCIPALES ---


# blank=False, null=False significa que entonces el campo es obligatorio? 
class Meta(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.TextField(max_length=500, blank=False, null=False)
    monto_objetivo = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    fecha_limite = models.DateField()
    prioridad = models.IntegerField(default=1) # 1 al 5
    imagen = models.ImageField(upload_to='metas/',null=True,blank=True) #Con upload_to, indco donde se guarda la imagen
    finalizada = models.BooleanField(default=False)
    es_hardcore = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True) 
    #default=timezone.now es mas flexible que auto_now_add ya que ese fija la fecha sin poder cambiarla

    #Foreign keys
    # Usamos settings.AUTH_USER_MODEL. 
    # on_delete=CASCADE: Si borras el usuario, se borran sus metas (Lógico).
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"
    
class Ingreso(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False) #Nombre del ingreso, de donde vino, seria la descripcion como la de banco pichincha
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    fecha_ingreso = models.DateField(auto_now_add=True, blank=False, null=False) #Cuando se hizo efectivo
    es_recurrente = models.BooleanField(default=False)
    es_pendiente = models.BooleanField(default=False) #Si es obligacion financiera o no
    #Nota, si es True, entonces me deben dinero aun no lo tengo (Cuenta por cobrar), si es false, entonces ya lo tengo (Ingreso real)

    #Foreign key
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meta_asociada = models.ForeignKey(Meta, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        estado = "Por Cobrar" if self.es_pendiente else "Recibido"
        return f"{self.nombre} - {self.cantidad} ({estado})"
    

class Gasto(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False) #Nombre del Gasto, de donde vino, seria la descripcion como la de banco pichincha
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    fecha_gasto = models.DateField(auto_now_add=True, blank=False, null=False)
    es_hormiga = models.BooleanField(default=False)

    #Foreign Keys
    meta_asociada = models.ForeignKey(Meta, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria_asociada = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"Gasto ${self.cantidad} - {self.categoria_asociada}"
    
# Se podria hacer un merge por herencia de cuentas por pagar y gastos pero no lo veo tan bueno
# Esto se debe a que si bien solo agrego 2 atributos mas y ambas entidades comparten 3 atributos
# Deberian ser entidades por separadas por el peso legal y economico que tiene cada uno a partir de su concepto
# Pero no estoy seguro aun

class Obligacion(models.Model): #Cuentas por pagar
    nombre = models.CharField(max_length=100, blank=False, null=False) #Nombre del Gasto, de donde vino, seria la descripcion como la de banco pichincha
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    fecha_registro = models.DateField(auto_now_add=True, blank=False, null=False)
    fecha_vencimiento = models.DateField(blank=False, null=False)
    estado_pago = models.BooleanField(default=False)

    #Foreign Keys
    meta_asociada = models.ForeignKey(Meta, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria_asociada = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    
    def __str__(self):
        return f"{self.nombre} - Vence: {self.fecha_vencimiento}"
    