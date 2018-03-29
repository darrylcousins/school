__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.core.files.storage import Storage
from django.core.files.storage import FileSystemStorage

class S3Storage(FileSystemStorage):

    def save(self, name, content, max_length=None):
        """
        Save new content to the file specified by name. The content should be
        a proper File object or any python file-like object, ready to be read
        from the beginning.

        Don't save anything.

        Clearly this should be more comprehensive, calling other methods on
        this storage will either produce and error or at least something
        untoward. But it does for now.
        """
        print('pretend saving', name)
        return name
