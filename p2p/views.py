from django.http import HttpResponse
from django.shortcuts import render
from Blockchain.apps import p2pNetwork

def new_node(request):
    id = request.POST.get("id")
    version = request.POST.get("version")
    print("version" + version)
    p2pNetwork.new_node(id, int(version))
    return HttpResponse()

def new_transaction(request):
    sender_id = request.POST.get("from")
    to_id = request.POST.get("to")
    kind = str(request.POST.get("kind"))
    p2pNetwork.add_transactions_for_node(sender_id, to_id, kind)
    return HttpResponse()

def new_simulation(request):
    nodes_count = request.POST.get("nodes_count")
    transactions_count = request.POST.get("transactions_count")
    p2pNetwork.reset()
    p2pNetwork.start_simulation(nodes_count, transactions_count)
    return HttpResponse()

def size(request):
    return HttpResponse(p2pNetwork.size())