from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time
import os

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

walletA = WalletExplorer.WalletExplorer (wallet_file='test2.wallet')
A = ForumManager.ForumManager (consMan, wallet=walletA)
walletB = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
B = ForumManager.ForumManager (consMan, wallet=walletB)

try:

	postidA = A.registerPost ('hello post', 'post test')
	
	#Prima di procedere con il commento dobbiamo aspettare che il dababase ci restituisca il valore 	dell'id postidA
	controllo = True
	while controllo:
		os.system ('clear')
		print('Post A non ancora creato, Loading.')
		time.sleep (1)
		os.system ('clear')
		print('Post A non ancora creato, Loading..')
		time.sleep (1)
		os.system ('clear')
		print('Post A non ancora creato, Loading...')
		time.sleep (1)



		v = A.getListPost ()
		for x in v:
			if x['postid'] == postidA:
				controllo = False
	print('Post A creato')

	walletA = WalletExplorer.WalletExplorer (wallet_file='test2.wallet')
	A = ForumManager.ForumManager (consMan, wallet=walletA)
	comidA = A.registerCom (postidA , 'this is a comment')
	
	walletB = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
	postidB = B.registerPost ('hello post 2', 'post test 2')

	#Non c'è bisogno di aspettare perchè il postidA è già stato creato, e non dobbiamo aspettare il 	postidB
	walletB = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
	B = ForumManager.ForumManager (consMan, wallet=walletB)
	comidB = B.registerCom (postidA , 'this is a comment of B')
	

	#Continua a ciclare perchè non è detto che i commenti comidA e conidB siano già stati registrati, 		quindi aspettare, fimchè non compaiono tutti gli elementi:
	while True:
		os.system ('clear')
		#Stampe dei degli ID
		print ('Post A: ', postidA)
		print ('Comm A: ', comidA)
		print ('Post B: ', postidB)
		print ('Comm B: ', comidB)
		
		print ('\n','--FORUM BASIC--')
		#Stampa titolo e testo del post A
		v = A.getListPost ()
		for x in v:
			if x['postid'] == postidA:
				print ('\n','Post A:  ',x['title'],'\t',x['body'])
				#Stampa commenti relativi al post A se c'è ne sono		
				v = B.getListCom (postidA)
				noCom=True
				for x in v:
					noCom=False
					print ('\t','id commento(',x['comid'],')','\t','testo:  ',x['body'])
				#se il Post non ha commenti stampa un messaggio che ti avisa
				if noCom :
					print('\t','IL POSTO NON È STATO ANCORA COMMENTATO')
			
		#Stampa titolo e testo del post B
		v = A.getListPost ()
		for x in v:
			if x['postid'] == postidB:
				print ('\n','Post B:  ',x['title'],'\t',x['body'])
				#Stampa commenti relativi al post B se c'è ne sono		
				v = B.getListCom (postidB)
				noCom=True
				for x in v:
					noCom=False
					print ('\t','id commento(',x['comid'],')','\t','testo:  ',x['body'])						
				#se il Post non ha commenti stampa un messaggio che ti avisa
				if noCom :
					print('\t','IL POSTO NON È STATO ANCORA COMMENTATO')
		
		time.sleep (10)

except:
	print ('Error.')
	
	
