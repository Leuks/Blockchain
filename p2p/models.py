from django.db import models

from Blockchain import enum
from Blockchain.settings import public_keys
import rsa
from chain.models import Blockchain
import random
import time


class Network(models.Model):
    def __init__(self):
        self.nodes = []
        self.main_node = self.build_main_node()

    def size(self):
        return len(self.nodes)

    def new_node(self, id, version, hacked):
        node = {
            'id': id,
            'privkey': self.keyGeneration(id),
            'chain': Blockchain(self.main_node, version) if int(hacked) == 0 else Blockchain(self.build_hacked_node(), version)
        }
        self.nodes.append(node)
        print("NODE CREATED")

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

    def build_hacked_node(self):
        id = 'hacked'+str(time.time())
        node = {
            'id': id,
            'privkey': self.keyGeneration(id),
            'chain': None
        }
        return node

    def add_transactions_for_node(self, sender_id, to_id, kind):
        kinds = kind.split(",");
        sender = self.find_node_by_id(sender_id)
        for i in range(0, len(kinds)):
            for node in self.nodes:
                if(node['id'] == to_id):
                    k = self.get_value_for_kind(kinds[i])
                    if i == len(kinds) - 1:
                        node['chain'].new_transaction(k, sender, sender['chain'].get_current_version_for_kind(k), True, False)
                    else:
                        node['chain'].new_transaction(k, sender, sender['chain'].get_current_version_for_kind(k), False, False)

    def find_node_by_id(self, id):
        for node in self.nodes:
            if(node['id'] == id):
                return node

    def get_value_for_kind(self, kind):
        if kind == "Engine":
            return enum.KIND_ENGINE
        elif kind == "Stereo":
            return enum.KIND_STEREO
        else:
            return enum.KIND_NAV

    def reset(self):
        self.nodes = []
        self.main_node = self.build_main_node()

    def get_alea_node(self):
        alea = random.randint(0, len(self.nodes) - 1)
        return self.nodes[alea]

    def start_simulation(self, node_count, transaction_count):
        for i in range(0, int(node_count)):
            self.new_node("Node" + str(len(self.nodes)), random.randint(1, 5))

        for i in range(0, int(transaction_count)):
            kind = "Navigation,Stereo,Engine"
            first_node = self.get_alea_node()
            second_node = self.get_alea_node()

            while(first_node == second_node):
                second_node = self.get_alea_node()

            self.add_transactions_for_node(first_node['id'], second_node['id'], kind)


    class Meta:
        managed = False



