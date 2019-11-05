import datetime
import json
import random as r

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
    def addInput(self,inobj):
        self.input.append(inobj.make_map())
        return self
    def addOutput(self,outobj):
        self.output=outobj.make_map()
        return self

class inobj:
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
    
class map2table(operation):
	"""
	convert a map to a matrix
	"""
	class inputs:
		"""
		inputs's possible keys:
			map - contains map to be converted to table
			colOrder - list of the columns to be merged into table (ORDER MATTERS)
		"""
		def __init__(self,map=None,colOrder=None):
			"""
			initializing inputs
			"""
			self.map=map
			self.colOrder=colOrder
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['map']=self.map
			m['colOrder']=self.colOrder
			return m
	class params:
		"""
		params's possible keys:
			axis - the orientation of the table (0=vertical/column, 1=horizontal/row)
		"""
		def __init__(self,axis=None):
			"""
			initializing params
			"""
			self.axis=axis
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['axis']=self.axis
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize map2table operation and define inputs, parameters, and outputs"""
		self.operation="map2table"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class groupBy(operation):
	"""
	group by a given column in an axis and aggregate the value of another column (like SQL)
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - data to group
			groupKeys - Column by which to group.
		"""
		def __init__(self,data=None,groupKeys=None):
			"""
			initializing inputs
			"""
			self.data=data
			self.groupKeys=groupKeys
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			m['groupKeys']=self.groupKeys
			return m
	class params:
		"""
		params's possible keys:
			asIndex - 
			axis - (0=vertical/column, 1=horizontal/row)
		"""
		def __init__(self,asIndex=None,axis=None):
			"""
			initializing params
			"""
			self.asIndex=asIndex
			self.axis=axis
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['asIndex']=self.asIndex
			if self.axis!=None:m['axis']=self.axis
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize groupBy operation and define inputs, parameters, and outputs"""
		self.operation="groupBy"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class reshape(operation):
	"""
	change the dimensionality of a matrix without changing the underlying data
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - data to be reshaped
			shape - array of integers where: 1) length of array  number of  output dimensions and 2) each integer specifies the number of values for a given dimension.  If the integer is -1 that dimension is sized to fit the data. i.e. [-1,2,3] for a 24 value array means a 4x2x3 matrix
		"""
		def __init__(self,data=None,shape=None):
			"""
			initializing inputs
			"""
			self.data=data
			self.shape=shape
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			m['shape']=self.shape
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize reshape operation and define inputs, parameters, and outputs"""
		self.operation="reshape"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class transpose(operation):
	"""
	transpose a matrix
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - Matrix to be transposed
		"""
		def __init__(self,data=None):
			"""
			initializing inputs
			"""
			self.data=data
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize transpose operation and define inputs, parameters, and outputs"""
		self.operation="transpose"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class dropCol(operation):
	"""
	Remove cols from matrix or map
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - original data set
			cols - indices or key for column in map or matrix to be removed
		"""
		def __init__(self,data=None,cols=None):
			"""
			initializing inputs
			"""
			self.data=data
			self.cols=cols
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			m['cols']=self.cols
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize dropCol operation and define inputs, parameters, and outputs"""
		self.operation="dropCol"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class cast(operation):
	"""
	Convert the base datatype of a data structure or datatype from one base type to another (i.e. [int32,int32] to [flat64,float64]), it is useful to note that maps of arrays are allowed and handle by the specification.
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - input data to be cast.
			toType - String depicting which datatype to cast to.  Allowed:int64,float64,string,int32,float32,boolean
		"""
		def __init__(self,data=None,toType=None):
			"""
			initializing inputs
			"""
			self.data=data
			self.toType=toType
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			m['toType']=self.toType
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize cast operation and define inputs, parameters, and outputs"""
		self.operation="cast"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class pivot(operation):
	"""
	group by a given column in an axis and aggregate the value of another column (like SQL)
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - Column(s) to use for populating new frame’s values.
		"""
		def __init__(self,data=None):
			"""
			initializing inputs
			"""
			self.data=data
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			return m
	class params:
		"""
		params's possible keys:
			index - Name of columns which value to be used to make new frame’s index
			columns - Name of columns which value to be used to make new frame’s columns.
			aggregate - Map key is groupKey, map value is aggregate function. Currently support Sum, Count, Mean, Min, Max
		"""
		def __init__(self,index=None,columns=None,aggregate=None):
			"""
			initializing params
			"""
			self.index=index
			self.columns=columns
			self.aggregate=aggregate
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['index']=self.index
			m['columns']=self.columns
			m['aggregate']=self.aggregate
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize pivot operation and define inputs, parameters, and outputs"""
		self.operation="pivot"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class addCol2Table(operation):
	"""
	Add a column to a matrix
	"""
	class inputs:
		"""
		inputs's possible keys:
			matrix - matrix to be expanded
			col - col to be added of same length as matrix's second dimention
		"""
		def __init__(self,matrix=None,col=None):
			"""
			initializing inputs
			"""
			self.matrix=matrix
			self.col=col
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['matrix']=self.matrix
			m['col']=self.col
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize addCol2Table operation and define inputs, parameters, and outputs"""
		self.operation="addCol2Table"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class flatten(operation):
	"""
	reduce multidimensional lists to single dimension
	"""
	class inputs:
		"""
		inputs's possible keys:
			matrix - matrix to be flattened
		"""
		def __init__(self,matrix=None):
			"""
			initializing inputs
			"""
			self.matrix=matrix
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['matrix']=self.matrix
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize flatten operation and define inputs, parameters, and outputs"""
		self.operation="flatten"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class table2map(operation):
	"""
	convert a matrix to a map by adding a name to each column
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - contains map to be converted to table
			colKeys - list of keys for map that correspond to 0 to n columns in table
		"""
		def __init__(self,data=None,colKeys=None):
			"""
			initializing inputs
			"""
			self.data=data
			self.colKeys=colKeys
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			m['colKeys']=self.colKeys
			return m
	class params:
		"""
		params's possible keys:
			axis - the orientation of the table (0=vertical/column, 1=horizontal/row)
		"""
		def __init__(self,axis=None):
			"""
			initializing params
			"""
			self.axis=axis
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.axis!=None:m['axis']=self.axis
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize table2map operation and define inputs, parameters, and outputs"""
		self.operation="table2map"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class join(operation):
	"""
	group by a given column in an axis and aggregate the value of another column (like SQL)
	"""
	class inputs:
		"""
		inputs's possible keys:
			data0 - contains matrices or maps of inputs
			data1 - contains matrices or maps of inputs
		"""
		def __init__(self,data0=None,data1=None):
			"""
			initializing inputs
			"""
			self.data0=data0
			self.data1=data1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data0']=self.data0
			m['data1']=self.data1
			return m
	class params:
		"""
		params's possible keys:
			on - either index or the col name/number
			how - sql join types
		"""
		def __init__(self,on=None,how=None):
			"""
			initializing params
			"""
			self.on=on
			self.how=how
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.on!=None:m['on']=self.on
			m['how']=self.how
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize join operation and define inputs, parameters, and outputs"""
		self.operation="join"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class scale(operation):
	"""
	resizes an image
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - data to get scale
			scaler - data to get scale
		"""
		def __init__(self,data=None,scaler=None):
			"""
			initializing inputs
			"""
			self.data=data
			self.scaler=scaler
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			m['scaler']=self.scaler
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize scale operation and define inputs, parameters, and outputs"""
		self.operation="scale"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class normalize(operation):
	"""
	divide all values of array by value (i.e. x/value), if minvalue is given applies (x-minval)/(value-minvalue) where x is the data 
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - data to get mean of
			value - value to normalize with (if starting at 0)
			minval - min value to start normalize with (if not starting at 0)
		"""
		def __init__(self,data=None,value=None,minval=None):
			"""
			initializing inputs
			"""
			self.data=data
			self.value=value
			self.minval=minval
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			m['value']=self.value
			if self.minval!=None:m['minval']=self.minval
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize normalize operation and define inputs, parameters, and outputs"""
		self.operation="normalize"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class multPairWise(operation):
	"""
	for matrices of the same shape multiply corresponding values
	"""
	class inputs:
		"""
		inputs's possible keys:
			matrix0 - first matrix
			matrix1 - second matrix.
		"""
		def __init__(self,matrix0=None,matrix1=None):
			"""
			initializing inputs
			"""
			self.matrix0=matrix0
			self.matrix1=matrix1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['matrix0']=self.matrix0
			m['matrix1']=self.matrix1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize multPairWise operation and define inputs, parameters, and outputs"""
		self.operation="multPairWise"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class norm(operation):
	"""
	determine the geometric length of a vector - output is a float.  If matrix determines magnitude of vectors based upon axis selected - output array of floats.
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - data to get geometric length of
		"""
		def __init__(self,data=None):
			"""
			initializing inputs
			"""
			self.data=data
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			return m
	class params:
		"""
		params's possible keys:
			axis - which axis to use, 0 (horizontal) is default
		"""
		def __init__(self,axis=None):
			"""
			initializing params
			"""
			self.axis=axis
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.axis!=None:m['axis']=self.axis
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize norm operation and define inputs, parameters, and outputs"""
		self.operation="norm"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class mean(operation):
	"""
	takes the mean of an array
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - data to get mean of
		"""
		def __init__(self,data=None):
			"""
			initializing inputs
			"""
			self.data=data
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			return m
	class params:
		"""
		params's possible keys:
			axis - which axis to use, 0 (horizontal) is default
		"""
		def __init__(self,axis=None):
			"""
			initializing params
			"""
			self.axis=axis
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.axis!=None:m['axis']=self.axis
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize mean operation and define inputs, parameters, and outputs"""
		self.operation="mean"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class concat(operation):
	"""
	join two strings together
	"""
	class inputs:
		"""
		inputs's possible keys:
			s0 - first string
			s1 - second string
			slist - list of strings
		"""
		def __init__(self,s0=None,s1=None,slist=None):
			"""
			initializing inputs
			"""
			self.s0=s0
			self.s1=s1
			self.slist=slist
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s0']=self.s0
			m['s1']=self.s1
			m['slist']=self.slist
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize concat operation and define inputs, parameters, and outputs"""
		self.operation="concat"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class levenshteinSimilarity(operation):
	"""
	Add a column to a matrix
	"""
	class inputs:
		"""
		inputs's possible keys:
			s0 - 1 string to get distance of
			s1 - 1 string to get distance of
		"""
		def __init__(self,s0=None,s1=None):
			"""
			initializing inputs
			"""
			self.s0=s0
			self.s1=s1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s0']=self.s0
			m['s1']=self.s1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize levenshteinSimilarity operation and define inputs, parameters, and outputs"""
		self.operation="levenshteinSimilarity"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class lastindex(operation):
	"""
	LastIndex returns the index of the last instance of substr in s, or -1 if substr is not present in s
	"""
	class inputs:
		"""
		inputs's possible keys:
			s0 - string
			s1 - substring
		"""
		def __init__(self,s0=None,s1=None):
			"""
			initializing inputs
			"""
			self.s0=s0
			self.s1=s1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s0']=self.s0
			m['s1']=self.s1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize lastindex operation and define inputs, parameters, and outputs"""
		self.operation="lastindex"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class tolower(operation):
	"""
	ToLower returns a copy of the string s with all Unicode letters mapped to their lower case.
	"""
	class inputs:
		"""
		inputs's possible keys:
			str - string to be made lowercase
		"""
		def __init__(self,str=None):
			"""
			initializing inputs
			"""
			self.str=str
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['str']=self.str
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize tolower operation and define inputs, parameters, and outputs"""
		self.operation="tolower"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class matchregex(operation):
	"""
	whether substring exists in string
	"""
	class inputs:
		"""
		inputs's possible keys:
			s0 - string
			s1 - substring
		"""
		def __init__(self,s0=None,s1=None):
			"""
			initializing inputs
			"""
			self.s0=s0
			self.s1=s1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s0']=self.s0
			m['s1']=self.s1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize matchregex operation and define inputs, parameters, and outputs"""
		self.operation="matchregex"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class count(operation):
	"""
	count number of times substring appears in string
	"""
	class inputs:
		"""
		inputs's possible keys:
			s0 - the string to be searched within
			s1 - the substring being searched for
		"""
		def __init__(self,s0=None,s1=None):
			"""
			initializing inputs
			"""
			self.s0=s0
			self.s1=s1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s0']=self.s0
			m['s1']=self.s1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize count operation and define inputs, parameters, and outputs"""
		self.operation="count"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class replace(operation):
	"""
	Replace returns a copy of the string s with the first n non-overlapping instances of old replaced by new. If n < 0, there is no limit on the number of replacements.
	"""
	class inputs:
		"""
		inputs's possible keys:
			s0 - string
			s1 - string to be replaced
			s2 - string to replace with
			i - number of possible replacements, default all
		"""
		def __init__(self,s0=None,s1=None,s2=None,i=None):
			"""
			initializing inputs
			"""
			self.s0=s0
			self.s1=s1
			self.s2=s2
			self.i=i
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s0']=self.s0
			m['s1']=self.s1
			m['s2']=self.s2
			if self.i!=None:m['i']=self.i
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize replace operation and define inputs, parameters, and outputs"""
		self.operation="replace"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class repeat(operation):
	"""
	Repeat returns a new string consisting of count copies of the string s
	"""
	class inputs:
		"""
		inputs's possible keys:
			s - string to be repeated
			i - the number of repeats
		"""
		def __init__(self,s=None,i=None):
			"""
			initializing inputs
			"""
			self.s=s
			self.i=i
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s']=self.s
			m['i']=self.i
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize repeat operation and define inputs, parameters, and outputs"""
		self.operation="repeat"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class uuid(operation):
	"""
	UUID generates a random UUID according to RFC 4122
	"""
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize uuid operation and define inputs, parameters, and outputs"""
		self.operation="uuid"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class split(operation):
	"""
	Split slices s into all substrings separated by sep and returns a slice of the substrings between those separators
	"""
	class inputs:
		"""
		inputs's possible keys:
			str - string to be seperated
			sep - strings to be seperated at .i.e. ',' , '	', etc.
		"""
		def __init__(self,str=None,sep=None):
			"""
			initializing inputs
			"""
			self.str=str
			self.sep=sep
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['str']=self.str
			m['sep']=self.sep
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize split operation and define inputs, parameters, and outputs"""
		self.operation="split"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class index(operation):
	"""
	Index returns the index of the first instance of substr in s, or -1 if substr is not present in s
	"""
	class inputs:
		"""
		inputs's possible keys:
			s0 - string
			s1 - substring
		"""
		def __init__(self,s0=None,s1=None):
			"""
			initializing inputs
			"""
			self.s0=s0
			self.s1=s1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s0']=self.s0
			m['s1']=self.s1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize index operation and define inputs, parameters, and outputs"""
		self.operation="index"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class toupper(operation):
	"""
	ToUpper returns a copy of the string s with all Unicode letters mapped to their upper case.
	"""
	class inputs:
		"""
		inputs's possible keys:
			str - string to be made upper case
		"""
		def __init__(self,str=None):
			"""
			initializing inputs
			"""
			self.str=str
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['str']=self.str
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize toupper operation and define inputs, parameters, and outputs"""
		self.operation="toupper"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class levenshteinDistance(operation):
	"""
	Add a column to a matrix
	"""
	class inputs:
		"""
		inputs's possible keys:
			s0 - 1 string to get distance of
			s1 - 1 string to get distance of
		"""
		def __init__(self,s0=None,s1=None):
			"""
			initializing inputs
			"""
			self.s0=s0
			self.s1=s1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s0']=self.s0
			m['s1']=self.s1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize levenshteinDistance operation and define inputs, parameters, and outputs"""
		self.operation="levenshteinDistance"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class contains(operation):
	"""
	whether substring exists in string
	"""
	class inputs:
		"""
		inputs's possible keys:
			s0 - string
			s1 - substring
		"""
		def __init__(self,s0=None,s1=None):
			"""
			initializing inputs
			"""
			self.s0=s0
			self.s1=s1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['s0']=self.s0
			m['s1']=self.s1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize contains operation and define inputs, parameters, and outputs"""
		self.operation="contains"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class getStopWords(operation):
	"""
	Gets array of ([stop words](https://en.wikipedia.org/wiki/Stop_words)), by either using a default, or reading from a file.
	"""
	class params:
		"""
		params's possible keys:
			lib - which library stopword list to load
			lang - The language to be used, based on [ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). For example: English='en'.
			fileLoc - path to file that contains list of stop words (1 word per line)
			merge - Whether to merge list from file with file from library
		"""
		def __init__(self,lib=None,lang=None,fileLoc=None,merge=None):
			"""
			initializing params
			"""
			self.lib=lib
			self.lang=lang
			self.fileLoc=fileLoc
			self.merge=merge
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.lib!=None:m['lib']=self.lib
			if self.lang!=None:m['lang']=self.lang
			if self.fileLoc!=None:m['fileLoc']=self.fileLoc
			if self.merge!=None:m['merge']=self.merge
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize getStopWords operation and define inputs, parameters, and outputs"""
		self.operation="getStopWords"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class removeStop(operation):
	"""
	removes Stop words from a string
	"""
	class inputs:
		"""
		inputs's possible keys:
			str - the string to have stop words removed from
		"""
		def __init__(self,str=None):
			"""
			initializing inputs
			"""
			self.str=str
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['str']=self.str
			return m
	class params:
		"""
		params's possible keys:
			lang - The language to be used, based on ISO 639-1 codes https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
		"""
		def __init__(self,lang=None):
			"""
			initializing params
			"""
			self.lang=lang
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.lang!=None:m['lang']=self.lang
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize removeStop operation and define inputs, parameters, and outputs"""
		self.operation="removeStop"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class tokenize(operation):
	"""
	separate text into tokens / words / punctuation.
	"""
	class inputs:
		"""
		inputs's possible keys:
			str - string to tokenize
		"""
		def __init__(self,str=None):
			"""
			initializing inputs
			"""
			self.str=str
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['str']=self.str
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize tokenize operation and define inputs, parameters, and outputs"""
		self.operation="tokenize"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class stem(operation):
	"""
	produces the stem of a word (i.e. running -> run)
	"""
	class inputs:
		"""
		inputs's possible keys:
			str - word to have endings removed
		"""
		def __init__(self,str=None):
			"""
			initializing inputs
			"""
			self.str=str
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['str']=self.str
			return m
	class params:
		"""
		params's possible keys:
			algo - The algorithm to be used
		"""
		def __init__(self,algo=None):
			"""
			initializing params
			"""
			self.algo=algo
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.algo!=None:m['algo']=self.algo
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize stem operation and define inputs, parameters, and outputs"""
		self.operation="stem"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class segment(operation):
	"""
	Seperates a paragraph into sentences.
	"""
	class inputs:
		"""
		inputs's possible keys:
			str - string
		"""
		def __init__(self,str=None):
			"""
			initializing inputs
			"""
			self.str=str
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['str']=self.str
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize segment operation and define inputs, parameters, and outputs"""
		self.operation="segment"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class posTag(operation):
	"""
	Part of speach tagger
	"""
	class inputs:
		"""
		inputs's possible keys:
			str - string
		"""
		def __init__(self,str=None):
			"""
			initializing inputs
			"""
			self.str=str
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['str']=self.str
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize posTag operation and define inputs, parameters, and outputs"""
		self.operation="posTag"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class set(operation):
	"""
	gets unordered array of unique values from original array
	"""
	class inputs:
		"""
		inputs's possible keys:
			arr - the array to be turned into set
		"""
		def __init__(self,arr=None):
			"""
			initializing inputs
			"""
			self.arr=arr
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['arr']=self.arr
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize set operation and define inputs, parameters, and outputs"""
		self.operation="set"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class ifnotin(operation):
	"""
	Given 2 arrays returns the new array with the elements of the first array only if they do not appear in the second array.
	"""
	class inputs:
		"""
		inputs's possible keys:
			arr0 - first array, the one to compare to the 'notin' list
			arr1 - the array for the 'not in' of if not in.
		"""
		def __init__(self,arr0=None,arr1=None):
			"""
			initializing inputs
			"""
			self.arr0=arr0
			self.arr1=arr1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['arr0']=self.arr0
			m['arr1']=self.arr1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize ifnotin operation and define inputs, parameters, and outputs"""
		self.operation="ifnotin"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class ifin(operation):
	"""
	Given 2 arrays returns the new array with the elements of the first array only if they appear in the second array as well.
	"""
	class inputs:
		"""
		inputs's possible keys:
			arr0 - first array, the one to compare to the 'in' list
			arr1 - the array for the 'in' of if in.
		"""
		def __init__(self,arr0=None,arr1=None):
			"""
			initializing inputs
			"""
			self.arr0=arr0
			self.arr1=arr1
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['arr0']=self.arr0
			m['arr1']=self.arr1
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize ifin operation and define inputs, parameters, and outputs"""
		self.operation="ifin"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class concatMap(operation):
	"""
	takes an array of maps and combines them into one.
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - array of maps to be combines into one
		"""
		def __init__(self,data=None):
			"""
			initializing inputs
			"""
			self.data=data
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize concatMap operation and define inputs, parameters, and outputs"""
		self.operation="concatMap"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class replaceValue(operation):
	"""
	Given a map replaces data (key) with map value
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - data to be operated on
			replaceMap - map gives key to replace with value
			replaceKey - what is to be replaced
			replaceValue - what is to be replaced with
		"""
		def __init__(self,data=None,replaceMap=None,replaceKey=None,replaceValue=None):
			"""
			initializing inputs
			"""
			self.data=data
			self.replaceMap=replaceMap
			self.replaceKey=replaceKey
			self.replaceValue=replaceValue
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			if self.replaceMap!=None:m['replaceMap']=self.replaceMap
			if self.replaceKey!=None:m['replaceKey']=self.replaceKey
			if self.replaceValue!=None:m['replaceValue']=self.replaceValue
			return m
	class params:
		"""
		params's possible keys:
			Axis - (0=vertical/column, 1=horizontal/row)
			Col - 
		"""
		def __init__(self,Axis=None,Col=None):
			"""
			initializing params
			"""
			self.Axis=Axis
			self.Col=Col
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.Axis!=None:m['Axis']=self.Axis
			if self.Col!=None:m['Col']=self.Col
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize replaceValue operation and define inputs, parameters, and outputs"""
		self.operation="replaceValue"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class apply(operation):
	"""
	apply a function to every value in a vector or key in a map
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - data to be operated on
			function - the operator to be used as the function, $item to be used as the variable taken from the data variable when defining inputs and params (instance of the loop), output not included in this object since output is in the apply object
		"""
		def __init__(self,data=None,function=None):
			"""
			initializing inputs
			"""
			self.data=data
			self.function=function
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			m['function']=self.function
			return m
	class params:
		"""
		params's possible keys:
			mapOrArray - determines whether the output is an array or a map (input value as key,  response as value)
		"""
		def __init__(self,mapOrArray=None):
			"""
			initializing params
			"""
			self.mapOrArray=mapOrArray
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.mapOrArray!=None:m['mapOrArray']=self.mapOrArray
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize apply operation and define inputs, parameters, and outputs"""
		self.operation="apply"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class oneHotEncoding(operation):
	"""
	convert categorical vector into a set of vectors for each category with a 0/1
	"""
	class inputs:
		"""
		inputs's possible keys:
			data - 2D table to be converted to map
		"""
		def __init__(self,data=None):
			"""
			initializing inputs
			"""
			self.data=data
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['data']=self.data
			return m
	class params:
		"""
		params's possible keys:
			inputColumns - the columns to which one Hot Encodding should be applied
			outputColumns - list of keys for map that correspond to 0 to n columns in table
			keepOrig - The rest of the data in the map/matrix is kept but column used is removed unless keepOrig is true
		"""
		def __init__(self,inputColumns=None,outputColumns=None,keepOrig=None):
			"""
			initializing params
			"""
			self.inputColumns=inputColumns
			self.outputColumns=outputColumns
			self.keepOrig=keepOrig
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['inputColumns']=self.inputColumns
			if self.outputColumns!=None:m['outputColumns']=self.outputColumns
			if self.keepOrig!=None:m['keepOrig']=self.keepOrig
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize oneHotEncoding operation and define inputs, parameters, and outputs"""
		self.operation="oneHotEncoding"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class grayscale(operation):
	"""
	grayscale an image
	"""
	class inputs:
		"""
		inputs's possible keys:
			img - the image to be grayscaled
		"""
		def __init__(self,img=None):
			"""
			initializing inputs
			"""
			self.img=img
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['img']=self.img
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize grayscale operation and define inputs, parameters, and outputs"""
		self.operation="grayscale"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class subSectionToImage(operation):
	"""
	takes a portion of an image and makes it an independent image (i.e. for selecting out a face).  If size from corner is larger than the image the subsection is returned up to the image edge.
	"""
	class inputs:
		"""
		inputs's possible keys:
			img - image to be have subsection removed from
		"""
		def __init__(self,img=None):
			"""
			initializing inputs
			"""
			self.img=img
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['img']=self.img
			return m
	class params:
		"""
		params's possible keys:
			size - the size of the subsection
			lowerLeftCorner - the x,y coordinates (the corner with the lowest x,y vaules)
		"""
		def __init__(self,size=None,lowerLeftCorner=None):
			"""
			initializing params
			"""
			self.size=size
			self.lowerLeftCorner=lowerLeftCorner
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['size']=self.size
			m['lowerLeftCorner']=self.lowerLeftCorner
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize subSectionToImage operation and define inputs, parameters, and outputs"""
		self.operation="subSectionToImage"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class resize(operation):
	"""
	resizes an image
	"""
	class inputs:
		"""
		inputs's possible keys:
			img - the image to be resized, jpg,png, or gif
		"""
		def __init__(self,img=None):
			"""
			initializing inputs
			"""
			self.img=img
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['img']=self.img
			return m
	class params:
		"""
		params's possible keys:
			xsize - the width of the new image, if only xsize included, xsize/ysize ratio is preserved
			ysize - the height of the new image, if only ysize included, ysize/xsize ratio is preserved
			algo - algorithm to use for resizing
		"""
		def __init__(self,xsize=None,ysize=None,algo=None):
			"""
			initializing params
			"""
			self.xsize=xsize
			self.ysize=ysize
			self.algo=algo
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.xsize!=None:m['xsize']=self.xsize
			if self.ysize!=None:m['ysize']=self.ysize
			if self.algo!=None:m['algo']=self.algo
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize resize operation and define inputs, parameters, and outputs"""
		self.operation="resize"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class img2tensor(operation):
	"""
	converts an image type to an array of arrays
	"""
	class inputs:
		"""
		inputs's possible keys:
			img - the image to be converted, jpg,png, or gif
		"""
		def __init__(self,img=None):
			"""
			initializing inputs
			"""
			self.img=img
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			m['img']=self.img
			return m
	class params:
		"""
		params's possible keys:
			removeAlpha - Most images have 4 values per pixel r,b,g,alpha, where alpha is something like transparency - alpha is not used in most ML cases.  True means remove alpha while converting.
			includeBatch - Often ML requires a dimension for batch (multiple images), if true dimensions = 4 with first dimension the batch, otherwise this produces a 3-D tensor (width, height, color).
		"""
		def __init__(self,removeAlpha=None,includeBatch=None):
			"""
			initializing params
			"""
			self.removeAlpha=removeAlpha
			self.includeBatch=includeBatch
		def make_map(self):
			"""
			method to convert data into a map for later printing
			"""
			m={}
			if self.removeAlpha!=None:m['removeAlpha']=self.removeAlpha
			if self.includeBatch!=None:m['includeBatch']=self.includeBatch
			return m
	def __init__(self,inputs=None,params=None,output=None):
		""" Initialize img2tensor operation and define inputs, parameters, and outputs"""
		self.operation="img2tensor"
		operation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)


