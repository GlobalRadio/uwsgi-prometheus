# uWSGI Prometheus

A uWSGI stats exporter for Prometheus that integrates directly into an existing uWSGI app

# Installation

Install using `pip`:

    pip install uwsgi-prometheus

Enable the http stats endpoint in your uWSGI config: 

[https://uwsgi-docs.readthedocs.io/en/latest/StatsServer.html](https://uwsgi-docs.readthedocs.io/en/latest/StatsServer.html)

Add the following in your `uwsgi.py`:

    from prometheus_client.core import REGISTRY
    from uwsgi_prometheus.collectors import UWSGIStatsCollector

    REGISTRY.register(UWSGIStatsCollector())

The following stats will then be added to your existing metrics endpoint:

- **uwsgi_listen_queue_requests** - Number of requests in the uWSGI listen queue
- **uwsgi_request_total** - Total number of uWSGI requests across all workers  
- **uwsgi_harakiris_total** - Total number of harakiris across all workers  

# Configuration

A few configuration options are available on the collector:

- **stats_url** - The URL that uWSGI is exposing stats on `Default: http://127.0.0.1:1717`
- **timeout** - The timeout for fetching stats `Default: 2`
- **prefix** - A prefix for the exported metrics (An underscore is automatically added if specified) `Default: ''`

```
REGISTRY.register(UWSGIStatsCollector(
    stats_url='http://127.0.0.1:1717',
    timeout=2,
    prefix=''
))
```
