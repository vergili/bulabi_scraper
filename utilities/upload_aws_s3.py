import os
import sys
from web_crawler.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def upload_s3(bucket_name, local_file_path, s3_path, s3_file_name):

    import boto

    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(bucket_name)

    def percent_cb(complete, total):
        #sys.stdout.write('.')
        sys.stdout.flush()

    key_name = s3_file_name

    full_key_name = os.path.join(s3_path, key_name)

    k = bucket.new_key(full_key_name)

    k.set_contents_from_filename(local_file_path, cb=percent_cb, num_cb=50)

    return full_key_name