class Response:
    def __init__(self):
        self.status_code = 200
        self.data = None
        self.message = None
        self.errors = []

    def add_error(self, error_message):
        self.errors.append(error_message)

    def set_status_ok(self):
        self.status_code = 200

    def set_status_redirect(self):
        self.status_code = 302

    def has_errors(self):
        return len(self.errors)
