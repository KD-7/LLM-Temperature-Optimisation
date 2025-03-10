from temp_eval.metrics import Metrics

# See README for how to run the tests
class TestMetrics:
    def test01_true_positives(self):
        metrics = Metrics()
        privacy_mask = [{'value': 'Alice'}, {'value': 'Bob'}]
        anonymised_text = 'Alice and Bob are friends.'
        assert metrics.true_positives(anonymised_text, privacy_mask) == 0

    def test02_true_positives(self):
        metrics = Metrics()
        privacy_mask = [{'value': 'Alice'}, {'value': 'Bob'}]
        anonymised_text = '[NAME] and [NAME] are friends.'
        assert metrics.true_positives(anonymised_text, privacy_mask) == 2

    def test01_false_positives_negatives(self):
        metrics = Metrics()
        anonymised_text = 'Alice and Bob are friends.'
        target_text = '[NAME] and [NAME] are friends.'
        assert metrics.false_positives_negatives(anonymised_text, target_text) == (0, 2)

    def test02_false_positives_negatives(self):
        metrics = Metrics()
        target_text = '[NAME] and [NAME] are friends.'
        anonymised_text = '[NAME] and [NAME] are friends.'
        assert metrics.false_positives_negatives(anonymised_text, target_text) == (0, 0)

    def test01_strip_anonymisation(self):
        metrics = Metrics()
        anonymised_text = 'Alice and Bob are friends.'
        stripped_anonymised_text = 'Alice and Bob are friends.'
        assert metrics.strip_anonymisation(anonymised_text) == stripped_anonymised_text

    def test02_strip_anonymisation(self):
        metrics = Metrics()
        anonymised_text = '[NAME] and [NAME] are friends.'
        stripped_anonymised_text = 'and  are friends.'
        assert metrics.strip_anonymisation(anonymised_text) == stripped_anonymised_text

    def test01_anonymisation_metrics(self):
        metrics = Metrics()
        anonymised_text = 'Alice and Bob are friends.'
        target_text = '[NAME] and [NAME] are friends.'
        privacy_mask = [{'value': 'Alice'}, {'value': 'Bob'}]
        assert metrics.anonymisation_metrics(anonymised_text, target_text, privacy_mask) == (0, 0, 0)

    def test02_anonymisation_metrics(self):
        metrics = Metrics()
        anonymised_text = 'Alice and [NAME] are friends.'
        target_text = '[NAME] and [NAME] are friends.'
        privacy_mask = [{'value': 'Alice'}, {'value': 'Bob'}]
        assert metrics.anonymisation_metrics(anonymised_text, target_text, privacy_mask) == (1, 0.5, 0.6666666666666666)

    def test03_anonymisation_metrics(self):
        metrics = Metrics()
        anonymised_text = '[NAME] and [NAME] are friends.'
        target_text = '[NAME] and [NAME] are friends.'
        privacy_mask = [{'value': 'Alice'}, {'value': 'Bob'}]
        assert metrics.anonymisation_metrics(anonymised_text, target_text, privacy_mask) == (1, 1, 1)

    def test01_text_similarity_metrics(self):
        metrics = Metrics()
        anonymised_text = '[NAME] and [NAME] are friends.'
        ground_truth = '[NAME] and [NAME] are friends.'
        assert metrics.text_similarity_metrics(anonymised_text, ground_truth) == (1, 1, 1)

    def test02_text_similarity_metrics(self):
        metrics = Metrics()
        anonymised_text = 'Alice and Bob are friends.'
        ground_truth = '[NAME] and [NAME] are friends.'
        assert metrics.text_similarity_metrics(anonymised_text, ground_truth) == (0.7499999999999999, 0.3333333333333333, 0.7499999999999999)




