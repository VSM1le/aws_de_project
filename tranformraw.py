import csv
import pandas as pd

data = {
    "province": [],
    "district": [],
    "subdistrict": [],
    "latitude": [],
    "longitude": []
}

last_district = ""

allow_district = {
    "province": "",
    "district": "",
    "subdistrict": "",
    "latitude": "",
    "longitude": ""
}

with open('raw/output.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:

        if last_district and row["district"] != last_district:
            data["province"].append(allow_district["province"])
            data["district"].append(allow_district["district"])
            data["subdistrict"].append(allow_district["subdistrict"])
            data["latitude"].append(allow_district["latitude"])
            data["longitude"].append(allow_district["longitude"])

        if not last_district or row["district"] != last_district:
            last_district = row["district"]
            allow_district = {
                "province": row["province"],
                "district": row["district"],
                "subdistrict": row["subdistrict"],
                "latitude": row["latitude"],
                "longitude": row["longitude"]
            }

        # Prefer the row where subdistrict == district
        if row["subdistrict"] == row["district"]:
            allow_district = {
                "province": row["province"],
                "district": row["district"],
                "subdistrict": row["subdistrict"],
                "latitude": row["latitude"],
                "longitude": row["longitude"]
            }

# Add the last district
if allow_district["district"]:
    data["province"].append(allow_district["province"])
    data["district"].append(allow_district["district"])
    data["subdistrict"].append(allow_district["subdistrict"])
    data["latitude"].append(allow_district["latitude"])
    data["longitude"].append(allow_district["longitude"])


df = pd.DataFrame(data)

# Save to CSV without the row index numbers
df.to_csv("master_district.csv", index=False)

            
        
