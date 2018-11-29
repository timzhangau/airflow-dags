import boto3
import os
import logging

def upload_file_to_s3(local_file, bucket_name, new_filename=None):
    s3 = boto3.client('s3')
    if new_filename is None:
        local_path, local_filename = os.path.split(local_file)
        new_filename = local_filename
    s3.upload_file(local_file, bucket_name, new_filename)
    logging.info(f'{local_file} uploaded to s3 bucket {bucket_name} with the name of {new_filename}')