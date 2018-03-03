__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import boto3
from boto3.s3.transfer import S3Transfer

class Command(BaseCommand):
    help = "Upload assets to S3 bucket"

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
                }
        bucket = 'cousinsd-ellesmere-static'

        boto3.setup_default_session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                )
        client = boto3.client('s3', aws_region)
        s3 = S3Transfer(client)

        ctypes = {
                'svg': 'text/svg+xml',
                'jpg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'txt': 'text/plain',
                'css': 'text/css',
                'js': 'text/javascript',
                'md': 'text/markdown',
                'woff': 'application/x-font-woff',
                }

        basename = 'assets'
        assets = os.path.join(settings.SITE_ROOT, basename)
        str_length = len(assets) - len(basename)
        count = 0
        types = []
        dirpath = ''
        for dname, subdirs, filelist in os.walk(assets):
            dirname = dname[str_length:].replace('\\', '/')
            for fname in filelist:
                count = count + 1
                extension = os.path.splitext(fname)[1][1:]
                if extension:
                    if extension not in types:
                        types.append(extension)
                    args = extra_args.copy()
                    ctype = ctypes.get(extension, None)
                    if ctype:
                        args['ContentType'] = ctype
                    key = dirname + '/' + fname
                    print('Uploading', fname, 'to', bucket, key)
                    s3.upload_file(os.path.join(dname, fname), bucket, key, extra_args=args)
        print(str(count) + ' files uploaded to ' + bucket)
        return


