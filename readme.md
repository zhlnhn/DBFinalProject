# Note
We have changed our dataset selections for the reason that there were 2 empty columns (latitude, longitude) in NYC parking tickets dataset. Please regrade our schema part. Thanks!

# Github link
https://github.com/zhlnhn/DBFinalProject

# Dataset source:
1. Airbnb New York (csv file)
● Downloaded dataset from webpage: http://insideairbnb.com/get-the-data.html
2. Yelp NYC (json file)
● Fetched dataset from: http://odds.cs.stonybrook.edu/yelpnyc-dataset/

# Our csv:
[yelp](https://drive.google.com/uc?export=download&id=1aMbNGpvAesBZZ43EBUcmu3HDfn8uQqoe)
[airbnb](https://drive.google.com/uc?export=download&id=1m7OQqGFD5GI-rvlT_talJany4-_GTKcn)
[airbnb address](https://drive.google.com/uc?export=download&id=1U0dC36tkSEAzX7PArwJpSdvslge03XpD)

# Setup:
- install packages
```sh
cd DBFinalProject
pip3 install -r requirements.txt
```
- load data
```sh
psql <dataloader/setup.sql
python3 dataloader/load_data.py
```


# To run terminal interaction version:
```sh
python application.py
```

# To run web application version:
You have to have npm installed and run
```sh
cd airbnb_yelp
npm install
```
Then, get back to DBFinalProject folder to run backend server
```sh
python application.py server
```
Then, open **another terminal**(don't close the first one) enter this folder to run frontend
```sh
cd airbnb_yelp
npm run dev
```
open [localhost:8081](localhost:8081/airbnb) in browser
