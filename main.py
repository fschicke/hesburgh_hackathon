# main.py
# Andrew Slavin

import cherrypy_cors
import cherrypy
from _whatsupp_database import _whatsupp_database
from events import eventsController as EC
from users import usersController as UC
import json


class optionsController:
	def OPTIONS(self, *args, **kwargs):
		return ""

def CORS():
	cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
	cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
	cherrypy.response.headers["Access-Control-Allow-Credentials"] = "*"

def start_service():
	dispatcher = cherrypy.dispatch.RoutesDispatcher()
	# create new whatsupp database
	wudb = _whatsupp_database() # shared across all controllers
	
	# load all data
	wudb.load_events("/home/aslavin/fschicke.github.io/events.dat")
	wudb.load_users("/home/aslavin/fschicke.github.io/users.dat")
	wudb.load_tags("/home/aslavin/fschicke.github.io/tags.dat")

	# initialize controllers
	eventsController = EC(wudb)
	usersController = UC(wudb)
	
	# HANDLERS
	# authenticate handler (uses usersController)
	dispatcher.connect('authenticate', '/authenticate/', controller=usersController, action='AUTHENTICATE', conditions=dict(method=['PUT']))
	
	# event handlers
	dispatcher.connect('put_event', '/events/:eid', controller=eventsController, action='PUT_EVENT', conditions=dict(method=['PUT']))
	dispatcher.connect('post_event', '/events/', controller=eventsController, action='POST_EVENT', conditions=dict(method=['PUT']))
	dispatcher.connect('get_events', '/events/', controller=eventsController, action='GET_EVENTS', conditions=dict(method=['GET']))
	dispatcher.connect('delete_event', '/events/:eid', controller=eventsController, action='DELETE_EVENT', conditions=dict(method=['DELETE']))
	
	# vote handler
	dispatcher.connect('vote', '/vote/:eid', controller=eventsController, action='VOTE', conditions=dict(method=['PUT']))
	
	# users handlers
	dispatcher.connect('get_user', '/users/:net_id', controller=usersController, action='GET_USER', conditions=dict(method=['GET']))
	dispatcher.connect('put_user', '/users/:net_id', controller=usersController, action='PUT_USER', conditions=dict(method=['PUT']))
	
	# match handler (uses event handler)
	dispatcher.connect('match', '/match/', controller=eventsController, action='MATCH', conditions=dict(method=['PUT']))
	
	# top5 handler
	dispatcher.connect('top5', '/top5/', controller=eventsController, action='TOP5', conditions=dict(method=['PUT']))

	# tags handler
	dispatcher.connect('tags', '/tags/', controller=eventsController, action='GET_TAGS', conditions=dict(method=['GET']))
	
	#options
	dispatcher.connect('all_match_op', '/match/', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
	
	dispatcher.connect('all_top5_op', '/top5/', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
	
	dispatcher.connect('all_tags_op', '/tags/', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
	
	dispatcher.connect('authenticate_op', '/authenticate/', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
	
	dispatcher.connect('events_key_op', '/events/:eid', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
	dispatcher.connect('events_all_op', '/events/', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
	
	dispatcher.connect('vote_key_op', '/vote/:eid', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))

	dispatcher.connect('users_key_op', '/users/:net_id', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))

	
	# create configuration, which is a dict
	conf = { 
		'global': { 
			'server.socket_host': '159.203.182.180',
			'server.socket_port': 5000
		},
		'/': {
			'request.dispatch':dispatcher,
			'tools.CORS.on'	 : True
		}
	}
	cherrypy.config.update(conf) # tells library what the configuration is
	# tell app what the configuration is
	app = cherrypy.tree.mount(None, config=conf)
	cherrypy.quickstart(app)

if __name__ == '__main__':
	cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
	start_service()
