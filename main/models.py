from django.db import models
from django.contrib.auth.models import User

class Hero(models.Model):
    subtitle = models.CharField(max_length=255,null=True, blank=True)
    tile = models.CharField(max_length=255,null=True, blank=True)
    description = models.CharField(max_length=255,null=True, blank=True)
    price = models.CharField(max_length=255,null=True, blank=True)
    image = models.ImageField(upload_to='hero/')


class Coupon(models.Model):
    value = models.CharField(max_length=200)
    reduction = models.DecimalField(max_digits=5, decimal_places=2)

class Total(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    #reduction = models.DecimalField(max_digits=10)

class Panier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    produits = models.ManyToManyField('Produit', through='ItemPanier')



class ItemPanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantite * self.produit.prix


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    image = models.ImageField(upload_to='produits/')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    reduction = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    categorie = models.CharField(max_length=100)
    etat = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.nom


class Adresse(models.Model):
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='adresse/')
    iban = models.CharField(max_length=34, default='')  # Valeur par défaut vide pour IBAN
    code_banque = models.CharField(max_length=20, default='')  # Valeur par défaut vide pour le code de la banque
    numero_de_compte = models.CharField(max_length=30, default='')  # Valeur par défaut vide pour le numéro de compte
    bic = models.CharField(max_length=11, default='')  # Valeur par défaut vide pour BIC
    titulaire = models.CharField(max_length=200, default='')  # Valeur par défaut vide pour le titulaire
    pays = models.CharField(max_length=100, default='')  # Valeur par défaut vide pour le pays

    def __str__(self):
        return self.titulaire


class UserData(models.Model):
    prenoms = models.CharField(max_length=255)
    nom_de_famille = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    ville = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=5)


class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipt_image = models.ImageField(upload_to='receipts/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt for {self.user.username} uploaded on {self.upload_date}"


