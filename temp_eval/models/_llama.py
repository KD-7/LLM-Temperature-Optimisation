import ollama


class LLama:

    def __init__(self, model_name: str, prompt: str):
        self.model_name = model_name
        self.prompt = prompt
        ollama.pull(model_name)

    def update_prompt(self, new_prompt: str):
        """Set a new instruction prompt for the model
        Args:
            new_prompt (str): The new instruction prompt
        """
        self.prompt = new_prompt

    def generate(self, data: str, temperature: float):
        """Get model response to user input
        Args:
            data (str): The user input
            temperature (float): The temperature setting for the model
        Returns:
            str: The response from the model
        """
        # No need to stream response for our use case
        return ollama.generate(model=self.model_name,
                               system=self.prompt,
                               prompt=data,
                               options={'temperature': temperature}).response
