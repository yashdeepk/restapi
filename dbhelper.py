
import sqlite3

class dbhelper:

    @staticmethod
    def getValuefromKeyValueString(dict, key):
        if key is None:
            return ""
        elif dict[key] is None:
            return ""
        else:
            return dict[key]

    @staticmethod
    def insert(dbPath, obj):

        pLookup = obj.objectPropertyList

        columnList = ', '.join(map(lambda i: i, pLookup))
        valueList = ', '.join(map(lambda i: "'{val}'".format(val=dbhelper.getValuefromKeyValueString(pLookup, i)), pLookup))

        query = "INSERT INTO {tableName}({columnList}) VALUES({valueList});".format(tableName=obj.objectEntity, columnList=columnList, valueList=valueList)
        print(query)

        conn = dbhelper.initDb(dbPath)
        id = dbhelper.executeReturnId(conn, query)
        dbhelper.closeDb(conn)

        obj.id = id

        return obj

    @staticmethod
    def update(dbPath, obj, whereList):

        pLookup = obj.objectPropertyList
        if len(whereList) > 0:
            whereClause = " WHERE {listString}".format(listString=' AND '.join(map(lambda i: "{col} = '{val}'".format(col=i, val=obj.getValue(i)), whereList)))
        else:
            whereClause = ""

        valueSetList = ', '.join(map(lambda i: "{col} = '{val}'".format(col=i, val=dbhelper.getValuefromKeyValueString(pLookup, i)), pLookup))

        query = "UPDATE {tableName} SET {valueSetList}{whereClause};".format(tableName=obj.objectEntity, valueSetList=valueSetList, whereClause=whereClause)
        print(query)

        conn = dbhelper.initDb(dbPath)
        dbhelper.executeNonQuery(conn, query)
        dbhelper.closeDb(conn)

        return obj

    @staticmethod
    def executeScriptPath(dbPath, scriptPath):

        conn = dbhelper.initDb(dbPath)
        script = dbhelper.loadFile(scriptPath)
        dbhelper.executeScript(conn, script)
        dbhelper.closeDb(conn)

    @staticmethod
    def getExistQuery(obj, propertyTagList):
        pLookup = obj.objectPropertyListWithId
        whereClause = ' AND '.join(map(lambda i: "{col} = '{val}'".format(col=i, val=dbhelper.getValuefromKeyValueString(pLookup, i)), propertyTagList))
        return "SELECT 1 FROM {entity} WHERE {whereClause};".format(entity=obj.objectEntity, whereClause=whereClause)

    @staticmethod
    def getSelectQuery(objType, whereList):
        obj = objType()
        pLookup = obj.objectPropertyListWithId
        columnList = ', '.join(map(lambda i: i, pLookup))
        if len(whereList) > 0:
            whereClause = " WHERE {listString}".format(listString=' AND '.join(map(lambda i: "{col} = '{val}'".format(col=i, val=whereList[i]), whereList)))
        else:
            whereClause = ""

        return "SELECT {columnList} FROM {entity}{whereClause};".format(columnList=columnList, entity=obj.objectEntity, whereClause=whereClause)

    @staticmethod
    def initDb(dbPath):
        conn = sqlite3.connect(
                dbPath,
                detect_types=sqlite3.PARSE_DECLTYPES
            )
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def closeDb(conn):
        conn.commit()
        conn.close()

    @staticmethod
    def execute(conn, query):
        cur = conn.cursor()
        cur.execute(query)

        return cur

    @staticmethod
    def executeIfExist(conn, query):
        cur = dbhelper.execute(conn, query)
        item = cur.fetchone()
        cur.close()

        if item is None:
            return False
        else:
            return True

    @staticmethod
    def executeReturnOne(conn, query):
        cur = dbhelper.execute(conn, query)
        item = cur.fetchone()
        cur.close()

        return item

    @staticmethod
    def executeReturnList(conn, query):
        cur = dbhelper.execute(conn, query)
        return cur.fetchall()

    @staticmethod
    def executeNonQuery(conn, query):
        cur = dbhelper.execute(conn, query)
        cur.close()

    @staticmethod
    def executeReturnId(conn, query):
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        id = cur.lastrowid
        cur.close()

        return id

    @staticmethod
    def executeScript(conn, queryFromScript):
        cur = conn.cursor()
        cur.executescript(queryFromScript)
        cur.close()

    @staticmethod
    def loadFile(filePath):
        data = ""

        with open(filePath, 'r') as filePtr:
            data = filePtr.read().replace('\n', '')

        return data
