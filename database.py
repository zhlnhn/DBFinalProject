import psycopg2
import psycopg2.extras
from texttable import Texttable
connection_string = "host='localhost' dbname='restaurant_hotel' user='restaurant_hotel_user' password=''"
conn = psycopg2.connect(connection_string)
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

def server_all_restaurant():
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude,a.url FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid and a.rid=c.rid LIMIT 10")
    return cursor.fetchall()

def server_all_restaurant_id():
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT a.rid,a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude,a.url FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid and a.rid=c.rid LIMIT 10")
    return cursor.fetchall()

def server_restaurant(post_data):
    cat=post_data.get('category').lower()
    cat='%'+cat+'%'
    min_price=post_data.get('min_price')
    max_price=post_data.get('max_price')
    min_rating=post_data.get('min_rating')
    max_rating=post_data.get('max_rating')
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude,a.url FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(min_price,max_price,cat,min_rating,max_rating))
    records = cursor.fetchall()
    return records

def server_airbnb_id(rid):
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT a.name,a.property_type,a.room_type,a.price,a.accommodates,a.review_scores_rating,b.neighbourhood,b.latitude,b.longitude,a.url FROM Lodging as a, Lodging_location as b,Nearby_pairs as c WHERE a.lid=b.lid AND a.lid=c.lid AND c.rid=%s"%(rid))
    records=cursor.fetchall()
    return records

def server_airbnb(post_data):
    cat=post_data.get('category').lower()
    cat='%'+cat+'%'
    min_price=post_data.get('min_price')
    max_price=post_data.get('max_price')
    min_rating=post_data.get('min_rating')
    max_rating=post_data.get('max_rating')
    max_dist=post_data.get('distance')
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print("SELECT a.rid,a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(min_price,max_price,cat,min_rating,max_rating))
    cursor.execute("SELECT a.rid,a.name,b.category,a.price,a.avg_rating,c.address,c.latitude, c.longitude FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid AND a.rid=c.rid AND a.price>=%s AND a.price<=%s AND b.category LIKE '%s' AND a.avg_rating>=%s AND a.avg_rating<=%s"%(min_price,max_price,cat,min_rating,max_rating))
    rest_records = cursor.fetchall()
    return rest_records

def server_airbnb_id_distance(rid,max_dist):
    cursor=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT a.name,a.property_type,a.room_type,a.price,a.accommodates,a.review_scores_rating,b.neighbourhood,b.latitude,b.longitude,a.url,c.rid,a.lid FROM Lodging as a, Lodging_location as b,Nearby_pairs as c WHERE a.lid=b.lid AND a.lid=c.lid AND c.rid=%s AND c.distance<%s"%(rid,max_dist))
    return cursor.fetchall()
