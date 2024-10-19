import subprocess
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


# Function to get network traffic data using vnstat
def get_network_data():
    try:
        # Run vnstat command to get network statistics in a single line format
        result = subprocess.run(['vnstat', '--oneline'], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("vnstat command failed")
        
        # Split the output by semicolon
        data = result.stdout.split(";")
        if len(data) < 5:
            # Print raw output for debugging
            print("Unexpected vnstat output:", result.stdout)
            raise ValueError("vnstat output does not contain the expected number of fields")
        
        # Extract the download and upload data (in MB)
        rx_mb = float(data[3].split()[0])  # Total downloaded in MB
        tx_mb = float(data[4].split()[0])  # Total uploaded in MB
        return rx_mb, tx_mb
    except (IndexError, ValueError) as e:
        print("Error processing vnstat output:", str(e))
        return 0.0, 0.0  # Return 0.0 for both values if there's an issue

# Function to log data into PostgreSQL database
def log_to_postgres(rx_mb, tx_mb):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD")
        )
        cursor = conn.cursor()
        # Insert data into the table
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO daily_usage (timestamp, download_mb, upload_mb)
            VALUES (%s, %s, %s)
        ''', (timestamp, rx_mb, tx_mb))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Logged to PostgreSQL: Download: {rx_mb} MB, Upload: {tx_mb} MB at {timestamp}")
    except Exception as e:
        print("Failed to log data to PostgreSQL:", str(e))

# Main function to collect and log data
def main():
    rx_mb, tx_mb = get_network_data()
    log_to_postgres(rx_mb, tx_mb)
    print(f"Logged: Download: {rx_mb} MB, Upload: {tx_mb} MB")

if __name__ == "__main__":
    main()
