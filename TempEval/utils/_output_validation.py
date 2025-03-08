
def sanitise_response(source_text, response: str) -> str:
    """
    Remove any extraneous text from the model response.

    This function ensures that the model only outputs the anonymized text,
    ignoring any additional messages

    Args:
    - response (str): The raw model response.

    Returns:
    - str: The cleaned model response.
    """
    first_word_source = source_text.split()[0]
    first_word_response = response.split()[0]

    # Check if the response is valid: If both start with the same word or if the
    # models response indicates the start of a category label then the response is
    # valid. (It wasn't checked against the source having a category label as the llm
    # could've mistakenly put one)

    if ((first_word_source == first_word_response) or
            (first_word_source[0] == first_word_response[0])):
        return response

    # Clean response
    response_tokens = response.split()
    for i in range(len(response_tokens)):
        if (response_tokens[i] == first_word_source) or (response_tokens[i][0] == "["):
            return str(response_tokens[i:])

    raise ValueError("Response does not match source text")
