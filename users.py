# users.py
# Andrew Slavin 

import json
import cherrypy

# class users controller and all the handlers that go with it
class usersController:

	def __init__(self, wudb):
		self.wudb = wudb
	
	# return success if netid/passwd are correct
	def AUTHENTICATE(self):
		msg = json.loads(cherrypy.request.body.read().decode('utf-8'))
		if self.wudb.authenticate(msg["netID"], msg["password"]): # passed
			return json.dumps({"result": "success"})
		else:
			return json.dumps({"result": "failure"})
	
	# return all data for a user
	def GET_USER(self, net_id):
		user = self.wudb.get_user(net_id)
		if user == None: # couldn't find user
			return json.dumps({"result": "failure"})
		else: # create json to send
			ret = {}
			ret["netid"] = net_id
			ret["admin"] = user[0]
			ret["email"] = user[1]
			ret["password"] = user[2]
			ret["fName"] = user[3]
			ret["lName"] = user[4]
			ret["tags"] = user[5]
			ret["classNum"] = user[6]
			ret["events"] = user[7]
			return json.dumps({"result": "success", "user": ret})
			
	
	# edit existing user
	def PUT_USER(self, net_ID):
		msg = json.loads(cherrypy.request.body.read().decode('utf-8'))
		userList = []
		userList.append(msg["admin"])
		userList.append(msg["email"])
		userList.append(msg["password"])
		userList.append(msg["fName"])
		userList.append(msg["lName"])
		userList.append(list(msg["tags"]))
		userList.append(int(msg["classNum"]))
		userList.append(list(msg["events"]))
		self.wudb.set_user(net_ID, userList)
		return json.dumps({"result": "success"})
		
