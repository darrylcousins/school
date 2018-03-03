__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import os
import tempfile

import boto3
from boto3.s3.transfer import S3Transfer

from PIL import Image

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from caretaking.models import Photo

class Command(BaseCommand):
    help = "Upload media files to S3 bucket"

    requires_migrations_checks = True

    def handle(self, *args, **options):
        """Lazy no error checking, relies on good collection of data.
        
        TODO: delete assets and call `collectstatic --noinput`
        """
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION')
        extra_args = {
                'ACL': 'public-read',
                'ContentType': 'jpg',
                }
        bucket = 'cousinsd-ellesmere-static'

        boto3.setup_default_session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                )
        client = boto3.client('s3', aws_region)
        s3 = S3Transfer(client)

        basename = 'media'
        media = os.path.join(settings.SITE_ROOT, basename)
        count = 0
        size = 768, 576

        for photo in Photo.objects.all():
            fpath = photo.image.path
            fname = photo.image.name
            img = Image.open(fpath)
            isize = img.width, img.height
            if isize != size:
                newimg = img.resize(size, Image.LANCZOS)
                img.close()
                newimg.save(fpath, 'jpeg')
                newimg.close()

            key = basename + '/' + fname
            print('Uploading', fpath, 'to', bucket, key)
            s3.upload_file(fpath, bucket, key, extra_args=extra_args)

        return
