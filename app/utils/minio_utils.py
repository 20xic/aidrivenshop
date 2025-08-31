from uuid import uuid4
from fastapi import UploadFile
from core import minio_helper, logger
from core.model.images import ImageMetadata

async def upload_image_to_minio(file: UploadFile, bucket: str) -> uuid.UUID:
    file_id = uuid4()
    try:
        client = minio_helper.get_client()
        client.put_object(
            bucket_name=bucket,
            object_name=str(file_id),
            data=file.file,
            length=file.size,
            content_type=file.content_type
        )
        
        image_metadata = ImageMetadata(
            id=file_id,
            original_filename=file.filename,
            file_size=file.size,
            content_type=file.content_type,
            bucket_name=bucket
        )
        return file_id
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise