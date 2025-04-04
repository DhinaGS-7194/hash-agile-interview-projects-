# CSV to PostgreSQL Table Import Script

## Overview
This Python script reads data from a CSV file, processes the data, and imports it into a PostgreSQL database table. The script dynamically determines the data types and creates a new table accordingly before inserting the records.

## Prerequisites
- Python installed on the system.
- PostgreSQL database running.
- `psycopg2` library installed for database interaction.
- A CSV file (`data.csv`) located in the `others/csv/` directory.

## Dependencies
```python
import csv
from math import floor
import psycopg2 as pg
```

## Database Connection
The script establishes a connection to a PostgreSQL database using `psycopg2`:
```python
cur = pg.connect(host="localhost", dbname="postgres", user="postgres", password="1234", port=5432).cursor()
```

## Reading the CSV File
The script opens and reads the CSV file:
```python
file = open(r"others\csv\data.csv", 'r')
```
The data is processed using `csv.reader()` where each value is converted to its appropriate data type:
```python
reader = []
for rows in csv.reader(file, delimiter=' ', lineterminator='\n'):
    row = []
    for i in rows:
        try:
            float(i)
            try:
                int(i)
                row.append(int(i))
            except ValueError:
                row.append(float(i))
        except ValueError:
            row.append(i)
    reader.append(row)
```

## Creating the Table
The script dynamically creates a new table (`csv1`) based on the column names and inferred data types:
```python
table = "csv1"
field_set = True
for row in reader:
    if field_set:
        cur.execute(f"CREATE TABLE {table}();")

        data_types = []
        for data in reader[-1]:
            if isinstance(data, float):
                data_types.append('FLOAT')
            elif isinstance(data, int):
                data_types.append('INTEGER')
            else:
                data_types.append('TEXT')

        for i in range(len(row)):
            cur.execute(f"ALTER TABLE {table} ADD {row[i]} {data_types[i]};")

        cur.execute("COMMIT;")
        field_set = False
```

## Inserting Data
After the table is created, the script inserts the data:
```python
    else:
        cur.execute(f"INSERT INTO csv1 VALUES{tuple(row)};")
```

## Committing Changes
Once all the data is processed, the script commits the changes to the database:
```python
cur.execute("COMMIT;")
```

## Closing the File
Finally, the script closes the CSV file:
```python
file.close()
```

## Notes
- The script assumes that the last row of the CSV file contains representative data for type inference.
- The delimiter used is a space (`' '`), which should match the format of the CSV file.
- Ensure that the PostgreSQL database is running and the credentials are correct.
- The script does not handle cases where the table already exists; running it multiple times may cause errors.

## Potential Improvements
- Implement error handling for database operations.
- Check for existing tables before creating a new one.
- Allow user input for database credentials instead of hardcoding them.
- Add logging to monitor execution progress.

