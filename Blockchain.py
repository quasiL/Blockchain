import hashlib
import json

class Blockchain:

    global COMPLEXITY
    global HASH_LENGTH
    COMPLEXITY = 4
    HASH_LENGTH = 10

    #create blockchain
    def __init__(self):
        self.blockchain = [
            [{
                "from": "",
                "to": "",
                "amount": 0.0
            }, {}, {}, {"hash": COMPLEXITY*"0"}]
        ]
        self.stack = []
    
    #add new transaction to stack (need to write a real stack)
    def newTransaction(self, fromUser, toUser, amount):
        transaction = {
            "from": fromUser,
            "to": toUser,
            "amount": amount,
        }
        self.stack.append(transaction)

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
        j = 3
        if len(self.stack) >= j:
            new_block = []
            while j != 0:
                transaction_information = self.stack.pop()
                new_block.append({
                    "from": transaction_information["from"],
                    "to": transaction_information["to"],
                    "amount": transaction_information["amount"],
                })
                j -= 1
            prev_block = self.blockchain[-1]
            proof = self.mineProofOfWork(new_block)
            prev_hash = prev_block[3]["hash"]
            data_hash = self.dataToHash(new_block)
            new_block.append({"prev_hash": prev_hash, "hash": self.hash, "data_hash": data_hash})
            self.blockchain.append(new_block)
            
    #validate the entire blockchain
    def validateBlockchain(self):
        prev_block = None
        i = 0

        print("Validation process started...")
        for block in self.blockchain:
            if prev_block:
                actual_hash = self.dataToHash(block[0:3])
                recorded_data_hash = block[3]["data_hash"]

                recorded_prev_hash = block[3]["prev_hash"]
                prev_hash = prev_block[3]["hash"]

                if actual_hash != recorded_data_hash or recorded_prev_hash[0:4] != COMPLEXITY*"0":
                    if actual_hash != recorded_data_hash: print(f"Blockchain is invalid in block {i}! Current block hash doesn't match, expected {recorded_data_hash}, actual = {actual_hash}")
                    if recorded_prev_hash[0:4] != COMPLEXITY*"0": print(f"Blockchain is invalid in block {i}! The previous hash doesn't match, expected {prev_hash}, actual = {recorded_prev_hash}")
                else:
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