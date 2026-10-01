import os
from cloudinary_storage.storage import MediaCloudinaryStorage


class DynamicCloudinaryStorage(MediaCloudinaryStorage):
    """
    Cloudinary storage backend that automatically categorizes files
    based on extension so that documents (e.g. PDF resumes, certificates)
    are uploaded as 'raw' assets while images are uploaded as 'image' assets.
    """
    RAW_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.zip', '.tar', '.gz', '.json', '.csv'}

    def _get_resource_type(self, name):
        ext = os.path.splitext(name)[1].lower()
        if ext in self.RAW_EXTENSIONS:
            return 'raw'
        return 'image'
