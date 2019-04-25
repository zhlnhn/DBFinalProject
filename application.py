from flask import Flask,jsonify,request
import psycopg2
import psycopg2.extras
from flask_cors import CORS
import json
import sys
from texttable import Texttable
app = Flask(__name__)
CORS(app)
connection_string = "host='localhost' dbname='restaurant_hotel' user='hanzhilin' password=''"
conn = psycopg2.connect(connection_string)
app.config['DEBUG'] = True

def wrap_yelp(tup):
    res={}
    res['name']=tup[0]
    res['category']=tup[1]
    res['price']=str(tup[2])
    res['rating']=str(tup[3])
    res['address']=tup[4]
    res['url']=tup[7]
    mk={'position':{'lat':float(tup[5]),'lng':float(tup[6])}}
    return res,mk
def wrap_airbnb(tup):
    res={}
    res['name']=tup[0]
    res['prop_type']=tup[1]
    res['price']=str(tup[3])
    res['rating']=str(tup[5])
    res['address']=tup[6]
    res['room_type']=tup[2]
    res['accommodates']=tup[4]
    res['url']=tup[9]
    mk={'position':{'lat':float(tup[7]),'lng':float(tup[8])}}
    return res,mk
@app.route("/allAirbnb",methods=['GET','POST'])
def allAirbnb():
    if request.method=='GET':
        cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT a.rid,a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid and a.rid=c.rid LIMIT 10")
        rest_records = cursor.fetchall()
        res=[]
        mks=[]
        for rest in rest_records:
            rid=rest[0]
            cursor.execute("SELECT a.name,a.property_type,a.room_type,a.price,a.accommodates,a.review_scores_rating,b.neighbourhood,b.latitude,b.longitude,a.url FROM Lodging as a, Lodging_location as b,Nearby_pairs as c WHERE a.lid=b.lid AND a.lid=c.lid AND c.rid=%s"%(rid))
            records=cursor.fetchall()
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
        cat=post_data.get('category').lower()
        cat='%'+cat+'%'
        min_price=post_data.get('min_price')
        max_price=post_data.get('max_price')
        min_rating=post_data.get('min_rating')
        max_rating=post_data.get('max_rating')
        max_dist=post_data.get('distance')
        print("SELECT a.rid,a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(min_price,max_price,cat,min_rating,max_rating))
        cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT a.rid,a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(min_price,max_price,cat,min_rating,max_rating))
        rest_records = cursor.fetchall()
        print(len(rest_records))
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
            cursor.execute("SELECT a.name,a.property_type,a.room_type,a.price,a.accommodates,a.review_scores_rating,b.neighbourhood,b.latitude,b.longitude,a.url,c.rid,a.lid FROM Lodging as a, Lodging_location as b,Nearby_pairs as c WHERE a.lid=b.lid AND a.lid=c.lid AND c.rid=%s AND c.distance<%s"%(rid,max_dist))
            records=cursor.fetchall()
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
        cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude,a.url FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid and a.rid=c.rid LIMIT 10")
        records = cursor.fetchall()
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
        print("Here")
        post_data = request.get_json()
        cat=post_data.get('category').lower()
        cat='%'+cat+'%'
        min_price=post_data.get('min_price')
        max_price=post_data.get('max_price')
        min_rating=post_data.get('min_rating')
        max_rating=post_data.get('max_rating')
        cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude,a.url FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(min_price,max_price,cat,min_rating,max_rating))
        records = cursor.fetchall()
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

def query_restaurants(qry):
    tmp=qry.split('\"')
    cat='%'+tmp[1].lower()+'%'
    rest=tmp[2][1:].split(" ")
    rest=[int(x) for x in rest]
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT a.name,b.category,a.price,a.avg_rating,c.address FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(rest[0],rest[1],cat,rest[2],rest[3]))
    records = cursor.fetchall()
    if len(records)==0:
        print("No result found")
        return
    t = Texttable()
    t.add_rows([['Name', 'Category','Price','Rating','Address']]+records)
    print(t.draw())
    return records

def query_lodgings(qry):
    tmp=qry.split('\"')
    nbh='%'+tmp[1].lower()+'%'
    rest=tmp[2][1:].split(" ")
    rest=[int(x) for x in rest]
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT a.name,a.property_type,a.price,a.accommodates,a.review_scores_rating,b.neighbourhood FROM lodging as a, lodging_location as b WHERE a.lid=b.lid AND a.price>=%s AND a.price<=%s AND b.neighbourhood LIKE '%s' AND a.review_scores_rating>=%s AND a.review_scores_rating<=%s"%(rest[0],rest[1],nbh,rest[2],rest[3]))
    records = cursor.fetchall()
    if len(records)==0:
        print("No result found")
        return
    t = Texttable()
    t.add_rows([['Name', 'Property Type','Price','Accommodates','Rating','Neighbourhood']]+records)
    print(t.draw())
    return

def query_lodgings_by_food(qry):
    tmp=qry.split('\"')
    cat='%'+tmp[1].lower()+'%'
    rest=tmp[2][1:].split(" ")
    rest=[float(x) for x in rest]
    max_dist=rest[4]
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT a.rid,a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(rest[0],rest[1],cat,rest[2],rest[3]))
    rest_records = cursor.fetchall()
    print(len(rest_records))
    if len(rest_records)==0:
        print("No result found")
        return
    res=[]
    visited_l=set()
    visited_r=set()
    for rest in rest_records:
        rid=rest[0]
        cursor.execute("SELECT a.name,a.property_type,a.price,a.accommodates,a.review_scores_rating,b.neighbourhood,c.rid,a.lid FROM Lodging as a, Lodging_location as b,Nearby_pairs as c WHERE a.lid=b.lid AND a.lid=c.lid AND c.rid=%s AND c.distance<%s"%(rid,max_dist))
        records=cursor.fetchall()
        for record in records:
            if record[-1] in visited_l or record[-2] in visited_r:
                continue
            visited_l.add(record[-1])
            visited_r.add(record[-2])
            res.append(record[:-2])
    t = Texttable()
    t.add_rows([['Name', 'Property Type','Price','Accommodates','Rating','Neighbourhood']]+res)
    print(t.draw())
    return

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


if __name__ == '__main__':
    if len(sys.argv)>1:
        if sys.argv[1]=='server':
            app.run(debug=True, port=8080)
        elif sys.argv[1]=='both':
            app.run(debug=True, port=8080)
            command_exe()
    else:
        command_exe()
