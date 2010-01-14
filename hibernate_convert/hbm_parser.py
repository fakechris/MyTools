import os
from lxml import etree

def map_java_type(java_type, length):
    if java_type == "java.util.Date" or java_type == "date":
        return "DateField", 0
    elif java_type == "java.lang.Float" or java_type == "float":
        return "FloatField", 0
    elif java_type == "java.lang.Short" or java_type == "short":
        return "SmallIntegerField", length
    elif java_type == "byte" or java_type == "java.lang.Byte": # todo , byte should use 1 byte
        return "SmallIntegerField", 1
    elif java_type == "java.lang.Boolean" or java_type == "boolean":
        return "BooleanField", 0
    elif java_type == "timestamp":
        return "DateTimeField", 0
    elif java_type == "java.lang.Integer" or java_type == "integer" or java_type == "long": # TODO, long type?
        return "IntegerField", length
    elif java_type == "java.lang.String" or java_type == "string":
        if length > 255:
            return "TextField", length
        else:
            if length == 0:
                length = 64 #TODO: default value?
            return "CharField", length    
    print java_type, "not handled"    
    raise "not handled"

def to_lxml(filename):
    f = file(filename, "r")
    root_node = etree.parse(f)
    f.close()
    return root_node

def get_len(l):
    if not l:
        return 0
    else:
        return int(l)

def parse_property_node(property_node):
    type = property_node.get("type")
    col = property_node.find("column")
    if col is not None:
        length = get_len(col.get("length"))
        not_null = col.get("not-null") is not None
        name = col.get("name")
    else:
        length = get_len(property_node.get("length"))
        not_null = col.get("not-null") is not None
        name = property_node.get("name")
    return name, not_null, map_java_type(type, length)

class HbmParser:
    def __init__(self, root_node):
        self.root_node = root_node
        
        self.table_name= None
        self.name = None
        self.id = None
        self.columns = []
        try:
            self.table_name = root_node.find("class").get("table")
            self.name = root_node.find("class").get("name")
        except:
            return
        
        try:
            try:
                self.id = root_node.find("class//id//column").get("name")                
            except:            
                self.id = root_node.find("class//id").get("column")
            self.columns = [parse_property_node(n) for n in root_node.findall("class//property")]
        except:                    
            self.columns = [parse_property_node(n) for n in root_node.findall("class//composite-id//key-property")]
            
    def generate_django_code(self):
        result = ""
        if self.name is not None:
            result += "class %s(models.Model):\n" % self.table_name            
            result += "\t%s = models.IntegerField(unique=True)\n" % self.id
            for name, not_null, (type, length) in self.columns:
                props = []
                if length:
                    props.append("max_length=%s" % length)
                if not not_null:
                    props.append("null=True")
                result += "\t%s = models.%s(%s)\n" % (name, type, ",".join(props))
            result += "\n\tclass Meta:\n"
            result += "\t\tdb_table = '%s'\n\n" % self.table_name  
            
        return result
            
        
if __name__ == "__main__":
    #process all hbms
    xml_path = r"""D:\workspace\b2c\src\cn\j\b2c\domain\\"""
    files = [xml_path+x for x in os.listdir(xml_path) if x.endswith("xml")]
    for f in files:        
        h = HbmParser(to_lxml(f))
        #print h.columns, h.id, h.table_name
        print h.generate_django_code()
            
        
    
        
        

