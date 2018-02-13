import cherrypy
import json
from settings import *


# URL structure is:
#   /key or /key/read
#   /key/write/value
#   /key/verify/value
#   /key/default
#   /all


settings = Settings()
settings.add(Setting('name', 'fred', verify=lambda x: type(x)== str))
settings.add(Setting('age', 25, verify=lambda x: type(x)== int))
settings.add(Setting('gender', 'male', verify=lambda x: x == 'male' or x =='female'))


class App(object):
    def __init__(self):
        self.settings = SettingsEngine()

    @cherrypy.expose
    def index(self):
        return open('empty.html')


@cherrypy.popargs('key')
class SettingsEngine(object):
    def __init__(self):
        self.write = Write()
        self.verify = Verify()
        self.default = Default()

    @cherrypy.expose(['read'])
    def index(self, key):
        if key == 'all':
            return str(settings)
        if key in settings.keys:
            return '{}'.format(settings.by_key(key).value)
        else:
            return '{} not found'.format(key)


@cherrypy.popargs('val')
class Write(object):
    @cherrypy.expose
    def index(self, key, val):
        if key in settings.keys:
            return '{}'.format(settings.by_key(key).write(val))
        else:
            return '{} not found'.format(key)


@cherrypy.popargs('val')
class Verify(object):
    @cherrypy.expose
    def index(self, key, val):
        if key in settings.keys:
            return '{}'.format(settings.by_key(key).verify(val))
        else:
            return '{} not found'.format(key)


class Default(object):
    @cherrypy.expose
    def index(self, key):
        if key in settings.keys:
            settings.by_key(key).default()
            return 'True'
        else:
            return '{} not found'.format(key)


if __name__ == '__main__':
    cherrypy.quickstart(App())
