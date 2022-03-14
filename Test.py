from Blockchain import Blockchain

B = Blockchain()

B.createWallet("John", 100)
B.createWallet("Mike", 100)
B.createWallet("Stan")
B.createWallet("Matt")

B.newTransaction("John", "Stan", 10)
B.newTransaction("Mike", "Stan", 20)
B.newTransaction("Mike", "Matt", 20)
B.newTransaction("Mike", "Matt", 30)
#B.newTransaction("Mike", "Stan", 50666)
#B.newTransaction("Mike", "Matt", 12510)
#B.newTransaction("Mike", "Matt", 670)
#B.newTransaction("Mike", "Matt", 6570)
#B.mine()
B.mine()

B.checkBlockchain()
B.validateBlockchain() 

print(B.getBalance("John"))
print(B.getBalance("Mike"))
print(B.getBalance("Stan"))
print(B.getBalance("Matt"))


#print("Trying to change the data in blockchain:\n")
#B.blockchain[1][2]["amount"] = 999999
#B.validateBlockchain() 
#B.checkBlockchain()