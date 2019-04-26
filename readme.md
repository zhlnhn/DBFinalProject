1. Airbnb New York (csv file)
● Downloaded dataset from webpage: http://insideairbnb.com/get-the-data.html
2. Yelp NYC (json file)
● Fetched dataset from: http://odds.cs.stonybrook.edu/yelpnyc-dataset/


Setup:
```sh
pip3 install -r requirements.txt
python3 dataloader/load_data.py
```

To run terminal interaction version:
```sh
python application.py
```

To run web application version:
First,
```sh
python application.py server
```
Then, open another terminal enter this folder
```sh
cd airbnb_yelp
npm run dev
```
open localhost:8081/
