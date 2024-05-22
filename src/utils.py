import uuid
import boto3
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME
from src.models import Image


s3 = boto3.client("s3",
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name='ru-central1',
                  endpoint_url='https://storage.yandexcloud.net'
                  )


def check_valid_extension(image_name: str):
    image_extensions = (".jpg", ".jpeg", ".png")
    for ext in image_extensions:
        if image_name.lower().endswith(ext):
            return ext
    raise Exception("Invalid image format")


async def upload_image_to_s3_and_save_url_to_db(file: UploadFile, session: AsyncSession) -> uuid.UUID:
    random_uuid = uuid.uuid4()
    image_extension = check_valid_extension(file.filename)
    image_name = str(random_uuid) + image_extension
    s3.put_object(Body=file.file.read(), Bucket=BUCKET_NAME, Key=image_name)
    url = f"https://{BUCKET_NAME}.storage.yandexcloud.net/{image_name}"
    image = Image(id=random_uuid, name=file.filename, image_url=url)
    session.add(image)
    await session.commit()
    return random_uuid


async def delete_image_from_s3_and_from_db(image_uuid, session):
    s3.delete_object(Bucket=BUCKET_NAME, Key=str(image_uuid))
    image = await session.get(Image, image_uuid)
    session.delete(image)
    await session.commit()
