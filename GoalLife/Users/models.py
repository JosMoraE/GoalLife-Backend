from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False) #Deberian haber mas de un emial?
    #meta_asocieada = models.ForeignKey() La entidad debil es meta entonces iria la foreign key en meta de Users
    #Los inicios de sesion y la fecha de creacion de la cuenta vienen en Django por lo que veo

    foto_perfil = models.ImageField(upload_to='perfiles', null=True, blank=True)
    plan_ahorro = models.CharField(max_length=20, choices=[('normal', 'Normal'), ('hardcore', 'Hardcore')], default='normal')
    numero_celular = models.CharField(max_length=15, null=True, blank=False) #Me complico?
    #Sistema de recompensas para tener una motivacion la cual el usuario entre
    racha_actual = models.IntegerField(default=0)
    racha_maxima = models.IntegerField(default=0)
    puntos = models.IntegerField(default=0)
    last_login = models.DateField(auto_now_add=True)

    # importante:
    # Username, Password, Fecha de creación (date_joined) y Last Login
    # YA VIENEN INCLUIDOS en AbstractUser. No necesitas escribirlos.
    def __str__(self):
        return f"{self.username}"