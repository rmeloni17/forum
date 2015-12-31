from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time
import os

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
srMan = ForumManager.ForumManager (consMan, wallet=wallet)

postid = input ('Insert IDPost: ')
while True:
	os.system ('clear')
	print ('List Com:')
	v = srMan.getListCom (postid)
	for x in v:
		print ('\t',x['comid'],'\t',x['hashpost'],'\t',x['body'])
	time.sleep (5)
