import smartpy as sp

FA2 = sp.io.import_script_from_url("https://smartpy.io/dev/templates/FA2.py")

class Token(FA2.FA2):
    pass

class DeRo(sp.Contract):
    def __init__ (self,admin, token):
        self.init (
            admin = admin,
            tokenAddress = token,
            stakeRegister = sp.map(tkey = sp.TAddress, tvalue = sp.TRecord (stakedAmt = sp.TMutez ,
                                                                             unlockDate = sp.TTimestamp)),
                                                                             
            playerBook =  sp.map(tkey = sp.TAddress, tvalue = sp.TRecord(depositAmt = sp.TNat, earnings = sp.TMutez)),

            treasury = sp.record(totalStaked = sp.mutez(0), 
                                   totalDeposits = sp.mutez(0)),
        )

    
    @sp.entry_point
    def addTokenAddress(self, params):
        sp.verify(sp.sender == self.data.admin)
        self.data.tokenAddress = params.tokenContract
    
    @sp.entry_point
    def addStake(self):

        sp.if self.data.stakeRegister.contains(sp.sender):
            self.data.stakeRegister[sp.sender].stakedAmt = self.data.stakeRegister[sp.sender].stakedAmt + sp.amount
            self.data.stakeRegister[sp.sender].unlockDate = sp.now.add_days(90)
        sp.else:
            self.data.stakeRegister[sp.sender] = sp.record(stakedAmt = sp.amount, unlockDate = sp.now.add_days(90))
        
       
        self.data.treasury.totalStaked = self.data.treasury.totalStaked + sp.amount


    @sp.entry_point
    def unStake(self, amount):

        sp.verify(self.data.stakeRegister.contains(sp.sender), "Invalid User")
        sp.verify(self.data.stakeRegister[sp.sender].unlockDate < sp.now, "Staking period not yet over")
        sp.verify(self.data.stakeRegister[sp.sender].stakedAmt >= sp.utils.nat_to_mutez(amount), "Invalid Amount")

        sp.send(sp.sender, sp.utils.nat_to_mutez(amount))
        self.data.treasury.totalStaked = self.data.treasury.totalStaked - sp.utils.nat_to_mutez(amount)

    @sp.entry_point
    def deposit(self):

        sp.if self.data.playerBook.contains(sp.sender):
            self.data.playerBook[sp.sender].depositAmt = self.data.playerBook[sp.sender].depositAmt + sp.utils.mutez_to_nat(sp.amount)
        sp.else:
            self.data.playerBook[sp.sender] = sp.record (depositAmt = sp.utils.mutez_to_nat(sp.amount) ,  earnings= sp.mutez(0))
        
        self.data.treasury.totalDeposits = self.data.treasury.totalDeposits + sp.amount

    
    @sp.entry_point
    def withdraw(self, amount):

        sp.verify(self.data.playerBook.contains(sp.sender), "Invalid User")
        sp.verify(self.data.playerBook[sp.sender].depositAmt >= amount, "Invalid Amount")
        self.data.playerBook[sp.sender].depositAmt = abs(self.data.playerBook[sp.sender].depositAmt - amount)
        sp.send(sp.sender, sp.utils.nat_to_mutez(amount))
        self.data.treasury.totalDeposits = self.data.treasury.totalDeposits - sp.utils.nat_to_mutez(amount) 

    @sp.entry_point
    def betting(self, amount):

        sp.verify( amount < self.data.playerBook[sp.sender].depositAmt , "Invalid Amount")
        self.data.playerBook[sp.sender].depositAmt = abs(self.data.playerBook[sp.sender].depositAmt - amount)
        self.data.treasury.totalDeposits = self.data.treasury.totalDeposits + sp.utils.nat_to_mutez(amount)

    @sp.entry_point
    def winnings(self, amount):

        self.data.playerBook[sp.sender].depositAmt = self.data.playerBook[sp.sender].depositAmt + amount
        self.data.treasury.totalDeposits = self.data.treasury.totalDeposits - sp.utils.nat_to_mutez(amount)



       


    @sp.entry_point
    def mintToken( self):


        b      = sp.pack("Decen Roulette Token")
        enID = sp.slice(b, 6, sp.as_nat(sp.len(b) - 6)).open_some()

        c      = sp.pack("DeRo")
        enSymbol  = sp.slice(c, 6, sp.as_nat(sp.len(c) - 6)).open_some()
        
        tokenMetadata = sp.map(l = {
            # Remember that michelson wants map already in ordered
            "decimals" : sp.utils.bytes_of_string("%d" % 0),
            "name"     : enID,
            "symbol"   : enSymbol
        })
        self.mintNewToken(clientAddress  = sp.sender,
                          tokenId        = 1,
                          tokenAmount    = 1,
                          tokenMetadata  = tokenMetadata)
    
    
    def mintNewToken(self, clientAddress, tokenId, tokenAmount, tokenMetadata):
        
        datatype   = sp.TRecord(address = sp.TAddress,
                               token_id = sp.TNat,
                               amount   = sp.TNat,
                               metadata = sp.TMap(sp.TString, sp.TBytes))
        
        tContract  = sp.contract(datatype, self.data.tokenAddress, "mint").open_some()

        params     = sp.record(address  = clientAddress,
                             token_id   = tokenId,
                             amount     = tokenAmount,
                             metadata   = tokenMetadata)
        sp.transfer(params, sp.mutez(0), tContract)


            
    



        

    
@sp.add_test(name = "Decen Roulette")
def test():
    scenario = sp.test_scenario()
    admin = sp.address('tz1hB4mef2jyR5XF1BNhvkgisLXepuGqUBqf')
    
    alice  = sp.test_account('alice')
    bob    = sp.test_account('bob')
    claire = sp.test_account('claire')
    dave   = sp.test_account('dave')
    eve    = sp.test_account('eve')
    flur   = sp.test_account('flur')


    token = Token(FA2.FA2_config(assume_consecutive_token_ids = False), admin = admin, metadata = sp.big_map({"": sp.utils.bytes_of_string("tezos-storage:content"),"content": sp.utils.bytes_of_string("""{"name" : "Decen Roulette", "version" : "01"}""")}))
    scenario += token
    tr       = DeRo(admin=admin, token=token.address)
    scenario += tr

    scenario += tr.addStake().run(sender = alice.address, amount = sp.mutez(5000000))
    scenario += tr.addStake().run(sender = bob.address, amount = sp.mutez(10000000))
    scenario += tr.addStake().run(sender = claire.address, amount = sp.mutez(24000000))

    scenario += tr.unStake(1000000).run(sender = alice.address)
    scenario += tr.unStake(1000000).run(sender = alice.address)

    scenario += tr.deposit().run(sender = alice.address, amount = sp.mutez(5000000))
    scenario += tr.deposit().run(sender = bob.address, amount = sp.mutez(10000000))
    scenario += tr.deposit().run(sender = claire.address, amount = sp.mutez(24000000))

    scenario += tr.withdraw(1000000).run(sender = alice.address)
    scenario += tr.withdraw(1000000).run(sender = alice.address)


    scenario += tr.betting(1000000).run(sender = alice.address)
    scenario += tr.betting(2000000).run(sender = bob.address)

    scenario += tr.winnings(2000000).run(sender = alice.address)
    scenario += tr.winnings(3000000).run(sender = bob.address)






        



    

        


            


