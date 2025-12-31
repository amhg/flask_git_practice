from werkzeug.exceptions import HTTPException

class DuplicateRecordException(HTTPException):
    code = 500
    #description = ""

    def __init__(self, message):
        super().__init__(description=message)

    def to_dict(self):
        return {
            'error': self.description,
            'code': self.code
        }
