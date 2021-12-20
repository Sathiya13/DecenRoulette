# DecenRoulette
Decentralized Roulette Game on Tezos 



![image](https://user-images.githubusercontent.com/93893007/146643028-09fbb016-a557-4952-9977-9ef863032ea3.png)

### Introduction

The bestway to make money from the casioo is to own it and run it. It is my goal to provide opportunity for Tezos community to own a decentralized casino. The first dapp for the decentralised casino is the DecenRoulette (DeRo) deployed in the Tezos Hangzhounet https://hangzhou2net.tzkt.io/KT1WvRXeDDbpAMPv9D91jokSvBg7u38XNCxQ/operations/ . 

### How it works

Since transaction on the tezos blockchain are costly, most of the operation like random number generation is taken care at the JS Front end level as it would give flexibility in changing to advanced random number generation methods in future without impacting underlying smartcontract and also saving transaction costs from using oracles. Only the currency transfer from the casino to user account and vice versa are coded at the smart contract level.

#### Actors
  
  - Smart Contract
  - Players
  - Stake Holders

###### Smart Contract

Smart Contract acts as the treasury for the casino. It holds on the account balance of the players and stakeholders. Smart contract also locks staked amount for 6 month, credits staking rewards to staker account and allows to unstake after the staking period. The steking period extends another 6 months when a new stake amount is added by the stakers. So stakers can extend the staking by adding a small tez to their account. Currently there is no limit to stake or deposit.  

###### Players

Players can gamble by depositing their tezos to the smartcontract. Players bet on the numbers, colors, range ( 1-12, 13-24,25-36, 1-18, 19-36) etc all combinations similar to the live roulette . And if they win ,the pay-off also will be similar to the real casino. Current code allows players to bet only after depositing amount to the smart contract. If the player wins , the winning amount will be added to their account in smart contract.
* Next version of the code will directly check the balance of players' wallet and debit the betting amount directly from wallet . The winnings also will be directly credited to their wallet. * 

###### Stake Holders

Stake Holder act as underwriters to cover excess loss of the casino if the players winnings exceed teh balance of the smart contract. In return the Stake holders are provided with the staking rewards. Currently the staking rewards are paid out in Tezos. * Next version staking and staking rewards will happen in the casino's own currency *.   

