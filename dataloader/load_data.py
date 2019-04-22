import psycopg2
import psycopg2.extras
import csv
import urllib3
import io
import ast
from math import cos, asin, sqrt
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return round(12742 * asin(sqrt(a)),2) #2*R*asin...
# get data from url::
files = open('dataset.txt', 'r').readlines()

## build connection

conn = psycopg2.connect("host=localhost dbname=restaurant_hotel user=hanzhilin")
cur = conn.cursor()
cur.execute("""
    DROP SCHEMA IF EXISTS eat_sleep CASCADE;
    CREATE SCHEMA eat_sleep;
    DROP TABLE IF EXISTS Restaurant;
    DROP TABLE IF EXISTS Restaurant_location;
    DROP TABLE IF EXISTS Restaurant_category;
    DROP TABLE IF EXISTS Lodging;
    DROP TABLE IF EXISTS Lodging_location;
    """)

cur.execute("""
    CREATE TABLE Restaurant (
        rid INT,
        name VARCHAR(100),
        phone_number VARCHAR(15),
        price INT DEFAULT 0,
        review_count INT,
        avg_rating DECIMAL NOT NULL,
        CONSTRAINT rating_range CHECK (avg_rating BETWEEN 1 AND 5),
        Primary Key (rid)
        );
    CREATE TABLE Restaurant_location(
      rid INT,
      address VARCHAR(100),
      latitude DECIMAL NOT NULL,
      longitude DECIMAL NOT NULL,
      Primary Key (rid)
    );

    CREATE TABLE Restaurant_category (
      rid INT,
      category VARCHAR(50),
      Primary Key (rid,category)
    );

    CREATE TABLE Lodging (
        lid INT,
        name VARCHAR(200),
        neighbourhood VARCHAR(100),
        price DECIMAL(10,2),
        weekly_price DECIMAL(10,2),
        property_type VARCHAR(50),
        room_type VARCHAR(100),
        monthly_price DECIMAL(10,2),
        accommodates INT,
        number_of_reviews INT,
        review_scores_rating DECIMAL DEFAULT NULL,
        review_scores_location DECIMAL DEFAULT NULL,
        Primary Key (lid)
    );

    CREATE TABLE Lodging_location (
        lid INT,
        neighbourhood VARCHAR(100),
        latitude DECIMAL NOT NULL,
        longitude DECIMAL NOT NULL,
        Primary Key (lid)
    );
    CREATE TABLE Nearby_pairs (
        lid INT,
        rid INT,
        distance DECIMAL(10,2),
        CONSTRAINT distance_range CHECK (distance BETWEEN 0 AND 3),
        Primary Key(lid,rid)
    )
""")

# ['CAMIS', 'id', 'name', 'url', 'phone',
# 'latitude', 'longitude', 'review_count', 'price', 'rating',
# 'transactions', 'categories', 'address', 'city', 'state', 'zip_code']


url = files[0].strip()
http = urllib3.PoolManager()
response = http.request('GET', url)
reader = csv.reader(io.TextIOWrapper(io.BytesIO(response.data), encoding='utf-8'))
print("insert yelp restaurant data into restaurant tables:\n")

yelp_loc={}

ii = 0
# with open('yelp.csv') as ifile:
# read = csv.reader(ifile)
# skip header
next(reader)
for row in reader:
    # print (row)
    if len(row[8]) == 0:
        price = 0
    else:
        price = row[8]
    insertRow1 = [int(row[0]), row[2], row[4], price, row[7], row[9]]
    insertRow2 = [int(row[0]), row[12], row[5], row[6]]
    yelp_loc[int(row[0])]=(row[5], row[6])
    cur.execute(
                "INSERT INTO Restaurant VALUES (%s, %s, %s, %s, %s, %s)", insertRow1
    )
    cur.execute(
                "INSERT INTO  Restaurant_location VALUES  (%s, %s, %s, %s)", insertRow2
    )
    if len(row[11]) != 0:
        categories = ast.literal_eval(row[11])
        for category in categories:
            insertRow3 = [int(row[0]), category]
            # print(insertRow2, insertRow3)
            cur.execute(
                        "INSERT INTO Restaurant_category VALUES (%s, %s)", insertRow3
            )
    ii += 1
    if ii > 5000:
         break
print("Done inserting %d records in yelp dataset\n" % ii)


# id,name,listing_url,neighbourhood,zipcode,price, weekly_price,\
# property_type,room_type,monthly_price,accommodates,number_of_reviews,review_scores_rating,review_scores_location
#

url = files[1].strip()
http = urllib3.PoolManager()
response = http.request('GET', url)
reader = csv.reader(io.TextIOWrapper(io.BytesIO(response.data), encoding='utf-8'))
print("insert airbnb data into Lodging tables\n")

ii = 0
# with open('airbnb.csv') as ifile:
#     reader = csv.reader(ifile)

# skip header
next(reader)
for row in reader:
    # print(row)
    name = row[1]
    if len(name) >= 200:
        continue
    price = row[5].replace('$', '').replace(',', '')
    week_price = row[6].replace('$', '').replace(',', '')
    mon_price = row[9].replace('$', '').replace(',', '')
    if len(mon_price) == 0:
        mon_price = 0.0
    if len(week_price) == 0:
        week_price = 0.0
    review_scores_rating = 0.0
    review_scores_location = 0.0

    if len(row[12]) > 0:
        review_scores_rating = row[12]
    if len(row[13]) > 0:
        review_scores_location = row[13]

    insertRow1 = [int(row[0]), row[1], row[3], price, week_price, row[7], row[8], mon_price, row[10], row[11], review_scores_rating, review_scores_location]
    # print(insertRow1)
    cur.execute(
        "INSERT INTO Lodging VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", insertRow1
    )
    ii += 1
    if ii > 5000:
         break
print("Done inserting %d records in airbnb dataset\n" % ii)


url = files[2].strip()
http = urllib3.PoolManager()
response = http.request('GET', url)
reader = csv.reader(io.TextIOWrapper(io.BytesIO(response.data), encoding='utf-8'))
print("insert airbnb address data into Lodging_location tables:\n")

ii = 0
#id,neighbourhood,zipcode,latitude,longitude

# with open('airbnb_address.csv') as ifile:
#     read = csv.reader(ifile)

next(reader)
kk=0
for row in reader:
    # print(row)
    insertRow1 = [int(row[0]), row[1], row[3], row[4]]
    # print(insertRow1)
    for rid in yelp_loc.keys():
        lat_y,lng_y=yelp_loc[rid]
        dist=distance(float(lat_y),float(lng_y),float(insertRow1[2]),float(insertRow1[3]))
        if abs(dist)<=2:
            cur.execute(
                "INSERT INTO Nearby_pairs VALUES (%s, %s, %s)"%(insertRow1[0],rid,abs(dist))
                )
            print(kk,dist)
            kk+=1
            if kk>=100000:
                break

    cur.execute(
        "INSERT INTO Lodging_location VALUES (%s, %s, %s, %s)", insertRow1
        )
    ii += 1
    if ii > 5000:
         break
print("Done inserting %d records in airbnb address dataset\n" % ii)

conn.commit()
