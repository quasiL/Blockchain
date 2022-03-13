from Blockchain import Blockchain

B = Blockchain()

B.newTransaction("John", "Stan", 16000)
B.newTransaction("Mike", "Stan", 50466)
B.newTransaction("Mike", "Matt", 12110)
B.newTransaction("Mike", "Matt", 6730)
B.newTransaction("Mike", "Stan", 50666)
B.newTransaction("Mike", "Matt", 12510)
B.newTransaction("Mike", "Matt", 670)
B.mine()
B.mine()

B.checkBlockchain()
B.validateBlockchain()

#print("Trying to change the data in blockchain:\n")
#B.blockchain[1][0]["amount"] = 999999
#B.validateBlockchain() 