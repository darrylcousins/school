__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.core.files.storage import Storage
from django.core.files.storage import FileSystemStorage

class S3Storage(FileSystemStorage):
    pass
