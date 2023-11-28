from django.urls import path
from .views import Index, Shop, Cart,Checkout, Contact, Detail, Add2cart, Validate_coupon, SupprimerDuPanier, Update_total, Checkout2
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('',Index.as_view(),name="index"),
    path('validate-coupon', csrf_exempt(Validate_coupon.as_view()),name="validate"),
    path('update_total', csrf_exempt(Update_total.as_view()),name="update"),
    path('shop',Shop.as_view(),name="shop"),
    path('adresse',csrf_exempt(Checkout2.as_view()),name='adresse'),
    path('checkout',csrf_exempt(Checkout.as_view()),name='checkout'),
    path('cart',Cart.as_view(),name='cart'),

    path('contact',Contact.as_view(),name='contact'),
    path('detail/<int:produit_id>/',Detail.as_view(),name='detail'),
    path('ajouter-au-panier/<int:produit_id>/', Add2cart.as_view(), name='ajouter_au_panier'),
    path('supprimer-du-panier/<int:item_id>/', SupprimerDuPanier.as_view(), name='supprimer_du_panier'),
    path('upload_receipt/', views.upload_receipt, name='upload_receipt'),

]