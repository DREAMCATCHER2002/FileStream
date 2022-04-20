class FileData:
    def __init__(
        self, *, media_type: int = None, dc_id: int = None, document_id: int = None, access_hash: int = None,
        thumb_size: str = None, peer_id: int = None, volume_id: int = None, local_id: int = None, is_big: bool = None,
        file_size: int = None, mime_type: str = None, file_name: str = None, date: int = None
    ):
        self.media_type = media_type
        self.dc_id = dc_id
        self.document_id = document_id
        self.access_hash = access_hash
        self.thumb_size = thumb_size
        self.peer_id = peer_id
        self.volume_id = volume_id
        self.local_id = local_id
        self.is_big = is_big
        self.file_size = file_size
        self.mime_type = mime_type
        self.file_name = file_name
        self.date = date
