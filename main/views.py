from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Produit, Panier, ItemPanier, Coupon, Total, Adresse, UserData, Receipt, Hero
import json #to jsonify some data
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage


class Index(View):
    def get(self,request):
        produits = Produit.objects.all()[:40]  # Récupérer les 20 premiers produits
        hero = Hero.objects.all()
        context = {
            'produits': produits,
            'heros':hero

        }
        if request.user.is_authenticated:
            panier, created = Panier.objects.get_or_create(user=request.user)
            items = ItemPanier.objects.filter(panier=panier)
            total = sum(item.total_cost for item in items)
            totalitem = sum(item.quantite for item in items)
            context = {
                "items":items,
                'produits': produits,
                "total": total,
                "totalitem": totalitem,
                'heros':hero
            }
            return render(request,"index.html",context)

        return render(request,"index.html",context)



class Shop(View):
    def get(self, request):
        produits = Produit.objects.all()
        context = {
            "produits": produits,
        }
        if request.user.is_authenticated:
            panier, created = Panier.objects.get_or_create(user=request.user)
            items = ItemPanier.objects.filter(panier=panier)
            total = sum(item.total_cost for item in items)
            totalitem = sum(item.quantite for item in items)
            context.update({
                "items": items,
                "total": total,
                "totalitem": totalitem,
            })
        return render(request, "all_product.html", context)

    def post(self, request):
        category_name = request.POST.get("categorie")
        search_query = request.POST.get("search")

        products = Produit.objects.all()

        if category_name == "all":
            category_name = None  # To indicate no category filter

        if category_name:
            products = products.filter(categorie=category_name)
        elif search_query:
            products = products.filter(nom__icontains=search_query)

        if request.user.is_authenticated:
            panier, created = Panier.objects.get_or_create(user=request.user)
            items = ItemPanier.objects.filter(panier=panier)
            total = sum(item.total_cost for item in items)
            totalitem = sum(item.quantite for item in items)
            context = {
                "produits": products,
                "items": items,
                "total": total,
                "totalitem": totalitem,
                "categorie": category_name,
                "search_query": search_query,
            }
        else:
            context = {"produits": products}

        return render(request, "shop-grid.html", context)



class Contact(View):
    def get(self, request):
        return render(request,"contact.html")


class Detail(View):
    def get(self,request,produit_id):
        # Retrieve the product based on the provided ID, or return a 404 error if not found
        product = get_object_or_404(Produit, pk=produit_id)

        # Pass the extracted data to the template
        context = {
            'product':product
        }

        return render(request, 'product-details.html', context)


