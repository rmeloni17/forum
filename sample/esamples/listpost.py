from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time
import os

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
srMan = ForumManager.ForumManager (consMan, wallet=wallet)

while True:
	os.system ('clear')
	print ('List Post:')
	v = srMan.getListPost ()
	for x in v:
		st= print ('\t',x['postid'],'\t',x['title'],'\t',x['body'])
	time.sleep (5)
	
