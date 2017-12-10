from django.db import models
from Blockchain.settings import public_keys
import rsa
from chain.models import Blockchain


class Network(models.Model):
    def __init__(self):
        self.nodes = []
        self.main_node = self.build_main_node()

    def size(self):
        return len(self.nodes)

    def new_node(self, id):
        node = {
            'id': id,
            'privkey': self.keyGeneration(id),
            'chain': Blockchain(self.main_node)
        }
        self.nodes.append(node)

    def keyGeneration(self, id):
        (pubkey, privkey) = rsa.newkeys(512)
        public_keys[id] = pubkey
        return privkey

    def build_main_node(self):
        id = 'main'
        node = {
            'id': id,
            'privkey': self.keyGeneration(id),
            'chain': None
        }
        return node

    def add_transaction_for_node(self, sender_id, to_id, kind):
        for node in self.nodes:
            if(node['id'] == to_id):
                node['chain'].new_transaction(kind, self.find_node_by_id(sender_id)) #verifiy chain before adding trans

    def find_node_by_id(self, id):
        for node in self.nodes:
            if(node['id'] == id):
                return node

    class Meta:
        managed = False



