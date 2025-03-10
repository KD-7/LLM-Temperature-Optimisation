def sanitise_response(source_text, response: str) -> str:
    """
    Remove any extraneous text from the model response.

    This function ensures that the model only outputs the anonymized text,
    ignoring any additional messages

    Args:
    - source_text (str): The original text that was passed to the model.
    - response (str): The raw model response.

    Returns:
    - str: The cleaned model response.
    """

    # Note our assumption is that the LLM will nestle the correct output structure
    # within its response.
    # ==============================
    # Check if the response is valid
    # ==============================
    # For the start of the response:
    # - If both start with the same word or if the models response indicates the start
    # of a category label then the start of the response is valid. (It wasn't checked
    # against the source having a category label as the llm could've mistakenly put one)
    #
    # For the end of the response:
    #  - If the models response ends with a category label
    #  - If the last two words of the response are the same as the source
    #  - If the last word of the response is the same as the source and the word before
    #    in the response is the end of a category label

    source_tokens = source_text.split()
    first_word_source = source_tokens[0]

    response_tokens = response.split()
    response_size = len(response_tokens)

    front_slice = 0
    back_slice = response_size

    front_correct = False
    back_correct = False

    for i in range(response_size):
        if not front_correct:
            if (response_tokens[i] == first_word_source) or (
                    response_tokens[i][0] == "["):
                front_slice = i
                front_correct = True

        if not back_correct:
            # Used for checking the last two words of the response
            last_word_index = response_size - i - 1
            word_before_last = last_word_index - 1

            # The last two words of the source remain the same
            last_word_source = source_tokens[len(source_tokens) - 1]
            word_before_last_source = source_tokens[len(source_tokens) - 2]

            # Move backwards through the response
            last_word_response = response_tokens[last_word_index]
            word_before_last_response = response_tokens[word_before_last]

            if (last_word_response[len(last_word_response) - 1] == "]"):
                back_slice = response_size - i
                back_correct = True

            if (last_word_source == last_word_response):
                if ((word_before_last_source == word_before_last_response) or
                        (word_before_last_response[
                             len(word_before_last_response) - 1] == "]")):
                    back_slice = response_size - i
                    back_correct = True

        if front_correct and back_correct:
            break

    return str(response_tokens[front_slice:back_slice])
