from temp_eval.utils import sanitise_response


class TestSanitisation:

    def test_left_padding(self):
        source_text = "Alice and Bob are friends"
        response = "I can anonymise this: [NAME] and [NAME] are friends"
        assert sanitise_response(source_text,
                                 response) == "[NAME] and [NAME] are friends"

    def test_right_padding(self):
        source_text = "Alice and Bob are friends"
        response = "[NAME] and [NAME] are friends, this is the correct anonymisation"
        assert sanitise_response(source_text,
                                 response) == "[NAME] and [NAME] are friends,"

    def test_left_right_padding(self):
        source_text = "Alice and Bob are friends"
        response = "This is the correct anonymisation: [NAME] and [NAME] are friends. Let me know if you would like to anonymise something else"
        assert sanitise_response(source_text,
                                 response) == "[NAME] and [NAME] are friends."

    def test_left_newline_padding(self):
        source_text = "Alice and Bob are friends"
        response = "This is the correct anonymisation:\n [NAME] and [NAME] are friends"
        assert sanitise_response(source_text,
                                 response) == "[NAME] and [NAME] are friends"

    def test_right_newline_padding(self):
        source_text = "Alice and Bob are friends"
        response = "[NAME] and [NAME] are friends\n This is the correct anonymisation"
        assert sanitise_response(source_text,
                                 response) == "[NAME] and [NAME] are friends"

    def test_left_right_newline_padding(self):
        source_text = "Alice and Bob are friends"
        response = "This is the correct anonymisation:\n [NAME] and [NAME] are friends. \n Let me know if you would like to anonymise something else"
        assert sanitise_response(source_text,
                                 response) == "[NAME] and [NAME] are friends."

    def test_left_multiline_padding(self):
        source_text = "Alice and Bob are friends"
        response = """This is the correct anonymisation:
        
        [NAME] and [NAME] are friends"""
        assert sanitise_response(source_text,
                                 response) == "[NAME] and [NAME] are friends"

    def test_right_multiline_padding(self):
        source_text = "Alice and Bob are friends"
        response = """[NAME] and [NAME] are friends
        
        Let me know if you would like to anonymise something else"""
        assert sanitise_response(source_text,
                                 response) == "[NAME] and [NAME] are friends"

    def test_left_right_multiline_padding(self):
        source_text = "Alice and Bob are friends"
        response = """This is the correct anonymisation:
        
        [NAME] and [NAME] are friends
        
        Let me know if you would like to anonymise something else"""
        assert sanitise_response(source_text,
                                 response) == "[NAME] and [NAME] are friends"
