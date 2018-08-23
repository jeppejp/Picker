import os
import configparser

class ConfObject():
    pass

class Config(dict):

    def __init__(self):
        conf_file = os.path.expanduser('~/.config/picker/picker.conf')
        self._config = configparser.ConfigParser()

        self._config.read(conf_file)


        self.general = ConfObject()
        self.general.hjkl = self._config['general'].getboolean('hjkl', True)

        self.jenkins = ConfObject()
        self.jenkins.url = self._config['jenkins'].get('url', None)
        self.jenkins.enabled = True
        self.jenkins.name = 'Jenkins'

        self.github = ConfObject()
        self.github.enabled = True
        self.github.name = "Github"
        self.github.username = self._config['github'].get('username', '')
        self.github.password = self._config['github'].get('password', '')


if __name__ == '__main__':
    c = Config()
    print(c.general.hjkl)
