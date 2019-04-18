import pymongo as mongo

myclient = mongo.MongoClient("mongodb://localhost:27017/")


def propertyExists(id):
    mydb = myclient["properties"]
    mycol = mydb["sale"]
    myquery = {"_id": id}
    #print(myclient.list_database_names())
    found = mycol.find_one(myquery)
    if found is None:
        return(False)
    else:
        return(True)


def insertOneEntry(data):
    mydb = myclient["properties"]
    mycol = mydb["sale"]
    mycol.insert_one(data)
    

def insertMany(data_list):
    mydb = myclient["properties"]
    mycol = mydb["sale"]
    mycol.insert_one(data_list)


