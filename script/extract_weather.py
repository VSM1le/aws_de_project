import csv
from datetime import datetime
import json 
import requests
import time
import boto3  # New: AWS SDK
import os
from dotenv import load_dotenv

load_dotenv()

# 1. AWS Configuration
# Tip: Never commit these keys to GitHub! Later we will move them to environment variables.
AWS_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_KEY")
BUCKET_NAME =  os.getenv("S3_BUCKET_NAME")

print("S3_ACCESS_KEY =", os.getenv("S3_ACCESS_KEY"))
print("S3_SECRET_KEY =", os.getenv("S3_SECRET_KEY"))
print("S3_BUCKET_NAME =", os.getenv("S3_BUCKET_NAME"))

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Initialize the S3 Client connection
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def weatherApi(lat, lon):
    URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(URL)
    return response.json()

def uploadJsonToS3(district_name, json_weather):   
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    # This creates the exact same time-partitioned folder structure inside S3!
    s3_key = f"raw/year={year}/month={month}/day={day}/{district_name}.json"

    # Convert our Python dictionary/JSON into a string format that S3 accepts
    json_string = json.dumps(json_weather, indent=4)

    # Upload directly to the cloud without saving a local file
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=json_string,
        ContentType="application/json"
    )
    print(f"Successfully uploaded {district_name}.json to S3 bucket path: {s3_key}")

# Main execution loop
# Adjusted path assuming you run this from the project root directory
with open('configs/master_district.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        time.sleep(1) 
        
        # Pull data using coordinates
        weather_json = weatherApi(row["latitude"], row["longitude"])
        
        # Upload straight to AWS S3 using the Thai district name as the filename
        uploadJsonToS3(row['district'], weather_json)
        
        # Let's break after 2 districts for your first test so you can verify it works instantly
        # without waiting for all 50 districts.
        print("Stopping test loop. Check your AWS console!")
        break