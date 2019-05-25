import pymongo as mongo
import encodings.idna

myclient = mongo.MongoClient("mongodb://localhost:27017/")


def propertyExists(id):
    mydb = myclient["properties"]
    mycol = mydb["rent"]
    myquery = {"_id": id}
    #print(myclient.list_database_names())
    found = mycol.find_one(myquery)
    if found is None:
        return(False)
    else:
        return(True)


def insertOneEntry(data):
    mydb = myclient["properties"]
    mycol = mydb["rent"]
    mycol.insert_one(data)
    

def insertMany(data_list):
    mydb = myclient["properties"]
    mycol = mydb["rent"]
    mycol.insert_one(data_list)


def getPrice(id):
    mydb = myclient["properties"]
    mycol = mydb["rent"]
    mycol.find({"_id": id},{ "price_high": 0 })
    
    
def getAllSaleID():
    mydb = myclient['properties']
    mycol = mydb['sale']
    returnList = list()
    for x in mycol.find({}, {"_id": 1}):
        returnList.append(x["_id"])
    return(returnList)


def getPrice(id):
    mydb = myclient['properties']
    mycol = mydb['sale']
    result = mycol.find_one({"_id": id}, {"price": 1})
    return(result["price"]))

