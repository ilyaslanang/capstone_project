import csv

# Load the csv file
with open('timedimension.csv', 'r') as f:
    reader = csv.reader(f)

    # Specify the column names
    headers = ['date_id', 'tanggal', 'bulan', 'tahun']

    # Create a new csv file with updated column names
    with open('timedimension_updated.csv', 'w', newline='') as f_updated:
        writer = csv.writer(f_updated)

        # Write the new column names to the csv file
        writer.writerow(headers)

        # Write the remaining rows from the original csv file
        for row in reader:
            writer.writerow(row)