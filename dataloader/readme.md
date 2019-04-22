# Project

We use `load_data.py` to load predefined schema and insert data into table which accessed from urls.

## What's in the folder?

`load_data.py` contains SQL code to generate predefined schema and SQL query to insert records in datasets into `restaurant_hotel` database. 

`dataset.txt` a text file containing the URL for each of our datasets (yelp dataset, airbnb dataset and airbnb_address dataset), one per line. 

`readme.md` readme file for data loading instruction.

## Setup
Run below command in terminal:
`psql < setup.sql`

## Execution
Run below command in terminal:
`python3 load_data.py`

Drop table if it exists for multiple runs.

Attributes are preprocessed for correct insertion.

## Change of Schema for robustness
