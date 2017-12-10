import json
import rsa
from django.db import models
import hashlib
import time
from Blockchain.enum import *

class Blockchain(models.Model):
    def __init__(self, main_node):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        transaction_engine = {
            'kind': KIND_ENGINE,
            'sender_id': main_node["id"]
        }
        transaction_stereo = {
            'kind': KIND_ENGINE,
            'sender_id': main_node["id"]
        }
        transaction_nav = {
            'kind': KIND_ENGINE,
            'sender_id': main_node["id"]
        }

        signed_transaction_engine = self.sign_transaction(transaction_engine, main_node);
        signed_transaction_stereo = self.sign_transaction(transaction_stereo, main_node);
        signed_transaction_nav = self.sign_transaction(transaction_nav, main_node);

        block = {
            'id': 1,
            'timestamp': time.time(),
            'transactions': [signed_transaction_engine, signed_transaction_stereo, signed_transaction_nav],
            'proof': 100,
            'previous_hash': 1
        }

        self.chain.append(block)

    def size(self):
        return len(self.chain)

    def get_last_block(self):
        return self.chain[self.size() - 1]

    def new_block(self):
        last_block = self.chain[self.size() - 1]
        proof = self.proof_of_work(last_block['proof'])
        id = self.hash(last_block)

        block = {
            'id': id,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': 1,
        }

        self.current_transactions = []
        self.chain.append(block)

    def new_transaction(self, kind, sender):
        if(self.verify_chain(sender)):
            transaction = {
                'kind': kind,
                'sender_id': sender['id']
            }

            signed_transaction = self.sign_transaction(transaction, sender)
            self.current_transactions.append(signed_transaction)

    def sign_transaction(self, transaction, sender):
        transaction['kind'] = rsa.sign(json.dumps(transaction['kind']).encode(), sender.privkey, 'SHA-1')
        return transaction

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def verify_chain(self, node):
        if(node['chain'][0]['id'] == 'main'):
            return True
        else:
            return False



    def __str__(self):
        return self.chain.__str__()






