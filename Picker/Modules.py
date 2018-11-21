import threading
import requests
import json
import Picker


class Github:
    def __init__(self, conf, picker):
        self._picker = picker
        self._conf = conf

        self._picker.add_category(self._conf.name, [])
        g = threading.Thread(target=self.github, daemon=True)
        g.start()

    def github_get(self, url):
        auth = requests.auth.HTTPBasicAuth(self._conf['username'],
                                           self._conf['password'])

        head = {'Accept': 'application/vnd.github.inertia-preview+json'}

        req = requests.get(url, headers=head, auth=auth)

        data = json.loads(req.text)

        for x in data:
            e_name = '[%s] %s' % (self._conf.name, x['full_name'])
            self._picker.add_to_category(self._conf.name, (e_name, Picker.NOCOL, x['html_url']))

        if 'Link' in req.headers:
            for tok in req.headers['Link'].split(','):
                if 'next' in tok:
                    return tok.split(';')[0].replace('<', '').replace('>', '')

    def github(self):
        url = "https://api.github.com/orgs/%s/repos" % self._conf['org']
        while url:
            url = self.github_get(url)


class Jenkins:
    def __init__(self, conf, picker):
        self._picker = picker
        self._conf = conf
        picker.add_category(conf.name, [])
        j = threading.Thread(target=self.get_jenkins, daemon=True)
        j.start()

    def get_jenkins(self):
        req = requests.get(self._conf['url'] + '/api/json')

        data = json.loads(req.text)
        lst = []
        for i, j in enumerate(data['jobs']):
            e_name = '[%s] %s' % (self._conf.name, j['name'])
            self._picker.add_to_category(self._conf.name, (e_name, Picker.NOCOL, j['url']))


class Jira:
    def __init__(self, conf, picker):
        self._picker = picker
        self._conf = conf
        picker.add_category(self._conf.name, [])
        j = threading.Thread(target=self.get_jira, daemon=True)
        j.start()

    def get_jira(self):
        # TODO error handling...
        self._auth = requests.auth.HTTPBasicAuth(self._conf['username'], self._conf['password'])
        r = requests.get(self._conf['url'] + '/rest/api/2/filter/' + self._conf['filterid'], auth=self._auth)
        data = json.loads(r.text)
        searchurl = data['searchUrl']
        r = requests.get(searchurl, auth=self._auth)
        data = json.loads(r.text)
        for i in data['issues']:
            issue_name = '[%s] %s' % (i['key'], i['fields']['summary'])
            issue_url = '%s/browse/%s' % (self._conf['url'], i['key'])
            e_name = '[%s] %s' % (self._conf.name, issue_name)
            self._picker.add_to_category(self._conf.name, (e_name, 0, issue_url))
