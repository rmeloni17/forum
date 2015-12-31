from libcontractvm import Wallet, ConsensusManager, DappManager

class ForumManager (DappManager.DappManager):
	def __init__ (self, consensusManager, wallet = None):
		super (ForumManager, self).__init__(consensusManager, wallet)
	#dato in imput titolo e il corpo del post, si creerà un Post, con un hash univoco come id, titolo e 		 corpo
	def registerPost (self, title, body):
		cid = self.produceTransaction ('forum.registerpost', ['id', title, body])
		return cid
	#dato in imput hash di un post esistente e un commento, si creerà un commento, con un hash univoco 		 come id, l'hash relativo al posto e body del commento
	def registerCom (self, postid, comment):
		cid = self.produceTransaction ('forum.registercom', [ 'id', postid, comment])
		return cid

	#restituisce la lista di tutti i Post
	def getListPost (self):
		return self.consensusManager.jsonConsensusCall ('forum.getlistpost', [])['result']

	#dato in imput hash di un post, restituisce la lista di tutti i commenti relativi al post
	def getListCom (self,postid):
		return self.consensusManager.jsonConsensusCall ('forum.getlistcom', [postid])['result']
