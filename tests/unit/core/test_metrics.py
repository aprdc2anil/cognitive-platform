from core.metrics.metrics import REQUEST_COUNT, REQUEST_LATENCY


def test_request_count_is_counter():
    from prometheus_client import Counter
    assert isinstance(REQUEST_COUNT, Counter)


def test_request_latency_is_histogram():
    from prometheus_client import Histogram
    assert isinstance(REQUEST_LATENCY, Histogram)


def test_request_count_increment():
    before = REQUEST_COUNT.labels(method="GET", endpoint="/test", status="200")._value.get()
    REQUEST_COUNT.labels(method="GET", endpoint="/test", status="200").inc()
    after = REQUEST_COUNT.labels(method="GET", endpoint="/test", status="200")._value.get()
    assert after == before + 1
