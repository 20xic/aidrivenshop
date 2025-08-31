from minio import Minio
from minio.error import S3Error
from core import settings
from core import logger

class MinioHelper:
    def __init__(self):
        self.client = None
        self.connected = False
        self.bucket_name = settings.minio.bucket_name

    def connect(self):
        try:
            print("MINIO ENDPOINT",settings.minio.endpoint)
            self.client = Minio(
                settings.minio.endpoint,
                access_key=settings.minio.access_key,
                secret_key=settings.minio.secret_key,
                secure=settings.minio.secure
            )
            # Создаем бакет по умолчанию, если его нет
            self._ensure_bucket_exists()
            self.connected = True
            logger.info("Minio connected successfully")
        except Exception as e:
            logger.error(f"Minio connection error: {e}")
            raise

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Bucket '{self.bucket_name}' created")
            else:
                logger.info(f"Bucket '{self.bucket_name}' already exists")
        except S3Error as e:
            logger.error(f"Error checking/creating bucket: {e}")
            raise

    def disconnect(self):
        self.client = None
        self.connected = False
        logger.info("Minio disconnected")

    def get_client(self) -> Minio:
        if not self.connected:
            self.connect()
        return self.client

minio_helper = MinioHelper()