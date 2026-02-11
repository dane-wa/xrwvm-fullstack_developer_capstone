# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Crée une vue login_request pour gérer les requêtes de connexion.
@csrf_exempt
def login_user(request):
    # Récupérer le nom d’utilisateur et le mot de passe depuis le dictionnaire request.POST
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Essaie de vérifier si les identifiants fournis peuvent être authentifiés.
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # Si l’utilisateur est valide, appeler la méthode login pour connecter l’utilisateur courant.
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Créer une vue logout_request pour gérer la demande de déconnexion.
def logout_request(request):
    logout(request) # Mettre fin à la session de l’utilisateur
    data = {"userName":""} # Retourner un nom d’utilisateur vide
    return JsonResponse(data)

# Crée une vue registration pour gérer les requêtes d’inscription.
@csrf_exempt
def registration(request):
    context = {}

    # Charger les données JSON à partir du corps de la requête.
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Vérifier si l’utilisateur existe déjà
        User.objects.get(username=username)
        username_exist = True
    except:
        # S’il n’y en a pas, enregistrez simplement que c’est un nouvel utilisateur.
        logger.debug("{} is new user".format(username))

    # S’il s’agit d’un nouvel utilisateur
    if not username_exist:
        # Créer un utilisateur dans la table auth_user
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Connecter l’utilisateur et le rediriger vers la page de liste.
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
