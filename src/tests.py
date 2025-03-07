from src.metrics_oop import Metrics


class TestMetrics:
    def test_true_positives(self):
        metrics = Metrics()
        privacy_mask = [{'value': 'Alice'}, {'value': 'Bob'}]
        anonymised_text = 'Alice and Bob are friends.'
        assert metrics.true_positives(anonymised_text, privacy_mask) == 2

    def test_false_positives_negatives(self):
        metrics = Metrics()
        target_text = 'Alice and Bob are friends.'
        anonymised_text = 'Alice and Bob are friends.'
        assert metrics.false_positives_negatives(anonymised_text, target_text) == (0, 0)

