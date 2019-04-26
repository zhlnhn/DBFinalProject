DROP DATABASE IF EXISTS restaurant_hotel;
CREATE DATABASE restaurant_hotel;

DROP USER IF EXISTS restaurant_hotel_user;
CREATE USER restaurant_hotel_user;

GRANT ALL PRIVILEGES ON DATABASE restaurant_hotel TO restaurant_hotel_user;