class ops:
	class restructuring:
		"""
		Operations that restructure data (pivot, join, etc.)
		"""
		class map2table(map2table):
			def __init__(self,inputs=None,params=None,output=None):
				map2table.__init__(self,inputs=inputs,params=params,output=output)
		class groupBy(groupBy):
			def __init__(self,inputs=None,params=None,output=None):
				groupBy.__init__(self,inputs=inputs,params=params,output=output)
		class reshape(reshape):
			def __init__(self,inputs=None,params=None,output=None):
				reshape.__init__(self,inputs=inputs,params=params,output=output)
		class transpose(transpose):
			def __init__(self,inputs=None,params=None,output=None):
				transpose.__init__(self,inputs=inputs,params=params,output=output)
		class dropCol(dropCol):
			def __init__(self,inputs=None,params=None,output=None):
				dropCol.__init__(self,inputs=inputs,params=params,output=output)
		class cast(cast):
			def __init__(self,inputs=None,params=None,output=None):
				cast.__init__(self,inputs=inputs,params=params,output=output)
		class pivot(pivot):
			def __init__(self,inputs=None,params=None,output=None):
				pivot.__init__(self,inputs=inputs,params=params,output=output)
		class addCol2Table(addCol2Table):
			def __init__(self,inputs=None,params=None,output=None):
				addCol2Table.__init__(self,inputs=inputs,params=params,output=output)
		class flatten(flatten):
			def __init__(self,inputs=None,params=None,output=None):
				flatten.__init__(self,inputs=inputs,params=params,output=output)
		class table2map(table2map):
			def __init__(self,inputs=None,params=None,output=None):
				table2map.__init__(self,inputs=inputs,params=params,output=output)
		class join(join):
			def __init__(self,inputs=None,params=None,output=None):
				join.__init__(self,inputs=inputs,params=params,output=output)
	class math:
		"""
		Math based operations
		"""
		class scale(scale):
			def __init__(self,inputs=None,params=None,output=None):
				scale.__init__(self,inputs=inputs,params=params,output=output)
		class normalize(normalize):
			def __init__(self,inputs=None,params=None,output=None):
				normalize.__init__(self,inputs=inputs,params=params,output=output)
		class multPairWise(multPairWise):
			def __init__(self,inputs=None,params=None,output=None):
				multPairWise.__init__(self,inputs=inputs,params=params,output=output)
		class norm(norm):
			def __init__(self,inputs=None,params=None,output=None):
				norm.__init__(self,inputs=inputs,params=params,output=output)
		class mean(mean):
			def __init__(self,inputs=None,params=None,output=None):
				mean.__init__(self,inputs=inputs,params=params,output=output)
	class string_processing:
		"""
		Operations that act on strings
		"""
		class concat(concat):
			def __init__(self,inputs=None,params=None,output=None):
				concat.__init__(self,inputs=inputs,params=params,output=output)
		class levenshteinSimilarity(levenshteinSimilarity):
			def __init__(self,inputs=None,params=None,output=None):
				levenshteinSimilarity.__init__(self,inputs=inputs,params=params,output=output)
		class lastindex(lastindex):
			def __init__(self,inputs=None,params=None,output=None):
				lastindex.__init__(self,inputs=inputs,params=params,output=output)
		class tolower(tolower):
			def __init__(self,inputs=None,params=None,output=None):
				tolower.__init__(self,inputs=inputs,params=params,output=output)
		class matchregex(matchregex):
			def __init__(self,inputs=None,params=None,output=None):
				matchregex.__init__(self,inputs=inputs,params=params,output=output)
		class count(count):
			def __init__(self,inputs=None,params=None,output=None):
				count.__init__(self,inputs=inputs,params=params,output=output)
		class replace(replace):
			def __init__(self,inputs=None,params=None,output=None):
				replace.__init__(self,inputs=inputs,params=params,output=output)
		class repeat(repeat):
			def __init__(self,inputs=None,params=None,output=None):
				repeat.__init__(self,inputs=inputs,params=params,output=output)
		class uuid(uuid):
			def __init__(self,inputs=None,params=None,output=None):
				uuid.__init__(self,inputs=inputs,params=params,output=output)
		class split(split):
			def __init__(self,inputs=None,params=None,output=None):
				split.__init__(self,inputs=inputs,params=params,output=output)
		class index(index):
			def __init__(self,inputs=None,params=None,output=None):
				index.__init__(self,inputs=inputs,params=params,output=output)
		class toupper(toupper):
			def __init__(self,inputs=None,params=None,output=None):
				toupper.__init__(self,inputs=inputs,params=params,output=output)
		class levenshteinDistance(levenshteinDistance):
			def __init__(self,inputs=None,params=None,output=None):
				levenshteinDistance.__init__(self,inputs=inputs,params=params,output=output)
		class contains(contains):
			def __init__(self,inputs=None,params=None,output=None):
				contains.__init__(self,inputs=inputs,params=params,output=output)
	class nlp:
		"""
		Natural Language Processing(NLP) related operations
		"""
		class getStopWords(getStopWords):
			def __init__(self,inputs=None,params=None,output=None):
				getStopWords.__init__(self,inputs=inputs,params=params,output=output)
		class removeStop(removeStop):
			def __init__(self,inputs=None,params=None,output=None):
				removeStop.__init__(self,inputs=inputs,params=params,output=output)
		class tokenize(tokenize):
			def __init__(self,inputs=None,params=None,output=None):
				tokenize.__init__(self,inputs=inputs,params=params,output=output)
		class stem(stem):
			def __init__(self,inputs=None,params=None,output=None):
				stem.__init__(self,inputs=inputs,params=params,output=output)
		class segment(segment):
			def __init__(self,inputs=None,params=None,output=None):
				segment.__init__(self,inputs=inputs,params=params,output=output)
		class posTag(posTag):
			def __init__(self,inputs=None,params=None,output=None):
				posTag.__init__(self,inputs=inputs,params=params,output=output)
	class cleaning:
		"""
		Operations that fall best under data cleaning
		"""
		class set(set):
			def __init__(self,inputs=None,params=None,output=None):
				set.__init__(self,inputs=inputs,params=params,output=output)
		class ifnotin(ifnotin):
			def __init__(self,inputs=None,params=None,output=None):
				ifnotin.__init__(self,inputs=inputs,params=params,output=output)
		class ifin(ifin):
			def __init__(self,inputs=None,params=None,output=None):
				ifin.__init__(self,inputs=inputs,params=params,output=output)
		class concatMap(concatMap):
			def __init__(self,inputs=None,params=None,output=None):
				concatMap.__init__(self,inputs=inputs,params=params,output=output)
		class replaceValue(replaceValue):
			def __init__(self,inputs=None,params=None,output=None):
				replaceValue.__init__(self,inputs=inputs,params=params,output=output)
		class apply(apply):
			def __init__(self,inputs=None,params=None,output=None):
				apply.__init__(self,inputs=inputs,params=params,output=output)
		class oneHotEncoding(oneHotEncoding):
			def __init__(self,inputs=None,params=None,output=None):
				oneHotEncoding.__init__(self,inputs=inputs,params=params,output=output)
	class image_processing:
		"""
		Image processing related operations
		"""
		class grayscale(grayscale):
			def __init__(self,inputs=None,params=None,output=None):
				grayscale.__init__(self,inputs=inputs,params=params,output=output)
		class subSectionToImage(subSectionToImage):
			def __init__(self,inputs=None,params=None,output=None):
				subSectionToImage.__init__(self,inputs=inputs,params=params,output=output)
		class resize(resize):
			def __init__(self,inputs=None,params=None,output=None):
				resize.__init__(self,inputs=inputs,params=params,output=output)
		class img2tensor(img2tensor):
			def __init__(self,inputs=None,params=None,output=None):
				img2tensor.__init__(self,inputs=inputs,params=params,output=output)
