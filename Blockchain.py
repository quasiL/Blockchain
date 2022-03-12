import hashlib
import json

class Blockchain:
    def __init__(self):
        self.blockchain = [
            [{
                "from": "",
                "to": "",
                "amount": 0.0
            }, {}, {}, {"hash": "0000"}]
        ]
        self.stack = []
    

    def newTransaction(self, fromUser, toUser, amount):
        transaction = {
            "from": fromUser,
            "to": toUser,
            "amount": amount,
        }
        self.stack.append(transaction)

    def dataToHash(self, data):
        json_data = json.dumps(data, sort_keys = True)
        binary_data = json_data.encode()
        return hashlib.sha256(binary_data).hexdigest()[:10]

    # число которое нужно подобрать чтобы хэш начинался с 0
    def isValidProof(self, block, proof):
        block_copy = block.copy()
        block_copy.append([{"proof": proof}]) 
        self.hash = self.dataToHash(block_copy)
        #is_valid_hash = hash[0:2] == "00"
        #if is_valid_hash: 
            #print(hash)
            #print(proof)
        return self.hash[0:4] == "0000"

    #намайнить число такое чтобы добавив его к блоку хэш начинался с 00
    def mineProofOfWork(self, block):
        proof = 0
        while not self.isValidProof(block, proof):
            proof += 1
        return proof

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
            
    def validate_blockchain(self):
        prev_block = None

        for block in self.blockchain:
            if prev_block:
                actual_hash = self.dataToHash(block[0:3])
                recorded_data_hash = block[3]["data_hash"]

                recorded_prev_hash = block[3]["prev_hash"]

                if actual_hash != recorded_data_hash or recorded_prev_hash[0:4] != "0000":
                    print(f"Blockchain is invalid, expected {recorded_data_hash}, actual = {actual_hash}")
                else:
                    print(f"Valid hash {actual_hash}")

            prev_block = block        

    def checkBlockchain(self):
        i = 0
        for block in self.blockchain:
            print(f"Block № {i}")
            for transaction in block:
                print(transaction)
            print("\n")
            i += 1

B = Blockchain()
B.newTransaction("Vasya", "Petya", 16000)
B.newTransaction("Mike", "Petya", 50466)
B.newTransaction("Mike", "Kolya", 12110)
B.newTransaction("Mike", "Kolya", 6730)
B.newTransaction("Mike", "Petya", 50666)
B.newTransaction("Mike", "Kolya", 12510)
B.newTransaction("Mike", "Kolya", 670)
B.mine()
B.mine()

B.checkBlockchain()
B.validate_blockchain()
#B.blockchain[1][0]["amount"] = 999999
#B.validate_blockchain()

def dataToHash(data):
    json_data = json.dumps(data, sort_keys = True)
    binary_data = json_data.encode()
    return hashlib.sha256(binary_data).hexdigest()[:10]



# число которое нужно подобрать чтобы хэш начинался с 0
def isValidProof(block, proof):
    block_copy = block.copy()
    block_copy["proof"] = proof
    hash = dataToHash(block_copy)
    is_valid_hash = hash[0:2] == "00"
    #if is_valid_hash: 
        #print(hash)
        #print(proof)
    return hash[0:2] == "00"

#намайнить число такое чтобы добавив его к блоку хэш начинался с 00
def mineProofOfWork(block):
    proof = 0
    while not isValidProof(block, proof):
        proof += 1
    return proof

def addNewBlock(account_from, account_to, amount):
    prev_block = blockchain[-1]
    prev_hash = dataToHash(prev_block)
    proof = mineProofOfWork(prev_block)
    block = {
        "from": account_from,
        "to": account_to,
        "amount": amount,
        "prev_hash": prev_hash,
        "proof": proof  
    }
    blockchain.append(block)

def validate_blockchain():
    prev_block = None

    for block in blockchain:
        if prev_block:
            actual_prev_hash = dataToHash(prev_block)
            recorded_prev_hash = block["prev_hash"]
            recorded_prev_proof = block["proof"]

            if actual_prev_hash != recorded_prev_hash or not isValidProof(prev_block, recorded_prev_proof):
                print(f"Blockchain is invalid, expected {recorded_prev_hash}, actual = {actual_prev_hash}")
            else:
                print(f"Valid hash {actual_prev_hash}")

        prev_block = block


#addNewBlock("Mike", "Vasya", 2000)
#addNewBlock("Mike", "Petya", 50)
#addNewBlock("Mike", "Kolya", 120)
#addNewBlock("Mike", "Nastya", 88000)

#print(blockchain)

#addNewBlock("Vasya", "Petya", 1000)
#addNewBlock("Petya", "Nastya", 500)
#addNewBlock("Petya", "Kolya", 500)

#print(blockchain)

#validate_blockchain()

#print("\n")

#blockchain[5]["ammount"] = 9999999

#validate_blockchain()

""" #hack
block = 5
amount = blockchain[block]["amount"]
expected_hash = blockchain[block+1]["prev_hash"] 

hash = ""

while hash != expected_hash:
    amount += 1
    blockchain[block]["amount"] = amount
    hash = dataToHash(blockchain[block])

print(f"New amount = {amount}")
validate_blockchain()
print(blockchain) """



#mineProofOfWork(blockchain[5])