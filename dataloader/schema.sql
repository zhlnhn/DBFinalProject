-- Database Project Schema Design:
-- Diya Li, Zhilin Han, Xi Chen, Qianjun Chen

-- we design a Restaurant schema from the yelp restaurant dataset which contains 9k+ records and select 9
-- relevant attributes from 17 attributes.
-- to avoid data redundancy, we remove records without latitude or longitude or average rating score.

CREATE TABLE Restaurant (
    rid INT,
    name VARCHAR(100),
    phone_number VARCHAR(15),
    price INT,
    review_count INT,
    avg_rating DECIMAL NOT NULL,
    CONSTRAINT rating_range CHECK (avg_rating BETWEEN 1 AND 5),
    Primary Key (rid)
);

CREATE TABLE Restaurant_location(
    rid INT,
    address VARHAR(100),
    latitude DECIMAL NOT NULL,
    longitude DECIMAL NOT NULL,
    Primary Key (rid)
)；

CREATE TABLE Restaurant_category (
    rid INT,
    category VARCHAR(20),
    Primary Key (rid,category)
);


-- we design a hotel lodge schema from the Airbnb Open Data in NYC dataset which contains 44.3k
-- records and select 16 relevant attributes from the given 96 attributes.
-- to avoid data redundancy, we remove records without latitude and longitude.

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
  )；
