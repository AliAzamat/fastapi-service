class AssistantError(Exception):
    """Base for domain errors mapped to HTTP responses by a handler."""
    status_code = 400

    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class NotFound(AssistantError):
    status_code = 404


class Conflict(AssistantError):
    status_code = 409
