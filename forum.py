from flask import jsonify

class forum:

    def __init__(self):

        self._objectLookup = {}
        self._objectLookup[self._id_tag] = None
        self._objectLookup[self._objectName_tag] = self.__class__.__name__
        self._objectType = self.__class__
        self.id = None
        self.objectLookup[self.name_tag] = None
        self.objectLookup[self.creator_tag] = None

    name_tag = "name"
    @property
    def name(self):
        return self.objectLookup[self.name_tag]

    @name.setter
    def name(self, value):
        self.objectLookup[self.name_tag] = value
    
    creator_tag = "creator"
    @property
    def creator(self):
        return self.objectLookup[self.creator_tag]

    @creator.setter
    def creator(self, value):
        self.objectLookup[self.creator_tag] = value

    _id_tag = "id"
    _objectName_tag = "objectName"

    @staticmethod
    def dictGetSafe(dict, key):
        if key in dict:
            return dict[key]
        else:
            return None
    @property
    def objectLookup(self):
        return self._objectLookup

    @property
    def objectPropertyList(self):
        pLookup = {}
        for k, v in self._objectLookup.items():
            if not self.isInstrinsic(k):
                pLookup[k] = v

        return pLookup

    @property
    def objectPropertyListWithId(self):
        pLookup = {}
        for k, v in self._objectLookup.items():
            if k != self._objectName_tag:
                pLookup[k] = v

        return pLookup

    #id
    @property
    def id(self):
        return self._objectLookup[self._id_tag]

    @id.setter
    def id(self, value):
        self._objectLookup[self._id_tag] = value

    #objectName
    @property
    def objectName(self):
        return self._objectLookup[self._objectName_tag]

    @objectName.setter
    def objectName(self, value):
        self._objectLookup[self._objectName_tag] = value

    @property
    def objectEntity(self):
        return "{o}s".format(o=self._objectLookup[self._objectName_tag])

    @property
    def objectType(self):
        return self._objectType

    #functions
    def process(self, func):
        pList = self.objectPropertyListWithId
        for i in pList:
            func(self, i)

    def getValue(self, tag):
        return self._objectLookup[tag]

    def setValue(self, tag, value):
        self._objectLookup[tag] = value

    def isInstrinsic(self, tag):
        return ((tag == self._id_tag)  or (tag == self._objectName_tag))

    def serializeItem(self):
        return self.objectPropertyListWithId

    def serializeJson(self):
        return jsonify(self.serializeItem())

    @staticmethod
    def deserializeObject(jsonObj, objectType):

        obj = objectType()

        pLookup = obj.objectPropertyList

        for k in pLookup.keys():
            obj.setValue(k, forum.dictGetSafe(jsonObj, k))

        return obj


