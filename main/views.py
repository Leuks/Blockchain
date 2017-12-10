import json

import sys
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from Blockchain.apps import p2pNetwork


def home(request):
    nodes = p2pNetwork.nodes
    return render(request, 'base.html', {"nodes": nodes})

