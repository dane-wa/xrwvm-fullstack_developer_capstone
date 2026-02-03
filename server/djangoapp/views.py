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
# from .populate import initiate


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

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

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
