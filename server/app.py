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
        cat=post_data.get('category')
        cat='%'+cat+'%'
        min_price=post_data.get('min_price')
        max_price=post_data.get('max_price')
        min_rating=post_data.get('min_rating')
        max_rating=post_data.get('max_rating')
        print("SELECT a.name,b.category,a.price,a.avg_rating,c.address FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.id=b.id AND a.id=c.id a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(min_price,max_price,cat,min_rating,max_rating))
        cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(min_price,max_price,cat,min_rating,max_rating))
        records = cursor.fetchall()
        res=[]
        mks=[]
        for record in records:
            tmp=wrap_yelp(record)
            res.append(tmp[0])
            mks.append(tmp[1])

        print("SELECT a.name,b.category,a.price,a.avg_rating,c.address FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.price>=%s AND a.price<=%s AND b.category LIKE %s AND a.avg_rating>=%s AND a.avg_rating<=%s",[min_price,max_price,cat,min_rating,max_rating])
        return jsonify({
            'status': 'success',
            'restaurants': res,
            'markers': mks
        })



if __name__ == '__main__':
    app.run(debug=True, port=8080)
