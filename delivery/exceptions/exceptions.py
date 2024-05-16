class FieldError(Exception):
        def __init__(self, error_message) -> None:
            super().__init__()
            if len(error_message) > 1:
                for i in range(0, len(error_message) - 1):
                    error_message[i] += ", "
            self.error_message = "".join(error_message)

        def __str__(self) -> str:
            return self.error_message