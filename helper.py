
from flask import abort, jsonify
import json

from dbhelper import dbhelper

class helper:

    def __init__(self, objectType):
        obj = objectType()
        self.objectType = obj.objectType
        self.objectName = obj.objectName
        self.mList = []
        
    emptyFunc = lambda: True

    @staticmethod
    def getList(dbPath, objectType, whereList):

        ilist = helper(objectType)

        query = dbhelper.getSelectQuery(objectType, whereList)
        conn = dbhelper.initDb(dbPath)
        dataList = dbhelper.executeReturnList(conn, query)
        for i in dataList:
            obj = ilist.objectType()
            helper.processObjectProp(obj, lambda iobj, j: iobj.setValue(j, i[j]))
            ilist.append(obj)

        dbhelper.closeDb(conn)

        return ilist

    @staticmethod
    def processObjectProp(obj, func):
        pList = obj.objectPropertyListWithId
        for i in pList:
            func(obj, i)

    @staticmethod
    def ifexist(dbPath, obj, propertyTag, errorStatus):
        query = dbhelper.getExistQuery(obj, propertyTag)
        return helper.checkIfExist(dbPath, query, errorStatus, 0)

    @staticmethod
    def ifnotexist(dbPath, obj, propertyTag, errorStatus):
        query = dbhelper.getExistQuery(obj, propertyTag)
        return helper.checkIfExist(dbPath, query, errorStatus, 1)

    @staticmethod
    def checkIfExist(dbPath, query, errorStatus, statusWhenExist):

        isPassed = True

        conn = dbhelper.initDb(dbPath)
        doesExist = dbhelper.executeIfExist(conn, query)
        dbhelper.closeDb(conn)

        if statusWhenExist == 0:
            if doesExist:
                isPassed = False
                abort(errorStatus)
        else:
            if not doesExist:
                isPassed = False
                abort(errorStatus)

        return isPassed

    def append(self, item):
        self.mList.append(item)

    def serialize(self):
        return json.dumps([i.serializeItem() for i in self.mList])

    def find(self, id):
        subList = helper(self.objectType)
        for i in iter(self.mList):
            if i.id == id:
                subList.append(i)
        return subList
    
    def process(self, listFunc, preFunc, postFunc):
        preFunc()
        for i in self.mList:
            listFunc(i)
        postFunc()

    def processPerProperty(self, propFunc, preFunc, postFunc):
        listFunc = lambda i: i.process(propFunc)
        self.process(listFunc, preFunc, postFunc)
