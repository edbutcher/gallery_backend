import uuid


class File(object):
    def __init__(self, file_id, file_name, type):
        # type: (str or None, str, str) -> None

        self.file_id = file_id or uuid.uuid4().hex
        self.file_name = file_name
        self.type = type

    def serialize(self):
        # type: () -> {}

        return {
            'fileId': self.file_id,
            'fileName': self.file_name,
            'type': self.type
        }

    @classmethod
    def deserialize(cls, data):
        # type: ({}) -> File

        return cls(
            file_id=data.get('fileId'),
            file_name=data.get('fileName'),
            type=data.get('type')
        )
