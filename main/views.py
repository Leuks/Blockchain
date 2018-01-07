import json

import sys
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from Blockchain.apps import p2pNetwork


def home(request):
    nodes = p2pNetwork.nodes

    current_nodes = []
    for node in nodes:
        sum_transac = 0
        for block in node['chain'].chain:
            sum_transac += len(block['transactions'])

        versions = node['chain'].get_current_versions()
        current_nodes.append({
            'node' : node,
            'version_nav': versions[0],
            'version_engine': versions[1],
            'version_stereo': versions[2],
            'count_transactions' : sum_transac
        })

    return render(request, 'base.html', {"nodes": current_nodes})

def detail(request, node_id):
    node = p2pNetwork.find_node_by_id(node_id)
    return render(request, 'detail.html', {"node": node})
