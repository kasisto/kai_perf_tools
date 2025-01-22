import boto3, zipfile, os, logging
from botocore.exceptions import ClientError
from datetime import datetime

def upload_folder_to_s3(origin_folder_path, destination_folder_path, bucket_name, zip_name):
    """
    Compress a folder into a ZIP file and upload it to S3.
    Returns a pre-signed URL for downloading the ZIP file.
    """
    if "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
        # Explicitly pass aws_access_key_id and aws_secret_access_key to utilize credentials used in Jenkins
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )
    else:
        s3_client = boto3.client('s3')

    # Create a ZIP file
    zip_path = f"{zip_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(origin_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, origin_folder_path)
                zipf.write(file_path, arcname)

    # Upload ZIP file to S3
    try:
        s3_client.upload_file(zip_path, bucket_name, f"{destination_folder_path}/{zip_path}")
        print(f"Uploaded {zip_path} to s3://{bucket_name}/{destination_folder_path}/{zip_path}")
    except ClientError as e:
        print(f"Error uploading ZIP file: {e}")
        return None
    finally:
        os.remove(zip_path)

    # Generate a pre-signed URL for the ZIP file
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': zip_name},
            ExpiresIn=86400  # 24 hours in seconds
        )

        with open('out.txt', 'w') as f:
            f.write(url)
        return url
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e}")
        return None

def upload_report(origin_folder_path, bucket):
    # It will be stored in bucket_name/test_reports/file_name
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        destination_folder_path = f"test_reports/performance"
        print(f"\nUploading folder to AWS S3... \nBucket: '{bucket}' \nSource folder: '{origin_folder_path}' \nDestination folder: '{destination_folder_path}'")
        
        upload_folder_to_s3(origin_folder_path, destination_folder_path, bucket, timestamp)
    except ClientError as e:
        logging.error(f"Error uploading folder: {e}")

origin_folder_path = "capi_jmeter/configs/kcb/reports/html"
bucket = 'kasisto-customer-data-qa'
upload_report(origin_folder_path, bucket)
