import threading
import requests
import json
import Picker

class Github:
    def __init__(self, conf, picker):
        if not conf.github.enabled:
            return
        self._picker = picker
        self._conf = conf

        self._picker.add_category(self._conf.github.name, [])
        g = threading.Thread(target=self.github, daemon=True)
        g.start()



    def github_get(self, url):
        auth = requests.auth.HTTPBasicAuth(self._conf.github.username,
                                           self._conf.github.password)

        head = {'Accept': 'application/vnd.github.inertia-preview+json'}


        req = requests.get(url, headers=head, auth=auth)

        data = json.loads(req.text)

        for x in data:
            self._picker.add_to_category(self._conf.github.name, (x['full_name'], Picker.RED))

        if 'Link' in req.headers:
            for tok in req.headers['Link'].split(','):
                if 'next' in tok:
                    return tok.split(';')[0].replace('<', '').replace('>', '')

    def github(self):
        url = "https://api.github.com/orgs/gomspace/repos"
        while url:
            url = self.github_get(url)

class Jenkins:
    def __init__(self, conf, picker):
        self._picker = picker
        self._conf = conf
        if not conf.jenkins.enabled:
            return
        picker.add_category(conf.jenkins.name, [])
        j = threading.Thread(target=self.get_jenkins, daemon=True)
        j.start()


    def get_jenkins(self):
        if not self._conf.jenkins.url:
            return

        req = requests.get(self._conf.jenkins.url + '/api/json')

        data = json.loads(req.text)
        lst = []
        for i, j in enumerate(data['jobs']):
            self._picker.add_to_category(self._conf.jenkins.name, (j['name'], i % 5, j['url']))

class Jira:
    def __init__(self, conf, picker):
        self._picker = picker
        self._conf = conf
        if not conf.jira.enabled:
            return
        picker.add_category(conf.jira.name, [])
        j = threading.Thread(target=self.get_jira, daemon=True)
        j.start()

    def get_jira(self):
        # TODO error handling...
        if not self._conf.jira.url:
            return
        if not self._conf.jira.username:
            return
        if not self._conf.jira.password:
            return
        if not self._conf.jira.filterid:
            return
        self._auth = requests.auth.HTTPBasicAuth(self._conf.jira.username, self._conf.jira.password)
        r = requests.get(self._conf.jira.url + '/rest/api/2/filter/' + self._conf.jira.filterid, auth=self._auth)
        data = json.loads(r.text)
        searchurl = data['searchUrl']
        r = requests.get(searchurl, auth=self._auth)
        data = json.loads(r.text)
        for i in data['issues']:
            issue_name = '[%s] %s' % (i['key'], i['fields']['summary'])
            self._picker.add_to_category(self._conf.jira.name, (issue_name, 0, 'todo url'))
