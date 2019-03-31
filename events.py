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
	
	# return list of top 5 events for a week
	def TOP5(self):
		msg = json.loads(cherrypy.request.body.read().decode('utf-8'))
		date = list(msg["date"])
		retDict = self.wudb.top5(date) # dict of events indexed by eid
		parsed = []
		for key, val in retDict.items():
			entry = {}
			entry["eid"] = key
			entry["title"] = val[0]
			entry["description"] = val[1]
			entry["tags"] = val[2]
			entry["startDate"] = val[3]
			entry["endDate"] = val[4]
			entry["eventType"] = val[5]
			entry["maxAttendance"] = val[6]
			entry["location"] = val[7]
			parsed.append(entry)
		return json.dumps({"result": parsed})

	def GET_TAGS(self):
		ret =  self.wudb.get_tags()
		return json.dumps({"result":ret})
