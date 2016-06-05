# ScheduleCreatorNDInterface.py
# Cherrypy interface that defines web controllers for application

import cherrypy

class ScheduleCreatorNDInterface(object):

    # Controller to return index page of application
    @cherrypy.expose
    def index(self):
        return "Hello World!"