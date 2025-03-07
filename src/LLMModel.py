import ollama

class LLMModel:
    """Handles interactions with the LLM model."""

    def __init__(self, model_name="llama3", instruction=None):
        self.model_name = model_name
        self.instruction = instruction or (
            "You are an advanced anonymizer that replaces personally identifiable "
            "information (PII) with a category label. You will NOT paraphrase or "
            "change any part of the text except for replacing PII with its category in square brackets.\n\n"

            "Example:\n"
            "Input: My name is Alice and I live in London.\n"
            "Output: My name is [NAME] and I live in [LOCATION]."
        )

    def anonymize_text(self, input_text, temperature):
        """Sends a request to the LLM model and returns the anonymized response."""
        stream = ollama.chat(
            model=self.model_name,
            messages=[
                {'role': 'system', 'content': self.instruction},
                {'role': 'user', 'content': input_text}
            ],
            stream=True,
            options={'temperature': temperature}
        )

        response_text = "".join(chunk.get('message', {}).get('content', '') for chunk in stream)
        return response_text
