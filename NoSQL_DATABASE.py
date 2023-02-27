import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["bankatadb"]

collection_customers = mydb["customers"]
collection_items = mydb["items"]
collection_bougth_item = mydb["bought_items"]

customers_data =[{"first_name":"Bruce","last_name":"Wayne"},
{"first_name":"Clark","last_name":"Kents"},
{"first_name":"Tony","last_name":"Stark"}]

items_data=[{"title":"USM","price":10.2},
{"title":"Mouse","price":12.23},
{"title":"Monitor","price":199.99}]

bought_data = [{"Order_number":1234,"order_date":"2020-03-02T01:11:18.965Z","final_amount":300},
{"Order_number":5643,"order_date":"2020-03-02T01:11:18.965Z","final_amount":3600},
{"Order_number":6453,"order_date":"2020-03-02T01:11:18.965Z","final_amount":454}]

insert_customers_data = collection_customers.insert_many(customer_data)
insert_items_data = collection_items.insert_many(items_data)
insert_bought_data = collection_items.insert_many(bought_data)

print(insert_customers_data.inserted_ids)
print(insert_items_data.inserted_ids)
print(insert_bought_data.inserted_ids)