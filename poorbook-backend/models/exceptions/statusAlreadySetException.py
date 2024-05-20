
class StatusAlreadySetException(Exception):

    def __init__(self, message: str  = "This status is already set.")-> None:
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return f'{self._message}'