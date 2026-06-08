import boto3
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(".env")

def mock_data() -> str:
    data = {
        'order_id': [1001, 1002, 1003, 1004],
        'customer': ['Alice', 'Bob', 'Charlie', 'David'],
        'country': ['US', 'UK', 'US', 'DE'],
        'amount': [150.00, 45.50, 200.00, 12.00],
        'status': ['completed', 'completed', 'canceled', 'completed']
    }   
    df = pd.DataFrame(data)
    # Save inside our shared volume data folder
    file_path = 'data/sell_' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.csv'
    df.to_csv(file_path, index=False)
    print("✅ Extracted raw orders successfully.")

    return file_path


def main():
    # 🌟 CHANGE: Use boto3.resource instead of boto3.client
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
        region_name=os.getenv("S3_REGION")
    )

    print("Connected to AWS Successfully! Here are your buckets:")
    # Now this loop works perfectly!
    bucket_name = ""
    for bucket in s3_resource.buckets.all():
        bucket_name = bucket.name
        print(f"📁 {bucket.name}")  
        break 

    if bucket_name == "":
       print("no bucket find...")
       return

    file_path = mock_data() 
    
    cloud_destination = "raw/2026-06-08/" + file_path

    print(f"🚀 Uploading {file_path} to S3...")

    # 3. Push the file to the cloud
    s3_resource.meta.client.upload_file(
        Filename=file_path,
        Bucket=bucket_name,
        Key=cloud_destination
    )

    print("🎉 Upload Complete! Go check your AWS Console!")


if __name__ == "__main__":
    main()

