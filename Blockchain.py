import hashlib
import json
import queue

class Blockchain:

    global COMPLEXITY
    global HASH_LENGTH
    global NUMBER_OF_TRANSACTIONS_IN_A_BLOCK
    COMPLEXITY = 4
    HASH_LENGTH = 12
    NUMBER_OF_TRANSACTIONS_IN_A_BLOCK = 4 

    #create blockchain
    def __init__(self):
        self.blockchain = [
            [{"hash": COMPLEXITY*"0"},
            {
                "from": "",
                "to": "",
                "amount": 0.0
            }]
        ]
        self.stack = queue.Queue()
        self.wallets = []

    #create new wallet
    def createWallet(self, name, amount = 0):
        wallet = {
            "name": name,
            "amount": amount
        }
        self.wallets.append(wallet)

    #try to find exiting wallet
    def checkUser(self, name):
        for wallet in self.wallets:
            if wallet["name"] == name: 
                return True
        return False

    def getBalance(self, name):
        for wallet in self.wallets:
            if wallet["name"] == name: 
                return wallet["amount"]    

    #check transactions in the block
    def checkTransactionsInBlock(self, block):
        for i in range(1, NUMBER_OF_TRANSACTIONS_IN_A_BLOCK+1, 1):
            if not self.checkUser(block[i]["from"]) or not self.checkUser(block[i]["to"]) or not (self.getBalance(block[i]["from"]) >= block[i]["amount"]):
                return False
        return True

    def setBalance(self, block):
        for i in range(1, NUMBER_OF_TRANSACTIONS_IN_A_BLOCK+1, 1):
            nameFrom = block[i]["from"]
            nameTo = block[i]["to"]
            amount = block[i]["amount"]
            for wallet in self.wallets:
                if wallet["name"] == nameFrom:
                    wallet["amount"] = int(wallet["amount"]) - amount
                if wallet["name"] == nameTo:
                    wallet["amount"] = int(wallet["amount"]) + amount

    #add new transaction to stack 
    def newTransaction(self, fromUser, toUser, amount):
        transaction = {
            "from": fromUser,
            "to": toUser,
            "amount": amount,
        }
        self.stack.put(transaction)

    #create hash from data
    def dataToHash(self, data):
        json_data = json.dumps(data, sort_keys = True)
        binary_data = json_data.encode()
        return hashlib.sha256(binary_data).hexdigest()[:HASH_LENGTH]

    #method for mineProofOfWork
    def isValidProof(self, block, proof):
        block_copy = block.copy()
        block_copy.append([{"proof": proof}]) 
        self.hash = self.dataToHash(block_copy)
        return self.hash[0:COMPLEXITY] == COMPLEXITY*"0"

    #find the number which create a valid hash
    def mineProofOfWork(self, block):
        proof = 0
        while not self.isValidProof(block, proof):
            proof += 1
        return proof

    #creating a new block with transactions from stack, actually mining
    def mine(self):
        j = NUMBER_OF_TRANSACTIONS_IN_A_BLOCK
        if self.stack.qsize() >= j:
            new_block = []
            prev_block = self.blockchain[-1]

            prev_hash = prev_block[0]["hash"]
            new_block.append({"prev_hash": prev_hash, "hash": "", "data_hash": ""})
            while j != 0:
                transaction_information = self.stack.get()
                new_block.append({
                    "from": transaction_information["from"],
                    "to": transaction_information["to"],
                    "amount": transaction_information["amount"],
                })
                j -= 1

            #mining 
            self.mineProofOfWork(new_block[1:])

            new_block[0]["hash"] = self.hash
            new_block[0]["data_hash"] = self.dataToHash(new_block[1:])
            self.blockchain.append(new_block)
        else: print("The stuck isn't full yet.\n")
            
    #validate the entire blockchain
    def validateBlockchain(self):
        prev_block = None
        i = 0

        print("Validation process started...")
        for block in self.blockchain:
            if prev_block:
                actual_hash = self.dataToHash(block[1:])
                recorded_data_hash = block[0]["data_hash"]

                recorded_prev_hash = block[0]["prev_hash"]
                prev_hash = prev_block[0]["hash"]

                if actual_hash != recorded_data_hash or recorded_prev_hash[0:COMPLEXITY] != COMPLEXITY*"0":
                    if actual_hash != recorded_data_hash: print(f"Blockchain is invalid in block {i}! Current block hash doesn't match, expected {recorded_data_hash}, actual = {actual_hash}")
                    if recorded_prev_hash[0:COMPLEXITY] != COMPLEXITY*"0": print(f"Blockchain is invalid in block {i}! The previous hash doesn't match, expected {prev_hash}, actual = {recorded_prev_hash}")
                else:
                    if not self.checkTransactionsInBlock(block):
                        print(f"Block {i}, wrong trasaction")
                    else:
                        #give coins
                        self.setBalance(block)
                        print(f"Block {i} Valid hash {actual_hash}")

            prev_block = block
            i += 1 
        print("Validation process completed!\n")       

    #print the entire blockchain
    def checkBlockchain(self):
        i = 0
        for block in self.blockchain:
            print(f"Block № {i}")
            for transaction in block:
                print(transaction)
            print("\n")
            i += 1