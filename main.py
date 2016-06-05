# main.py
# Starts the cherrypy server

import os
import cherrypy
from src import ScheduleCreatorNDInterface

# Function to set up a cherrypy server for the application
def main():

    # Set up config for cherrypy server
    globalConfig = {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080
    }

    cherrypy.config.update(globalConfig)

    # Set up application level configurations
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath("./src/www")
        },
        '/static/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './src/www/js'
        },
        '/static/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './src/www/css'
        }
    }

    cherrypy.quickstart(ScheduleCreatorNDInterface.ScheduleCreatorNDInterface(), script_name='/', config=conf)

#Set up cherrypy server
if __name__ == '__main__':
    main()