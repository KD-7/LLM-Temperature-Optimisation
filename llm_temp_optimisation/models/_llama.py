
#TODO Setup config here make the only thing that we can modify the constructor with the temperature parameter

class LLama3_1:
    def __init__(self, temperature: float):
        self.temperature = temperature

    def _setup(self):
        pass