class Cart(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("google_login")
        panier, created = Panier.objects.get_or_create(user=request.user)
        items = ItemPanier.objects.filter(panier=panier)
        total = sum(item.total_cost for item in items)
        totalitem = sum(item.quantite for item in items)
        context = {
            "items":items,
            "total": total,
            "totalitem": totalitem,
        }
        return render(request,"cart_summary.html",context)



class Add2cart(View):
    def get(self, request, produit_id):
        if not request.user.is_authenticated:
            return redirect("google_login")
        produit = get_object_or_404(Produit, id=produit_id)
        panier, created = Panier.objects.get_or_create(user=request.user)
        item, item_created = ItemPanier.objects.get_or_create(panier=panier, produit=produit)
        if not item_created:
            item.quantite += 1
            item.save()
        return redirect('cart')  # Redirige vers la vue du panier


class Checkout(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect("google_login")
        total,created = Total.objects.get_or_create(user=request.user)

        total_user = total.total_amount
        context = {
            "total":total_user
        }
        return render(request,"checkout.html",context)

"""class Profil(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, "authentication/login.html")
        return render(request,"index.html")"""

"""class Validate_coupon(View):
    def post(self,request):
        data=json.loads(request.body)

        try :
            value = data['coupon']
            if not str(value).isalnum():
                return JsonResponse({'coupon_error':"le coupon ne peux pas contenir de caractères spéciaux"},status=400)

            elif not Coupon.objects.filter(value=str(value)).exists():
                return JsonResponse({"coupon_error":"Désolé, le coupon est invalide"},status=400)

            else:
                couponobj = get_object_or_404(Coupon,value=str(value))
                return JsonResponse({"reduc":couponobj.reduction},status=400)
        except :
            user = request.user
            new_value = data['total']  # Supposons que le champ value soit passé dans la requête POST

            total = Total.objects.filter(user=user).first()


            if not total:
                total = Total(user=user)

            # Mettez à jour la valeur et enregistrez le modèle
            total.value = new_value
            total.save()

            return JsonResponse({'message': 'Total updated successfully.'})"""

class Validate_coupon(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("google_login")
        data = json.loads(request.body)

        value = data['coupon']
        if not str(value).isalnum():
            return JsonResponse({'coupon_error': "le coupon ne peut pas contenir de caractères spéciaux"}, status=400)

        elif not Coupon.objects.filter(value=str(value)).exists():
            return JsonResponse({"coupon_error": "Désolé, le coupon est invalide"}, status=400)

        else:
            couponobj = get_object_or_404(Coupon, value=str(value))
            return JsonResponse({"reduc": couponobj.reduction})


class Update_total(View):
   def post(self, request):
        if not request.user.is_authenticated:
            return redirect("google_login")
        data = json.loads(request.body)
        user = request.user
        new_value = data.get('total')

        try:
            new_value_int = int(new_value)  # Convertir en nombre entier

            # Vérifier si l'utilisateur a déjà une instance de Total
            total, created = Total.objects.get_or_create(user=user)

            # Mettre à jour la valeur et enregistrer le modèle
            total.total_amount = new_value_int
            total.save()

            return JsonResponse({'message': 'Total updated successfully.'})

        except (ValueError, TypeError) as e:
            return JsonResponse({'error': 'Invalid value provided.'}, status=400)



class SupprimerDuPanier(View):
    def get(self, request, item_id):
        if not request.user.is_authenticated:
            return redirect("google_login")
        item = ItemPanier.objects.get(id=item_id)
        item.delete()
        return redirect('cart')


class Checkout2 (View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("google_login")
        addresse = Adresse.objects.all()[0]
        total,created = Total.objects.get_or_create(user=request.user)
        total_user = total.total_amount
        context = {
            "addresse":addresse,
            "total":total_user
        }

        return render(request,"payement.html",context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("google_login")
        # Récupérez les données du formulaire à partir de la requête POST
        prenoms = request.POST['name']
        nom_de_famille = request.POST['firstname']
        email = request.POST['email']
        telephone = request.POST['number']
        ville = request.POST['state-province']
        address = request.POST['address']
        code_postal = request.POST['post']

        # Créez une instance de UserData avec les données du formulaire
        user_data = UserData(
            prenoms=prenoms,
            nom_de_famille=nom_de_famille,
            email=email,
            telephone=telephone,
            ville=ville,
            address=address,
            code_postal=code_postal
        )

        # Enregistrez les données dans la base de données
        user_data.save()


        # Redirigez l'utilisateur vers une autre page après la soumission du formulaire
        return redirect('adresse')




@login_required  # Ensure the user is logged in
def upload_receipt(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('receipt_image')

        if uploaded_file:
            # Save the receipt
            receipt = Receipt(receipt_image=uploaded_file,user=request.user)
            receipt.save()

            # Get the URL of the uploaded receipt image (you may need to adjust this)
            receipt_url = receipt.receipt_image.url

            # Create an EmailMessage object
            email_subject = 'NOuveau recu du site de iphone'
            email_body = 'UN nouveau recu a été envoyé.'
            from_email = 'appleshopnow@outlook.com'  # Replace with the sender's email address
            to_email = ['suppoeshop@gmail.com']  # Replace with the recipient's email address

            email = EmailMessage(email_subject, email_body, from_email, to_email)

            # Attach the receipt image file to the email
            email.attach_file(receipt.receipt_image.path)

            # Send the email
            email.send()

            return redirect('adresse')  # Redirect to the 'adresse' page after a successful upload
    else:
        return redirect('adresse')

    return redirect('adresse')
