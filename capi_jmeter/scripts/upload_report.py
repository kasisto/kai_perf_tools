import boto3, zipfile, os, logging
from botocore.exceptions import ClientError
from datetime import datetime

def upload_report():
    if "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
        # Explicitly pass aws_access_key_id and aws_secret_access_key to utilize credentials used in Jenkins
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
            )
    else:
        s3_client = boto3.client('s3')

    origin_folder_path = "capi_jmeter/configs/kcb/reports/html"
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Create a ZIP file
    zip_path = f"{timestamp}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(origin_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, origin_folder_path)
                zipf.write(file_path, arcname)
    

    target_s3_path = f"test_reports/performance/{zip_path}"
    bucket = 'kasisto-customer-data-qa'

    print(f"\nUploading report to AWS S3... \nBucket: '{bucket}' \nTarget path: '/{target_s3_path}'")
    try:
        s3_client.upload_file(zip_path, bucket, target_s3_path)

        # Generate the URL to get 'key-name' from 'bucket-name'
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket,
                'Key': target_s3_path,
                'ResponseContentDisposition': 'attachment'
            },
            ExpiresIn=86400 # 24 hours in seconds
        )
        with open('out.txt', 'w') as f:
            f.write(url)
    except ClientError as e:
        logging.error(e)

upload_report()