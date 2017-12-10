from django.http import HttpResponse
from django.shortcuts import render
from Blockchain.apps import p2pNetwork

def new_node(request):
    id = request.POST.get("id")
    p2pNetwork.new_node(id)
    return HttpResponse()

def new_transaction(request):
    sender_id = request.POST.get("from")
    to_id = request.POST.get("to")
    kind = request.POST.get("kind")

    p2pNetwork.add_transaction_for_node(sender_id, to_id, kind)

def size(request):
    return HttpResponse(p2pNetwork.size())