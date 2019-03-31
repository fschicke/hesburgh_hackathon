# events.py
# Andrew Slavin 

import json
import cherrypy

# class events controller and all the handlers that go with it
class eventsController:

	def __init__(self, wudb):
		self.wudb = wudb
	
	def POST_EVENT(self):
		msg = json.loads(cherrypy.request.body.read().decode('utf-8'))
		eventList = []
		eventList.append(msg["title"])
		eventList.append(msg["description"])
		eventList.append(list(msg["tags"]))
		eventList.append(list(msg["startDate"]))
		eventList.append(list(msg["endDate"]))
		eventList.append(msg["eventType"])
		eventList.append(msg["maxAttendance"])
		eventList.append(msg["location"])
		# set new event and get its ID
		eid = self.wudb.add_event(eventList)
		return json.dumps({"result": "success", "eid": eid})
	
	def PUT_EVENT(self, eid):
		eid = int(eid)
		msg = json.loads(cherrypy.request.body.read().decode('utf-8'))
		eventList = []
		eventList.append(msg["title"])
		eventList.append(msg["description"])
		eventList.append(list(msg["tags"]))
		eventList.append(list(msg["startDate"]))
		eventList.append(list(msg["endDate"]))
		eventList.append(msg["eventType"])
		eventList.append(msg["maxAttendance"])
		eventList.append(msg["location"])
		# set new event and get its ID
		retVal = self.wudb.edit_event(eid, eventList)
		if retVal == 1:
			return json.dumps({"result": "success"})
		else:
			return json.dumps({"result": "failure"})
	
	def DELETE_EVENT(self, eid):
		eid = int(eid)
		retVal = self.wudb.delete_event(eid)
		if retVal == 1:
			return json.dumps({"result": "success"})
		else:
			return json.dumps({"result": "failure"})
	
	# return list of matching eids
	def MATCH(self):
		msg = json.loads(cherrypy.request.body.read().decode('utf-8'))
		matches = self.wudb.match(msg["date"], msg["netID"])
		return json.dumps({"matches": matches})
	
	# send a vote for an event
	def VOTE(self, eid):
		eid = int(eid)
		self.wudb.vote(eid)
		return json.dumps({"result": "success"})
