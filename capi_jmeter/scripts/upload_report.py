import boto3
import os
import logging
from botocore.exceptions import ClientError
from datetime import datetime

def upload_folder_to_s3(folder_path, destination_folder_path, bucket_name, s3_client):
    """
    Uploads all files in a folder to the specified S3 bucket.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            s3_path = os.path.join(destination_folder_path, file)
            print(s3_path)
            try:
                print(f"Uploading {file_path} to s3://{bucket_name}/{s3_path}")
                s3_client.upload_file(file_path, bucket_name, s3_path)
            except ClientError as e:
                logging.error(f"Error uploading {file_path}: {e}")

def upload_report():
    # It will be stored in bucket_name/test_reports/file_name
    print(f"AWS_ACCESS_KEY_ID: {'AWS_ACCESS_KEY_ID' in os.environ}")
    print(f"AWS_SECRET_ACCESS_KEY: {'AWS_SECRET_ACCESS_KEY' in os.environ}")
    print("AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ)

    if "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
        # Explicitly pass aws_access_key_id and aws_secret_access_key to utilize credentials used in Jenkins
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )
    else:
        s3_client = boto3.client('s3')

    folder_name = 'html'
    origin_folder_path = f"configs/kcb/reports/{folder_name}"
    bucket = 'kasisto-customer-data-qa'

    print(f"\nUploading folder to AWS S3... \nBucket: '{bucket}' \nSource folder: '{origin_folder_path}'")
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        destination_folder_path = f"test_reports/{timestamp}/"
        # upload_folder_to_s3(origin_folder_path, destination_folder_path, bucket, s3_client)
        print(s3_client.upload_file(f"{origin_folder_path}/index.html", bucket, destination_folder_path))
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket,
                'Key': destination_folder_path,
                'ResponseContentDisposition': 'attachment'
            },
            ExpiresIn=86400  # 24 hours in seconds
        )
        print(url)
        with open('out.txt', 'w') as f:
            f.write(url)
    except ClientError as e:
        logging.error(f"Error uploading folder {folder_name}: {e}")

upload_report()
