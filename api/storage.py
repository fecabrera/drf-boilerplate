from django.conf import settings
from django.core.files.storage import default_storage
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


if settings.TESTING:
    static_storage = default_storage
    media_storage = default_storage
    private_media_storage = default_storage
else:
    static_storage = StaticStorage()
    media_storage = MediaStorage()
    private_media_storage = PrivateMediaStorage()
