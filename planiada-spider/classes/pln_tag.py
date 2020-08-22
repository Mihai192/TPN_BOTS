
pTags = [ ]

class pTag:
    id: int
    pId: int
    name: str

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def save(self):
        pTags.append(self)