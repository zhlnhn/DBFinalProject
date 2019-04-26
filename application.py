from flask import Flask,jsonify,request
import psycopg2
import psycopg2.extras
from flask_cors import CORS
import json
import sys
from database import query_lodgings_by_food,query_lodgings,query_restaurants
from database import server_all_restaurant,server_restaurant
from database import *
app = Flask(__name__)
CORS(app)
connection_string = "host='localhost' dbname='restaurant_hotel' user='restaurant_hotel' password=''"
conn = psycopg2.connect(connection_string)
app.config['DEBUG'] = True


@app.route("/allAirbnb",methods=['GET','POST'])
def allAirbnb():
    if request.method=='GET':
        rest_records = server_all_restaurant_id()
        res=[]
        mks=[]
        for rest in rest_records:
            rid=rest[0]
            records=server_airbnb_id(rid)
            for record in records:
                tmp=wrap_airbnb(record)
                res.append(tmp[0])
                mks.append(tmp[1])
        return jsonify({
            'status': 'success',
            'lodgings': res,
            'markers': mks
        })
    else:
        post_data = request.get_json()
        max_dist=post_data.get('distance')
        rest_records = server_airbnb(post_data)
        #print(len(rest_records))
        if len(rest_records)==0:
            return jsonify({
                'status': 'fail',
                'lodgings': [],
                'markers': []
            })
        res=[]
        mks=[]
        visited_l=set()
        visited_r=set()
        for rest in rest_records:
            rid=rest[0]
            records=server_airbnb_id_distance(rid,max_dist)
            for record in records:
                if record[-1] in visited_l or record[-2] in visited_r:
                    continue
                visited_l.add(record[-1])
                visited_r.add(record[-2])
                tmp=wrap_airbnb(record)
                res.append(tmp[0])
                mks.append(tmp[1])
        return jsonify({
            'status': 'success',
            'lodgings': res,
            'markers': mks
        })


@app.route("/allCategory",methods=['GET'])
def allCategory():
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT DISTINCT category FROM restaurant_category")
    records=cursor.fetchall()
    res = [record[0] for record in records]
    return jsonify({
        'status': 'success',
        'restaurants': res
    })


@app.route("/allRestaurant",methods=['GET','POST'])
def allRestaurant():
    if request.method == 'GET':
        records = server_all_restaurant()
        res=[]
        mks=[]
        for record in records:
            tmp=wrap_yelp(record)
            res.append(tmp[0])
            mks.append(tmp[1])
        return jsonify({
            'status': 'success',
            'restaurants': res,
            'markers': mks
        })
    else:
        post_data = request.get_json()
        records=server_restaurant(post_data)
        if len(records)==0:
            return jsonify({
                'status': 'fail',
                'restaurants': [],
                'markers': []
            })
        res=[]
        mks=[]
        for record in records:
            tmp=wrap_yelp(record)
            res.append(tmp[0])
            mks.append(tmp[1])
        return jsonify({
            'status': 'success',
            'restaurants': res,
            'markers': mks
        })


def command_exe():
    state=''
    while state!='9':
        state=input("""Please Enter:
1) help
2) Query Restaurants (<Category> <min_price> <max_price> <min_rating> <max_rating>)
3) Query Airbnbs (<Neighbourhood> <min_price> <max_price> <min_rating> <max_rating>)
4) Query Airbnbs based on restaurant preference  (<Category> <min_price> <max_price> <min_rating> <max_rating> <distance>)
9) Exit
""")
        print("user input is",state)
        if state=='1':
            continue
        elif state=='2':
            query=input("Query Restaurants (Example:\"hotdog\" 2 3 3 5)\n")
            query_restaurants(query)
        elif state=='3':
            query=input("Query Airbnbs (Example: \"Midtown\" 200 300 90 100)\n")
            query_lodgings(query)
        elif state=='4':
            query=input("Query Airbnbs based on restaurant preference (<Category> <min_price> <max_price> <min_rating> <max_rating> <distance>)\n (Example: \"hotdog\" 2 3 3 5 1)\n")
            query_lodgings_by_food(query)

def start_server():
    app.run(debug=True, port=8080)


if __name__ == '__main__':
    if len(sys.argv)>1:
        if sys.argv[1]=='server':
            start_server()
        else:
            print("invalid argument!")
    else:
        command_exe()
