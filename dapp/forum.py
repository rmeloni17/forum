import logging

from contractvmd import dapp, config, proto
from contractvmd.chain import message

logger = logging.getLogger(config.APP_NAME)

class ForumProto:
	DAPP_CODE = [ 0x57, 0x58 ]
	METHOD_POST = 0x01
	METHOD_MSG  = 0x02
	METHOD_LIST = [METHOD_POST,METHOD_MSG]
	
class ForumMessage (message.Message):
	def registerpost (sid, title, body):
		m = ForumMessage ()
		m.PostID = sid
		m.Title = title
		m.Body = body
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_POST
		return m

	def registercom (comid, hashpost, body):
		m = ForumMessage ()
		m.ComID = comid
		m.HashPost = hashpost
		m.Body = body
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_MSG
		return m


	def toJSON (self):
		data = super (ForumMessage, self).toJSON ()

		if self.Method == ForumProto.METHOD_POST:
			data['postid'] = self.PostID
			data['body'] = self.Body
			data['title'] = self.Title
		else:
			if self.Method == ForumProto.METHOD_MSG:
				data['comid'] = self.ComID
				data['body'] = self.Body
				data['hashpost'] = self.HashPost
			else:
				return None

		return data


class ForumCore (dapp.Core):
	def __init__ (self, chain, database):
		database.init ('post', [])
		database.init ('com', [])
		super (ForumCore, self).__init__ (chain, database)

	#registra un post, inserendo un id, un titolo e il body		
	def registerpost (self, postid, title, body):
		return self.database.listappend ('post', {'postid': postid, 'title': title, 'body': body})
			
	#registra un commento, inserendo un id, l'id del post a cui appartiene e il body del commento
	def registercom (self, comid, hashpost, body):
		v = ForumCore.getlistpost(self)
		for x in v:
			if x['postid'] == hashpost:
				return self.database.listappend ('com', {'comid': comid, 'hashpost': hashpost, 'body': body})
		
		
	#restituisce tutti i post
	def getlistpost (self):
		return self.database.get ('post')

	#dato l'id di un post, restiuisce tutti i commenti relativi al post scelto
	def getlistcom (self,postid):
		v= self.database.get ('com')
		c=[]		
		for x in v:
			if x['hashpost'] == postid:
				c.append(x)		
		return c


class ForumAPI (dapp.API):
	def __init__ (self, core, dht, api):
		self.api = api
		rpcmethods = {}

		rpcmethods["getlistpost"] = {
			"call": self.method_getlistpost,
			"help": {"args": [], "return": {}}
		}

		rpcmethods["getlistcom"] = {
			"call": self.method_getlistcom,
			"help": {"args": ["hashpost"], "return": {}}
		}

		rpcmethods["registerpost"] = {
			"call": self.method_registerpost,
			"help": {"args": ["postid", "title", "body"], "return": {}}
		}

		rpcmethods["registercom"] = {
			"call": self.method_registercom,
			"help": {"args": ["comid", "hashpost", "body"], "return": {}}
		}

		errors = { }

		super (ForumAPI, self).__init__(core, dht, rpcmethods, errors)

	def method_getlistpost (self):
		return self.core.getlistpost ()

	def method_getlistcom (self,postid):
		return self.core.getlistcom (postid)

	def method_registerpost (self, postid, title, body):
		msg = ForumMessage.registerpost (postid, title, body)
		return self.createTransactionResponse (msg)

	def method_registercom (self, comid, posthash, body):
		msg = ForumMessage.registercom (comid, posthash, body)
		return self.createTransactionResponse (msg)

class forum (dapp.Dapp):
	def __init__ (self, chain, db, dht, apiMaster):
		self.core = ForumCore (chain, db)
		apiprov = ForumAPI (self.core, dht, apiMaster)
		super (forum, self).__init__(ForumProto.DAPP_CODE, ForumProto.METHOD_LIST, chain, db, dht, apiprov)

	def handleMessage (self, m):
		if m.Method == ForumProto.METHOD_POST:
			logger.pluginfo ('Found new message %s: registration of %s', m.Hash, m.Data['postid'])
			self.core.registerpost (m.Hash, m.Data['title'], m.Data['body'])
		elif m.Method == ForumProto.METHOD_MSG:
			logger.pluginfo ('Found new message %s: registration of %s', m.Hash, m.Data['comid'])
			self.core.registercom (m.Hash, m.Data['hashpost'], m.Data['body'])
