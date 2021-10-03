import hashlib
import datetime

class Transaction:
    fromAddress = ''
    toAddress = ''
    amount = None
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
    
    def getFromAddress(self):
        return self.fromAddress
    
    def getToAddress(self):
        return self.toAddress

class Block:
    timestamp = None
    previousHash = None
    hash = None
    nonce = None
    transactions = None

    def __init__(self, timestamp, transactions, previousHash = ''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.hash = self.calculateHash()
        self.nonce = 0

    def calculateHash(self):
        h = hashlib.sha256()
        h.update(
            str(self.previousHash).encode("utf-8") +
            str(self.timestamp).encode("utf-8") +
            str(self.transactions).encode("utf-8") +
            str(self.nonce).encode("utf-8")
        )
        return h.hexdigest()
    
    def getTransactions(self):
        return self.transactions
    
    def getHash(self):
        return self.hash

    def setHash(self, hash):
        self.hash = hash
    
    def setPrevHash(self, hash):
        self.previousHash = hash

    def getPrevHash(self):
        return self.previousHash

    def getInfo(self):
        return "index: %s | timestamp: %s | data: %s | previousHash: %s | hash: %s" %(self.index, self.timestamp, self.data, self.previousHash, self.hash) 

    def mineBlock(self, difficulty):
        num = ""
        l = ["0" for i in range(difficulty)]
        #convert list to string
        for ele in l:
            num += ele

        while(self.hash[0:difficulty] != num):
            self.nonce += 1
            self.hash = self.calculateHash()
        print("Block mined: ", self.hash)

class Blockchain:
    chain = []
    difficulty = 0
    pendingTransactions = []
    miningRewardAddress = None
    miningReward = 0

    def __init__(self):
        self.chain.append(self.createGenesisBlock())
        self.difficulty = 5
        self.pendingTransaction = []
        self.miningReward = 100

    def createGenesisBlock(self):
        return Block(datetime.datetime.now(), [], 0x0)

    def getLatestBlock(self):
        return self.chain[len(self.chain) - 1]

    def minePendingTransactions(self, miningRewardAddress):
        block = Block(datetime.datetime.now(), self.pendingTransactions, self.getLatestBlock().getHash())
        block.mineBlock(self.difficulty)

        print('Block successfully mined!')
        self.chain.append(block)
        self.pendingTransactions.append(
            Transaction('', miningRewardAddress, self.miningReward)
        )

    def createTransaction(self, Transaction):
        self.pendingTransactions.append(Transaction)

    def getBalanceOfAddress(self, address):
        balance = 0
        for block in self.chain:
            for trans in block.getTransactions():
                if trans.getFromAddress() == address:
                    balance -= trans.amount
                if trans.getToAddress() == address:
                    balance += trans.amount
        return balance

    def getChain(self):
        return self.chain

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            CURRENTBLOCK = self.chain[i]
            PREVIOUSBLOCK = self.chain[i - 1]

            if CURRENTBLOCK.getHash() != CURRENTBLOCK.calculateHash():
                return False
            if CURRENTBLOCK.getPrevHash() != PREVIOUSBLOCK.getHash():
                return False
        return True