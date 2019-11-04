import datetime
import json

class structure:
    """
    Object that holds (and builds) a cml class
    """
    def __init__(self,name="name",description="description",version="0.0.0",createdDate=datetime.datetime.now()):
        date=createdDate.strftime("%Y%m%d")
        self.name=name
        self.description=description
        self.version=version
        self.createdDate=date
        self.model=None
        self.input=[]
        self.structure=[]
        self.output=None
    def __repr__(self):
        return json.dumps(self.make_map())
    def make_map(self):
        m={}
        m["name"]=self.name
        m["description"]=self.description
        m["version"]=self.version
        m["createdDate"]=self.createdDate
        if self.model!=None:m["model"]=self.model
        if self.input!=None:m["input"]=self.input
        struc=[]
        for op in self.structure:
            struc.append(op.make_map())
        m["structure"]=struc
        m["output"]=self.output
        return m
    def addOps(self,ops,order=-1):
        if order<0:
            self.structure.append(ops)
        else:
            self.structure[order]=ops
        return self
    def listVars(self):
        l=[]
        for i in self.input:
            l.append(i["label"])
        for o in self.structure:
            l.append(o.output)
        s="["+", ".join(l)+"]"
        return s
    def addInput(self,inpobj):
        self.input.append(inpobj.make_map())
        return self
    def addOutput(self,outobj):
        self.output=outobj.make_map()
        return self

class inpobj:
    """
    the structure of an input object has type,label, dim, and shape
    type (1st) and label(2nd) are required with dim and shape optional
    """
    def __init__(self,typ,label,dim=None,shape=None):
        self.typ=typ
        self.label=label
        self.dimensions=dim
        self.shape=shape
    def make_map(self):
        m={}
        m["type"]=self.typ
        m["label"]=self.label
        if self.dimensions!=None:m["dimensions"]=self.dimensions
        if self.shape!=None:m["shape"]=self.shape
        return m
    
    
class outobj:
    """
    the structure of an input object has type,data
    type (1st) and data (2nd) are required 
    """
    def __init__(self,typ,data):
        self.typ=typ
        self.data=data
    def make_map(self):
        m={}
        m["type"]=self.typ
        m["data"]=self.data
        return m

class operation:
    class inputs:
        def make_map(self):
            return None
    class params:
        def make_map(self):
            return None
    operation=None
    def __init__(self,inputs=None,params=None,output=None,operation="untitled"):
        self.operation=operation
        self.inps=inputs
        self.pars=params
        if output==None:
            output=self.operation+f"{r.randint(0,9999)}"

        self.output=output
    def make_map(self):
        m={}
        m["operation"]=self.operation
        try:
            inpmap=self.inps.make_map()
            m["input"]=inpmap
        except AttributeError: pass
        try: 
            parmap=self.pars.make_map()
            m["params"]=parmap
        except AttributeError: pass
        
        m["output"]=self.output
        return m
    def __repr__(self):
        m=self.make_map()
        if m==None:return json.dumps()
        return json.dumps(m)
    
