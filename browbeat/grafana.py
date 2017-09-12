#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging


class Grafana(object):

    def __init__(self, config):
        self.logger = logging.getLogger('browbeat.grafana')
        self.config = config
        self.cloud_name = self.config['browbeat']['cloud_name']
        self.hosts_file = self.config['ansible']['hosts']
        self.grafana_ip = self.config['grafana']['grafana_ip']
        self.grafana_port = self.config['grafana']['grafana_port']
        self.playbook = self.config['ansible']['grafana_snapshot']
        self.grafana_url = {}

    def extra_vars(self, from_ts, to_ts, result_dir, test_name):
        extra_vars = 'grafana_ip={} '.format(
            self.config['grafana']['grafana_ip'])
        extra_vars += 'grafana_port={} '.format(
            self.config['grafana']['grafana_port'])
        extra_vars += 'from={} '.format(from_ts)
        extra_vars += 'to={} '.format(to_ts)
        extra_vars += 'results_dir={}/{} '.format(result_dir, test_name)
        extra_vars += 'var_cloud={} '.format(self.cloud_name)
        if self.config['grafana']['snapshot']['snapshot_compute']:
            extra_vars += 'snapshot_compute=true '
        return extra_vars

    def grafana_urls(self):
        return self.grafana_url

    def create_grafana_urls(self, time):
        if 'grafana' in self.config and self.config['grafana']['enabled']:
            from_ts = time['from_ts']
            to_ts = time['to_ts']
            url = 'http://{}:{}/dashboard/db/'.format(
                self.grafana_ip, self.grafana_port)
            for dashboard in self.config['grafana']['dashboards']:
                self.grafana_url[dashboard] = '{}{}?from={}&to={}&var-Cloud={}'.format(
                    url,
                    dashboard,
                    from_ts,
                    to_ts,
                    self.cloud_name)

    def print_dashboard_url(self, test_name):
        for dashboard in self.grafana_url:
            self.logger.debug(
                '{} - Grafana Dashboard {} URL: {}'.format(
                    test_name,
                    dashboard,
                    self.grafana_url[dashboard]))