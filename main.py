# main.py
# Andrew Slavin

import cherrypy
from _whatsupp_database import _whatsupp_database
from events import eventsController
from users import usersController
import json

# create new whatsupp database
wudb = _whatsupp_database() # shared across all controllers

# load all data
wudb.load_events("/home/btrossen/fschicke.github.io/events.dat")
wudb.load_users("/home/btrossen/fschicke.github.io/users.dat")
wudb.load_votes("/home/btrossen/fschicke.github.io/votes.dat")
dispatcher = cherrypy.dispatch.RoutesDispatcher()


# create configuration, which is a dict
conf = { 'global': {'server.socket_host': '159.203.182.180',
		     'server.socket_port': 5000},
			 '/': {'request.dispatch':dispatcher}}
# initialize controllers
eventsController = eventsController(wudb)
usersController = usersController(wudb)

# HANDLERS
# authenticate handler (uses usersController)
dispatcher.connect('authenticate', '/authenticate/', controller=usersController, action='AUTHENTICATE', conditions=dict(method=['PUT']))

# event handlers
dispatcher.connect('put_event', '/events/:eid', controller=eventsController, action='PUT_EVENT', conditions=dict(method=['PUT']))
dispatcher.connect('post_event', '/events/', controller=eventsController, action='POST_EVENT', conditions=dict(method=['PUT']))
dispatcher.connect('delete_event', '/events/:eid', controller=eventsController, action='DELETE_EVENT', conditions=dict(method=['DELETE']))

# vote handler
dispatcher.connect('vote', '/vote/:eid', controller=eventsController, action='VOTE', conditions=dict(method=['PUT']))

# top 5 handler
dispatcher.connect('top5', '/top5/', controller=eventsController, action='TOP5', conditions=dict(method=['PUT']))

# users handlers
dispatcher.connect('get_user', '/users/:net_id', controller=usersController, action='GET_USER', conditions=dict(method=['GET']))
dispatcher.connect('put_user', '/users/:net_ID', controller=usersController, action='PUT_USER', conditions=dict(method=['PUT']))

# match handler (uses event handler)
dispatcher.connect('match', '/match/', controller=eventsController, action='MATCH', conditions=dict(method=['PUT']))

cherrypy.config.update(conf) # tells library what the configuration is

# tell app what the configuration is
app = cherrypy.tree.mount(None, config=conf)
cherrypy.quickstart(app)

