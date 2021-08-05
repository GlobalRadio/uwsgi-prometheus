import pytest

from uwsgi_prometheus.collectors import UWSGIStatsCollector


@pytest.fixture
def mock_uwsgi_stats(mocker):
    response = mocker.Mock(status_code=200, json=lambda: {
        'listen_queue': 2,
        'workers': [
            {
                'requests': 10,
                'harakiri_count': 1,
            },
            {
                'requests': 5,
                'harakiri_count': 2,
            }
        ]
    })
    return mocker.patch('requests.get', return_value=response)


def test_default_collector(mock_uwsgi_stats):
    collector = UWSGIStatsCollector()
    metrics = list(collector.collect())

    assert metrics[0].name == 'uwsgi_listen_queue_requests'
    assert metrics[0].samples[0].name == 'uwsgi_listen_queue_requests'
    assert metrics[0].samples[0].value == 2

    # Prometheus does interesting things with names that end with certain words, like total
    assert metrics[1].name == 'uwsgi_requests'
    assert metrics[1].samples[0].name == 'uwsgi_requests_total'
    assert metrics[1].samples[0].value == 15

    assert metrics[2].name == 'uwsgi_harakiris'
    assert metrics[2].samples[0].name == 'uwsgi_harakiris_total'
    assert metrics[2].samples[0].value == 3

    with pytest.raises(IndexError):
        assert metrics[3].name == 'shouldnt_exist'

    mock_uwsgi_stats.assert_called_once_with('http://127.0.0.1:1717', timeout=2)


def test_collector_with_options(mock_uwsgi_stats):
    collector = UWSGIStatsCollector(stats_url='http://192.168.0.1:1919', timeout=5, prefix='test')
    metrics = list(collector.collect())

    assert metrics[0].name == 'test_uwsgi_listen_queue_requests'
    assert metrics[0].samples[0].name == 'test_uwsgi_listen_queue_requests'
    assert metrics[0].samples[0].value == 2

    # Prometheus does interesting things with names that end with certain words, like total
    assert metrics[1].name == 'test_uwsgi_requests'
    assert metrics[1].samples[0].name == 'test_uwsgi_requests_total'
    assert metrics[1].samples[0].value == 15

    assert metrics[2].name == 'test_uwsgi_harakiris'
    assert metrics[2].samples[0].name == 'test_uwsgi_harakiris_total'
    assert metrics[2].samples[0].value == 3

    with pytest.raises(IndexError):
        assert metrics[3].name == 'shouldnt_exist'

    mock_uwsgi_stats.assert_called_once_with('http://192.168.0.1:1919', timeout=5)
