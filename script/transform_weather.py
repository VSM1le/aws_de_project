from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, input_file_name, regexp_extract
import os

def run_transformation():
    # 1. Initialize local Spark Session
    spark = SparkSession.builder \
        .appName("BangkokWeatherTransformation") \
        .master("local[*]") \
        .getOrCreate()

    # Get current date formatted to match our datalake folders
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    # 2. Define source paths using wildcard (*) to load all files at once
    raw_input_path = f"datalake/raw/year={year}/month={month}/day={day}/*.json"
    processed_output_path = f"datalake/processed/year={year}/month={month}/day={day}/"


    print(f"Reading raw files from: {raw_input_path}")

    try:
        # Read all JSON files into a Spark DataFrame
        df_raw = spark.read.option("multiLine", True).json(raw_input_path)

        # 3. Transform and Flatten nested attributes
        df_cleaned = df_raw.select(
            # CHANGED: Extract the Thai district name from the file name safely
            regexp_extract(input_file_name(), r"([^/]+)\.json$", 1).alias("district_name_th"),
            
            col("main.temp").alias("temperature"),
            col("main.humidity").alias("humidity"),
            col("main.pressure").alias("pressure"),
            col("wind.speed").alias("wind_speed"),
            col("weather")[0]["main"].alias("weather_condition"),
            current_timestamp().alias("processed_at")
        )

        # Show transformation results in the console for confirmation
        df_cleaned.show(5)

        # 4. Save cleanly structured data as Parquet
        df_cleaned.write \
            .mode("overwrite") \
            .parquet(processed_output_path)
            
        print(f"Transformation complete! Data saved to: {processed_output_path}")

    except Exception as e:
        print(f"Error during transformation phase: {e}")
    
    finally:
        # Always terminate session to clear memory leaks
        spark.stop()

if __name__ == "__main__":
    run_transformation()
