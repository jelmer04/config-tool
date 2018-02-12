import cherrypy

# URL structure is:
#   /key or /key/read
#   /key/write/value
#   /key/verify/value
#   /key/default

data = {'name': 'Fred',
        'age': 25,
        'gender': 'male'}

class Setting(object):
    def __init__(self, key, title=None, text="",
                 default="", verify=lambda x: True):

        self.key = key

        if title == None:
            self.title = key
        else:
            self.title = title

        self.text = text

        self.default = ""
        self.verify = verify


class Settings(object):
    def __init__(self):
        self.settings_list = []
        self.keys = []

    def add(setting):
        self.settings_list.append(setting)
        self.keys.append(setting.key)

    def by_key(key):
        if key in self.keys:
            return self.settings_list[self.keys.index(key)]
        else:
            return None


    settings = Settings()
    settings.add(Setting('name'))
    settings.add(Setting('age'))
    settings.add(Setting('gender'))


def key_to_setting(key, setting_list):
    return filter(lambda s: s.name == key, setting_list)[0]


@cherrypy.popargs('key')
class FunctionHost(object):
    def __init__(self):
        self.write = Write()
        self.verify = Verify()
        self.default = Default()
        self.debug = Debug()

    @cherrypy.expose(['read'])
    def index(self, key):
        if key in data:
            return '{}'.format(data[key])
        else:
            return "{} not found".format(key)

@cherrypy.popargs('val')
class Write(object):
    @cherrypy.expose
    def index(self, key, val):
        if key in data:
            data[key] = val
            return 'True'
        else:
            return "{} not found".format(key)

@cherrypy.popargs('val')
class Verify(object):
    @cherrypy.expose
    def index(self, key, val):
        if key in data:
            # do some checking?
            return 'True'
        else:
            return "{} not found".format(key)

class Default(object):
    @cherrypy.expose
    def index(self, key):
        if key in data:
            data[key] = 'default'
            return 'True'
        else:
            return "{} not found".format(key)

class Debug(object):
    @cherrypy.expose
    def index(self, key):
        return '{}'.format(data)

if __name__ == '__main__':
    cherrypy.quickstart(FunctionHost())
