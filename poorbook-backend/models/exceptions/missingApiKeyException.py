class MissingApiKeyException(Exception):
    
    def __init__(self) -> None:
        self._message = "Missing API Key header."
        super().__init__(self._message)

    def __str__(self):
        return f'{self._message}'