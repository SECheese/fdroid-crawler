import urllib
from xml.etree import ElementTree

from pymongo import MongoClient

def insert_into_dictionary(collection ,document):
    if (collection.find({"_id": document['_id']}).count() == 0):
        print(collection.insert_one(document).inserted_id + " has been inserted to db")
    else:
        old = collection.find_one({"_id": document['_id']})
        # merge older versions with new one
        old_versions = old.get('versions')
        old_versions.update(document.get('versions'))
        print(str(collection.update({"_id": document['_id']}, {"$set": {"versions": old_versions}},
                                    upsert=True)) + " id: " + str(document.get('_id')))
    pass


print("Waiting for mongodb connection")
client = MongoClient()
db = client.fdroid
apps = db.apps
print("MongoClient connected successfully")

urllib.urlretrieve("https://f-droid.org/repo/index.xml", "index.xml")
with open('index.xml', 'rt') as f:
    tree = ElementTree.parse(f)
dic = {}

for node in tree.iter('application'):
    temp_dic = {}
    for node2 in node.getchildren():
        temp_dic[str(node2.tag)] = node2.text
    temp_dic['_id'] = node.attrib.get('id')
    dic[node.attrib.get('id')] = temp_dic

for node in tree.iter('application'):
    version_dic = {}
    for node2 in node.getchildren():
        temp2_dic = {}
        if node2.tag == "package":
            temp = ""
            for node3 in node2.getchildren():
                temp2_dic[str(node3.tag)] = node3.text
                if node3.tag == "version":
                    temp = node3.text.replace('.', '_')
            version_dic[temp] = temp2_dic
    dic[node.attrib.get('id')]['versions'] = version_dic

for document in dic.itervalues():
    insert_into_dictionary(apps, document)


