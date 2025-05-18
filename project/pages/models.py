from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('visiteur', 'Visiteur'),
        ('membre', 'Membre'),
        ('arbitre', 'Arbitre'),
        ('admin', 'Administration'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visiteur')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def profile(self):
        return self.user_profile if hasattr(self, 'user_profile') else None


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    profile_picture = models.ImageField(upload_to='avatar/', blank=True, null=True)
    display_name = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    cin = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def avatar(self):
        if self.profile_picture:
            return self.profile_picture.url
        return f'{settings.STATIC_URL1}avatar/defaults.png'


class Ligue(models.Model):
    nom = models.CharField("Nom de la ligue", max_length=100, unique=True, null=False, blank=False)
    description = models.TextField("Description", blank=True)

    def __str__(self):
        return self.nom


class Actualite(models.Model):
    titre = models.CharField("Titre", max_length=200,null=False, blank=False)
    contenu = models.TextField("Contenu",null=False, blank=False)
    image = models.ImageField("Image", upload_to='actualites/',null=True, blank=True)
    date_pub = models.DateField("Date de publication", auto_now_add=True,null=False, blank=False)
    ligue = models.ForeignKey(
        Ligue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ligue associée",
        related_name='actualites'
    )

    class Meta:
        ordering = ['-date_pub']
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def __str__(self):
        return f"{self.titre} ({self.ligue or 'Général'})"
    
class Club(models.Model):
    nom = models.CharField("Nom du club", max_length=100, unique=True, null=False, blank=False)
    description = models.TextField("Description", blank=True)
    logo = models.ImageField("Logo", upload_to='clubs/', null=False, blank=False)
    ville = models.CharField("Ville", max_length=100, null=False, blank=False)
    ligue = models.ForeignKey(Ligue, on_delete=models.CASCADE, related_name='clubs')
    
    class Meta:
        verbose_name = "Club"
        verbose_name_plural = "Clubs"
    
    def __str__(self):
         return f"{self.nom} ({self.ligue.nom})"
    
    
class concours(models.Model):
    nom = models.CharField("Nom du concours", max_length=100, unique=True, null=False, blank=False)
    description = models.TextField("Description", blank=True)
    image = models.ImageField("Image", upload_to='concours/', null=False, blank=False)
    date_debut = models.DateField("Date de début", null=False, blank=False)
    date_fin = models.DateField("Date de fin", null=False, blank=False)
    ligue = models.ForeignKey(Ligue, on_delete=models.CASCADE, related_name='concours')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='concours',default=None, null=True, blank=True)
    class Meta:
        verbose_name = "Concours"
        verbose_name_plural = "Concours"

    def __str__(self):
     return f"{self.nom} - {self.date_debut.strftime('%d/%m/%Y')}"
    

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.full_name} ({self.email})"
