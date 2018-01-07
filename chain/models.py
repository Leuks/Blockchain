import json
import rsa
from django.db import models
import hashlib
import time

from Blockchain import enum
from Blockchain.enum import *

class Blockchain(models.Model):
    def __init__(self, main_node, version):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_transaction(KIND_ENGINE, main_node, version, False)
        self.new_transaction(KIND_STEREO, main_node, version, False)
        self.new_transaction(KIND_NAV, main_node, version, False)

        block = {
            'id': 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': 100,
            'previous_hash': 1
        }

        self.current_transactions = []
        self.chain.append(block)

    def size(self):
        return len(self.chain)

    def get_last_block(self):
        return self.chain[self.size() - 1]

    def get_first_block(self):
        return self.chain[0]

    def new_block(self):
        last_block = self.chain[self.size() - 1]
        proof = self.proof_of_work(last_block['proof'])
        id = self.hash(last_block)

        block = {
            'id': id,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': 1,
        }

        self.current_transactions = []
        self.chain.append(block)
        print("BLOCK ADDED")

    def new_transaction(self, kind, sender, version, add):
        if(self.verify_chain(sender) and version > self.get_current_version_for_kind(kind)):
            transaction = {
                'kind': kind,
                'sender_id': sender['id'],
                'version': version
            }

            signed_transaction = self.sign_transaction(transaction, sender)
            self.current_transactions.append(signed_transaction)
            print("TRANSACTION ADDED")
            if add:
                self.new_block()

    def sign_transaction(self, transaction, sender):
        transaction['sign'] = rsa.sign(json.dumps(transaction['kind']).encode(), sender['privkey'], 'SHA-1')
        return transaction

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def hash(self, block):
        block_string = json.dumps(block['id'], sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def verify_chain(self, node):
        if(node['id'] == 'main' or self.is_node_from_main(node)):
            return True
        else:
            return False

    def is_node_from_main(self, node):
        return node['chain'].get_first_block()['transactions'][0]['sender_id'] == 'main'

    def get_current_versions(self):
        last_tr_nav = None
        last_tr_stereo = None
        last_tr_engine = None

        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['kind'] == KIND_NAV:
                    if last_tr_nav == None:
                        last_tr_nav = transaction
                    elif last_tr_nav['version'] < transaction['version']:
                        last_tr_nav = transaction
                if transaction['kind'] == KIND_STEREO:
                    if last_tr_stereo == None:
                        last_tr_stereo = transaction
                    elif last_tr_stereo['version'] < transaction['version']:
                        last_tr_stereo = transaction
                if transaction['kind'] == KIND_ENGINE:
                    if last_tr_engine == None:
                        last_tr_engine = transaction
                    elif last_tr_engine['version'] < transaction['version']:
                        last_tr_engine = transaction
        return (last_tr_nav['version'], last_tr_engine['version'], last_tr_stereo['version'])

    def get_current_version_for_kind(self, kind):
        for block in reversed(self.chain):
            for transaction in block['transactions']:
                if transaction['kind'] == kind:
                    return transaction['version']
        return 0

    def __str__(self):
        return self.chain.__str__()






