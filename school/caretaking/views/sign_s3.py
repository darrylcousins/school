__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import os
import datetime
import posixpath

from django.http import JsonResponse, Http404
from django.views.generic import View

import boto3

from caretaking.models import Photo

class SignS3View(View):

    def get(self, request, *args, **kwargs):
        """
        """

        filename = request.GET.get('filename')
        filetype = request.GET.get('filetype')

        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION')
        bucket = os.getenv('AWS_BUCKET')
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

        upload_to = Photo._meta.get_field('image').upload_to
        dirname = datetime.datetime.now().strftime(upload_to)
        filename = posixpath.join(dirname, filename)
        filename = 'media/' + filename

        presigned_post = client.generate_presigned_post(
            Bucket = bucket,
            Key = filename,
            Fields = {
                "acl": "public-read",
                "Content-Type": filetype,
                },
            Conditions = [
                {"acl": "public-read"},
                {"Content-Type": filetype}
                ],
            ExpiresIn = 3600
        )

        data = {
            'data': presigned_post,
            'url': 'https://%s.s3.amazonaws.com/%s' % (bucket, filename)
        }
        return JsonResponse(data)

