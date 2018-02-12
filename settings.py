class Setting(object):
    def __init__(self, key, value, title=None, text="",
                 default=None, verify=lambda x: True):

        self.key = key
        self.value = value

        if title == None:
            self.title = key
        else:
            self.title = title

        self.text = text

        if default == None:
            self.default = value
        else:
            self._default = default

        self._verify = verify

    def default(self):
        self.value = self._default

    def verify(self, value):
        try:
            value =  type(self.value)(value)
        except (TypeError, ValueError) as e:
            return False

        return self._verify(value)

    def write(self, value):
        try:
            value =  type(self.value)(value)
        except (TypeError, ValueError) as e:
            return False

        if self._verify(value):
            self.value = value
            return True
        else:
            return False


class Settings(object):
    def __init__(self):
        self.settings_list = []
        self.keys = []

    def add(self, setting):
        self.settings_list.append(setting)
        self.keys.append(setting.key)

    def by_key(self, key):
        if key in self.keys:
            return self.settings_list[self.keys.index(key)]
        else:
            return None

    def __str__(self):
        string = ''
        for s in self.settings_list:
            string = string + '{}: {}\n'.format(s.key, s.value)
        return string
