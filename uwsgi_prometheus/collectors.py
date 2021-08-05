import requests

from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily


class UWSGIStatsCollector:
    def __init__(
        self,
        stats_url='http://127.0.0.1:1717',
        timeout=2,
        prefix='',
    ):
        self.stats_url = stats_url
        self.timeout = timeout
        self.prefix = '%s_' % prefix if prefix else prefix

    def collect(self):
        try:
            response = requests.get(self.stats_url, timeout=self.timeout)
            response.raise_for_status()
        except (requests.ConnectionError, requests.HTTPError):
            return

        uwsgi_stats = response.json()

        listen_queue_length = uwsgi_stats['listen_queue']
        requests_total = 0
        harakiris_total = 0
        for worker in uwsgi_stats['workers']:
            requests_total += worker['requests']
            harakiris_total += worker['harakiri_count']

        yield GaugeMetricFamily('%suwsgi_listen_queue_requests' % self.prefix, 'Number of requests in the uWSGI listen queue', value=listen_queue_length)
        yield CounterMetricFamily('%suwsgi_requests_total' % self.prefix, 'Total number of uWSGI requests', value=requests_total)
        yield CounterMetricFamily('%suwsgi_harakiris_total' % self.prefix, 'Total number of Harakiris', value=harakiris_total)
