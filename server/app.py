from flask import Flask,jsonify,request
from models import db
import psycopg2
import psycopg2.extras
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
POSTGRES = {
    'user': 'restaurant_hotel',
    'pw': '',
    'db': 'restaurant_hotel',
    'host': 'localhost',
    'port': '5432',
}
connection_string = "host='localhost' dbname='restaurant_hotel' user='hanzhilin' password=''"
conn = psycopg2.connect(connection_string)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

def wrap_yelp(tup):
    res={}
    res['name']=tup[0]
    res['category']=tup[1]
    res['price']=str(tup[2])
    res['rating']=str(tup[3])
    res['address']=tup[4]
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
            cursor.execute("SELECT a.name,a.property_type,a.room_type,a.price,a.accommodates,a.review_scores_rating,b.neighbourhood,b.latitude,b.longitude FROM Lodging as a, Lodging_location as b,Nearby_pairs as c WHERE a.lid=b.lid AND a.lid=c.lid AND c.rid=%s"%(rid))
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
            cursor.execute("SELECT a.name,a.property_type,a.room_type,a.price,a.accommodates,a.review_scores_rating,b.neighbourhood,b.latitude,b.longitude,c.rid,a.lid FROM Lodging as a, Lodging_location as b,Nearby_pairs as c WHERE a.lid=b.lid AND a.lid=c.lid AND c.rid=%s AND c.distance<%s"%(rid,max_dist))
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
def ping():
    if request.method == 'GET':
        cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid and a.rid=c.rid LIMIT 10")
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
        cursor.execute("SELECT a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(min_price,max_price,cat,min_rating,max_rating))
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



if __name__ == '__main__':
    app.run(debug=True, port=8080)
