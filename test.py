import psycopg2
import psycopg2.extras
def wrap_airbnb(tup):
    print(tup)
    res={}
    res['name']=tup[0]
    res['category']=tup[1]
    res['price']=tup[2]
    res['rating']=tup[3]
    res['address']=tup[4]
    return res

def main():
    connection_string = "host='localhost' dbname='restaurant_hotel' user='hanzhilin' password=''"
    conn = psycopg2.connect(connection_string)
    cursor=conn.cursor()
    cursor.execute("SELECT a.name,b.category,a.price,a.avg_rating,c.address FROM Restaurant as a, Restaurant_category as b, Restaurant_location as c WHERE a.rid=b.rid and a.rid=c.rid")
    records = cursor.fetchall()
    return [wrap_airbnb(record) for record in records]

print(main()[0])
