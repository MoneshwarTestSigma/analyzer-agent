import boto3
import json
import gzip
import io
import os

class S3Client():
    """
    A Singleton class for managing interactions with AWS S3.
    Ensures only one instance of the S3 client is created.
    """

    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name="us-east-1",
            endpoint_url="https://s3.amazonaws.com/"
        )
    
    def get_presigned_url(self, url , expiration=10800):
            """
            Generate a presigned URL for an S3 object.

            :param bucket_name: Name of the S3 bucket.
            :param object_key: Key of the object in the bucket.
            :param expiration: Time in seconds for the presigned URL to remain valid (default is 10,800 seconds) (3 Hrs).
            :return: Presigned URL as a string.
            """
            try:
                bucket_name, object_key = self.extract_bucket_and_prefix(url)
                if self.get_file(bucket_name + object_key) is None:
                    return None
                url = self.s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket_name, 'Key': object_key},
                    ExpiresIn=expiration
                )
                return url
            except Exception as e:
                # print(f"Error generating presigned URL: {e}")
                return None
    
    def get_file(self, url, decode='utf-8'):
        """
        Gets a file from S3 using a full S3 URL and decodes it
        """
        bucket, prefix = self.extract_bucket_and_prefix(url)
        
        try:
            obj = self.s3.get_object(Bucket=bucket, Key=prefix)
            data = obj['Body'].read().decode(decode,errors='ignore')
            
            if decode == 'windows-1252':
                return data.splitlines()
            return json.loads(data)
        except self.s3.exceptions.NoSuchKey:
            # print(f"File not found in S3: {url}")
            return None
        except Exception as e:
            # print(f"Error accessing file {url}: {str(e)}")
            return None
    
    def extract_bucket_and_prefix(self, url):
        """
        Extracts bucket and prefix from a full S3 URL
        
        Args:
            url (str): Full S3 URL (e.g., "results-staging.testsigma.com/3817/step-results/...")
            
        Returns:
            tuple: (bucket_name, prefix)
        """
        parts = url.split('/')
        bucket = parts[0]
        prefix = '/'.join(parts[1:]) if len(parts) > 1 else ''
        return bucket, prefix
    
    def get_all_step_results(self, url):
        """
        Lists all available paths in given S3 folder and downloads JSON files
        
        Args:
            url (str): Full S3 URL containing bucket and path
            
        Returns:
            list: List containing contents of all JSON files
        """
        bucket, prefix = self.extract_bucket_and_prefix(url)
        json_contents = []
        
        paginator = self.s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
      
        for page in pages:
            if 'Contents' not in page:
                continue
                
            json_files = []
            for obj in page['Contents']:
                if obj['Key'].endswith('.json') and 'step-results-' in obj['Key']:
                    json_files.append(obj)
            
            json_files.sort(key=lambda x: int(x['Key'].split('-')[-1].replace('.json', '')))
            
            for obj in json_files:
                try:
                    response = self.s3.get_object(Bucket=bucket, Key=obj['Key'])
                    content = response['Body'].read()
                    
                    with gzip.GzipFile(fileobj=io.BytesIO(content)) as gz:
                            file_content = gz.read().decode('utf-8')
                        
                    json_data = json.loads(file_content)
                    if isinstance(json_data, list):
                        json_contents.extend(json_data)
                    else:
                        json_contents.append(json_data)
                except Exception as e:
                    print(f"Error processing {obj['Key']}: {str(e)}")
                    raise Exception(f"Error processing {obj['Key']}: {str(e)}")
        
        return json_contents
    
    def upload_json(self, data, url):
        """
        Uploads JSON data to S3 at the specified URL
        
        Args:
            data: The data to upload (dict or list)
            url: Full S3 URL where to upload the file
        """
        bucket, key = self.extract_bucket_and_prefix(url)
        try:
            json_data = json.dumps(data)
            self.s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=json_data,
                ContentType='application/json'
            )
            print(f"Successfully uploaded JSON to {url}")
        except Exception as e:
            print(f"Error uploading to {url}: {str(e)}")
            raise Exception(f"Error uploading to {url}: {str(e)}")
            
