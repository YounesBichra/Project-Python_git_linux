7#!/bin/bash

# set variables
curl https://www.google.com/finance/quote/.INX:INDEXSP?hl=fr > /home/ec2-user/Projet_Younes_Bichra/page_scrape.txt
CSV_FILE="values.csv"


# create CSV file with headers if it doesn't exist
if [ ! -f "$CSV_FILE" ]; then
  echo "$COLUMN_HEADERS" > "$CSV_FILE"
fi

#!/bin/bash

# Get current date and time
now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Scrape S&P500 value
value=$(cat /home/ec2-user/Projet_Younes_Bichra/page_scrape.txt | grep -oP '(?<="YMlKec fxKbKc">)[^<]+' | tr ',' '.')

# Save date and value to CSV file
echo "$now,$value" >> /home/ec2-user/Projet_Younes_Bichra/values.csv
sudo fuser -k 8050/tcp && /usr/bin/python3 /home/ec2-user/Projet_Younes_Bichra/create_dashboard.py
