from blockchain import Blockchain, Transaction

coin = Blockchain()
Trans = Transaction("address1", "address2", 100)
coin.createTransaction(Trans)
Trans = Transaction("address2", "address1", 50)
coin.createTransaction(Trans)

print('Starting the miner...')
coin.minePendingTransactions("kiko-address")

print('Balance of kiko is', coin.getBalanceOfAddress("kiko-address"))
print('Balance of address1 is', coin.getBalanceOfAddress("address1"))
print('Balance of address2 is', coin.getBalanceOfAddress("address2"))