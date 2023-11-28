from django.contrib import admin
from .models import Hero, Produit, Coupon, Adresse, UserData

admin.site.register(Hero)

# Créez une classe d'administration pour UserData
@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('prenoms', 'nom_de_famille', 'email', 'telephone',  'ville', 'address', 'code_postal')
    search_fields = ('prenoms', 'nom_de_famille', 'email', 'telephone',  'ville', 'address', 'code_postal')


class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'categorie', 'etat', 'image', 'reduction')  # Champs à afficher dans la liste des produits

admin.site.register(Produit, ProduitAdmin)


class couponAdmin(admin.ModelAdmin):
    list_display = ('value', 'reduction')  # Champs à afficher dans la liste des produits

admin.site.register(Coupon, couponAdmin)

admin.site.register(Adresse)
