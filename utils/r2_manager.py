import boto3
import json
import os

R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_BUCKET_NAME = 'hopehub-storage'

r2_client = boto3.client('s3',
    endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY
)

def upload_media_list(media, source):
    try:
        r2_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=f"MEDIA/{source}_media.json",
            Body=json.dumps(media, indent=2).encode('utf-8'),
            ContentType='application/json'
        )
        print(f"[Upload] Successfully uploaded {source}_media.json")
    except Exception as e:
        print(f"[Upload] Failed to upload to R2: {e}")
