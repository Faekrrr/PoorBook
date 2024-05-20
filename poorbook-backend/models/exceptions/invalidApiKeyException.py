class InvalidApiKeyException(Exception):
    
    def __init__(self) -> None:
        self._message = "Invalid API Key"
        super().__init__(self._message)
    
    def __str__(self):
        return f'{self._message}'