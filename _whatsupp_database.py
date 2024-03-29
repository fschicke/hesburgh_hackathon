# _whatsupp_database.py
# Andrew Slavin

import requests
import json
import operator

class _whatsupp_database:
	def __init__(self):
		self.events = {} # uses event ID as key
		self.users = {} # uses profiel ID as a key
		self.votes = {}
		self.tags = []

	# opens events file and reads all data into the events dictionary
	def load_events(self, events_file):
		# clear existing dict
		self.events = {}
		# load in new events
		inData = open(events_file, "r")
		for line in inData.readlines():
			separated = line.split("::")
			eid = int(separated[0])
			title = separated[1]
			description = separated[2]
			tags = [x.strip() for x in separated[3].split(',')]
			startDate = [x.strip() for x in separated[4].split(',')]
			endDate = [x.strip() for x in separated[5].split(',')]
			startDate = [int(x) for x in startDate]
			endDate = [int(x) for x in endDate]
			eventType = int(separated[6])
			maxAttendance = int(separated[7])
			location = separated[8].strip('\n')
			self.events[int(separated[0])] = [title, description, tags, startDate, endDate, eventType, maxAttendance, location]
	
	def load_users(self, user_file):
		# clear existing dict
		self.users = {}
		# load new users
		inData = open(user_file, "r")
		for line in inData.readlines():
			separated = line.split("::")
			admin = int(separated[1])
			email = separated[2]
			password = separated[3]
			fName = separated[4]
			lName = separated[5]
			tags = [x.strip() for x in separated[6].split(',')]
			classNum = int(separated[7])
			events = [x.strip() for x in separated[8].strip(' \t\n').split(',')]
			events = [int(x) for x in events]
			self.users[separated[0]] = [admin, email, password, fName, lName, tags, classNum, events]
	
	# load in dummy votes
	def load_votes(self, votes_file):
		self.votes = {}
		inData = open(votes_file, "r")
		for line in inData.readlines():
			separated = line.split("::")
			self.votes[int(separated[0])] = int(separated[1].strip('\n'))
	
	# load in all tags
	def load_tags(self, tags_file):
		self.tags = []
		inData = open(tags_file, "r")
		for line in inData.readlines():
			self.tags.append(line.strip(' \t\n'))

	# return list of all tags
	def get_tags(self):
		self.tags.sort()
		return self.tags

	# return true if password/username match up
	def authenticate(self, username, password):
		if self.users[username][2] == password:
			return True
		else:
			return False
	
	# create new or change existing event
	def add_event(self, eventList):
		# find next eid for event
		eventId = 1
		while (eventId in self.events.keys()):
			eventId+=1
		self.events[eventId] = eventList
		print(self.events)
		return eventId
	
	def edit_event(self, eid, eventList):
		if eid in self.events.keys():
			self.events[eid] = eventList
			return 1
		else:
			return 0 # failure
	
	# remove event from dictionary
	def delete_event(self, eventID):
		if eventID in self.events.keys():
			self.events.pop(eventID, None)
			votes[eventID] = 0
			return 1
		else:
			return 0 # failure
	
	# return all user info for a netID
	def get_user(self, netID):
		if netID in self.users.keys():
			return self.users[netID]
		else:
			return None

	# add or edit user
	def set_user(self, netID, userList):
		self.users[netID] = userList
	
	# find matches on date for that person
	def match(self, date, netID):
		matches = []
		# iterate through every event
		for eid in self.events.keys():
			# check if date matches
			if self.events[eid][3][0:3] == date:
				# iterate through tags in that event
				for tag in self.events[eid][2]:
					# check if that tag matches user
					if tag in self.users[netID][5]:
						matches.append(eid)
		return matches
	
	# set a vote for event by its ID
	def vote(self, eid):
		if eid in self.votes.keys():
			self.votes[eid] += 1
		else:
			self.votes[eid] = 1

	# return dict of top 5 events after date indexed by eid
	def top5(self, date):
		sortedVotes = sorted(self.votes.items(), key=operator.itemgetter(1))
		counter = 0
		retDict = {} # list of events
		sortedVotes.reverse()
		for vote in sortedVotes:
			eventDate = self.events[vote[0]][3]
			if (eventDate[0] == date[0] and eventDate[1] == date[1] and eventDate[2]-7 < date[2] and eventDate[2] >= date[2]) or (eventDate[0] == date[0] and eventDate[1]-1 == date[1] and eventDate[2] < 7):
				counter += 1
				retDict[vote[1]] = self.events[vote[0]]
			if counter == 5:
				break
		return retDict
	
	# return all events
	def get_events(self):
		return self.events
