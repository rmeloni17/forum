from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
srMan = ForumManager.ForumManager (consMan, wallet=wallet)

titl = input ('Insert the Hash Post: ')
body = input ('Insert the Body Com: ')

try:
	print ('Broadcasted:', srMan.registerCom (titl, body))
except:
	print ('Error.')
	
