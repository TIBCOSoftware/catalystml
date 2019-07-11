# Feature Preperation Specification

## Introduction

The purpose of this specification is to facilitate the easy transformation of data from an input source such that it is ready for input into an ML model.  A related secondary purpose is to transform data from an ML model into a final presentable format.  This specification will be defined in a JSON format so that it is language agnostic with the expectation that language specific implementations can interpret the specification and process incoming data.  This document seeks to lay out the expected structure and behavior of such interpreters.  A single JSON document is intended to represent a single Preparation structure.

## General Structure

The specification will be represented within a JSON format.  The first level of the JSON format will contain:
1. __General information of the specification__ - i.e. name for the feature processing structure, version, target model metadata, ...
 
2. __Inputs__ - a list describing the data to be processed types, labels, etc.
3. __Structure__ - a list of the functions to operate on the data
4. __Outputs__ - describing how the processed data is to be output

## Types and Structures

Throughout the specification (especially in Inputs and Outputs) data types and structures are used to represent data.  Here we define and discuss the supported data types.  The types fall into two categories structures and types.  Structures are object types (lists, maps, data frames) that can be constructed with values that are either data types or other data structures.

* data structures:
    * "list" - is an array of objects
    * "map" - a hash table of key value pairs - values are data types or lists
    * "image" - a type that holds all image data, should support at least png,gif,jpeg types
* data types:
    * "string"
    * "int32"
    * "int64"
    * "float32"
    * "float64"
    * "boolean"

Since strings and data references are both surrounded by quotes to distinguish between them data references have a “$” at the beginning of the label.

## Object Names:

When an object is defined either within input or as the output of an operation the object is given the name corresponding to the value associated with the “label” key.  This name can then be used to refer to this object in either another operation’s input or as a component of the structure output.  Collisions of labels should raise a warning during structure build time, but still allow for data overwrite. For maps and lists the columns/keys can be reference by appending the column/key (in single quotes for maps) to the end of the object name surrounded by square brackets.  For example a map object named df with columns/keys “col0”, “col1”, etc could have its first column called with “df['col0']”.  Similarly, list objects can have their components referred by their index number by appending the index to the end of the object name surrounded by square brackets.  For multi-dimensional list each index would be within their own brackets.  For example a list of lists (2D) named “matrix” could refer to a component as “matrix[0][3]” .  Indexes for lists begin at 0.

## Comments

JSON formats do not allow comments, i.e. all inclusions must be data.  However, for this specification comments can effectively be included as a key/value pair in any map level by using a key of "//comment".  With such a key the value would be ignored by the parser, which effectively creates an avenue for a comment.  

## Structure Specification:

### General Information:

General information describes several key:value pairs within the first level of the preparation structure JSON that contains information and metadata for the structure.  These values are optional.


* _Name_ - [string] - General name for the structure i.e. AccelerometerProcessing
* _Description_ -  [string] - A note that describes the purpose/use case of the structure
* _Version_- [string] - Version of structure i.e. 0.8.3
* _CMLVersion_ - [string] - Version of CatalystML spec structure is written for
* _createdDate_: [string] - the date the structure was created
* _Model_- [json object] The metadata for a model (tag/etc.) containing the following parameters
	* _Framework_ - [string] - target model framework (Tensorflow, PyTorch, etc.)
	* _inputTensorName_ - [string] - the names of the input tensors
    * _Tags_ - [string] - TF model descriptor
    * _SignatureDef_ - [string] - TF model descriptor

### Inputs:
* __Input__: [array of objects] defines a list containing all inputs 

The root level key value “input” is used to define the data that is passed into the specification.  Since multiple data objects can be passed to the specification “input” is a JSON list of objects containing the following key words:
* type
* dimensions - if relevant
* shape - if relevant
* label

### Structure of Operations:
The structure key in the JSON specification defines the interactions and order of execution between operations and includes the list of operations used.  The order in which operations are executed is specified to be in the order in which the operations are  listed.  However, optimization can be left to the implementation.  For example, any operations that may not have dependencies on prior operation output that have not been run can be run in parallel, etc.  The structure (and the basic structure for operations) is defined as:

structure: [array of objects] defines a list containing all operations - the operations objects are of the form:
* Operation- [string] name of operation (i.e. norm, scale, etc.)
    * Id - label for this instance of the operation by the user (will be used to refer to operatin instance output)
    * Input -  [map object] describes the inputs:
        * Data: value of a labeled variable or a list of values
        * Other keys specific to operation possible
    * Params - object containing operation specific parameters (optional)
    * Output: - name of the output of the operation
        * If map give keys of map

Below are a list of operations supported by this specification by category with their expected results and their operation specific keywords.


#### Supported Operations:
_Math_:
* __norm__: determine the geometric length of a vector - output is a float.  If matrix determines magnitude of vectors based upon axis selected - output array of floats.
    * Input
        * Data - [array or array of arrays]
            * Optional=False
    * Params
        * Axis - [int]
            * Optional=True
            * Default=0
    * Output - [array of floats] (array of length 1 if needed)
* __normalize__: divide all values of array by value
    * Input
        * Data - [array or array of arrays]
            * Optional=False
        * value - [int, float] 
    * Output - [array of floats]
* __scale__: multiply every value of a matrix by a scalar
    *Input
        * Data - < array of arrays> 
            * Optional=False
        * scaler - [float]
            * Optional=False
    * Params
        * None
    * Output - [array of arrays] (same size as input)
* __mean__: average of an array - axis of matrix can be selected
    * Input
        * Data - [array or array of arrays]
            * Optional=False
    * Params
        * Axis - [int] 
            * Optional=True
            * Default=0
    * Output - [array of floats]
* __multPairWise__:for matrices of the same shape multiply corresponding values
   * Input
        * matrix0 - [array of arrays]
            *Optional=False
        * matrix1 - [array of arrays]
            * Optional=False
    * Params
        * None
    * Output - [array of arrays] (same size as inputs)
* __addPairWise__:for matrices of the same shape add corresponding values
    * Input
        * matrix0 - [array of arrays]
            *Optional=False
        * matrix1 - [array of arrays]
            * Optional=False
    * Params
        * None
    * Output - [array of arrays] (same size as inputs)
* __divPairWise__: for matrices of the same shape divide corresponding values
    * Input
        * matrix0 - [array of arrays] 
            * Optional=False
        * matrix1 - [array of arrays]
            * Optional=False
    * Params
        * None
    * Output - [array of arrays] (same size as inputs)
* __castToArray__: casts single value to array or array of arrays of given shape
    * Input
        * value - [int,string,float,etc] 
            * Optional=False
        * shape - [array of ints] - array determines shape of output ([2,3] means a 2x3 matrix)
            * Optional=False
    * Params
        * None
    * Output - [array of arrays] (same size as inputs)
* __add__: add two numbers
    * Input
        * a0 - [int,string,float,etc] 
            * Optional=False
        * a1 - [int,float] 
            * Optional=False
    * Output - [int,float]
* __multi__: multiply two numbers
    * Input
        * a0 - [int,string,float,etc] 
            * Optional=False
        * a1 - [int,float] 
            * Optional=False
    * Output - [int,float]
* __divide__: divide two numbers
    * Input
        * num - [int,string,float,etc] 
            * Optional=False
        * denom - [int,float] 
            * Optional=False
    * Output - [int,float]

_Cleaning_:
* __replaceValue__: Given a map replaces data (key) with map value 
    * Input
        * Data - [array or map]
            * Optional=False
        * replaceMap - [map] - map gives key to replace with value
	        * Optional=True
        * replaceKey - [NaN,int,string,float,etc] - what is to be replaced
	        * Optional=True
	        * Default=NaN (if neither replaceMap or replaceKey given)
        * replaceValue - [NaN,int,string,float,etc] - what is to be replaced with 
	        * Optional=True
	        * Default=NaN (if neither replaceMap or replaceKey given)
    * Params
        * Axis - [int] 
            * Optional=True
            * Default=0
        * Col - [string] 
            * Optional=True
            * Default=’index’
    * Output - [array or map] (same type as inputs)
* __removeOutliers__: negatives or values vastly outside range of data
    * Input
        * Data - [array of arrays or map]
			* Optional=False
        * Col - map key or column number
    * Params
        * outlierType [string]
			* Optional=True
			* Default = “Negatives”
			* Accepted Values - “Negatives”,
    * Output - [array or map] (same type as inputs)
* __arrange/sort__:  sort a matrix/map based on given columns
    * Input
        * Data - [array of arrays or map]
			* Optional=False
        * Col - map key or column number
    * Params
        * Ascending - [boolean]
        * KeepRow - [boolean] (keeps row/column)
        * Axis - [int]
* __filter__:  keep/remove rows with certain values
    * Input
        * Data - [array or map]
            * Optional=False
        * Value - [int, float, string, NaN]
	        * Optional=True
	        * Default=NaN
        * filterType - [string]
	        * Optional=True
	        * Default=Remove
	        * Acceptable values = “Remove”,”Keep”
    * Params
        * Axis - [int]
            * Optional=True
            * Default=0
        * Col - [string]
            * Optional=True
            * Default=’index’
    * Output - [array or map] (same type as inputs)
* __groupBy__:  group by a given column in an axis and aggregate the value of another column (like SQL)
    * Input
        * Data - [array or map] data to group
            * Optional=False
        * groupKeys [array] - Column by which to group
    * Params
        * asIndex - [boolean]
        * axis - [int]
* __pivot__:  reshape a matrix or map by re-indexing like the pivot function in pandas
* __transpose__:  transpose a matrix
* __join__:  join two data objects like the Left Join command in SQL
    * Input
        * Data0 - [array of data variables]  contains matrices or data frames of inputs
            * Optional=False
        * Data1 - [array of data variables]  contains matrices or data frames of inputs
            *Optional=False
    * Params
        * on - [array of strings]  - either index or the col name/number
            * Optional=True???
            * Default= array of “index”
        * how - [string]
            * Options: left, right, inner, outer
            * Optional=False
    * Output - [matrix or map]
* __apply__: apply a function to every value in a vector
* __flatten__: reduce multidimensional lists to single dimension
* __reShape__: change the dimensionality of a matrix without changing the underlying data

_Retyping_:
* __map2Table__: convert a map to a matrix
    * Input
        * map - [map]  contains map to be converted to table
            * Optional=False
        * colOrder - [array of strings] list of the columns to be merged into table (ORDER MATTERS)
            * Optional=False
    * Params
        * axis - the orientation of the table
            * default=0
    * Output - [array of arrays]
* __table2Map__: convert a matrix to a map by adding a name to each column
    * Input
        * table - [array or arrays] 2D table to be converted to map
        * colKeys - [array of strings] list of keys for map that correspond to 0 to n columns in table
    * Params
        * axis - the orientation of the table
            * default=0
    * Output - [map]
* __cast__: convert from one base type to another

_Categorical_:
* __binning__: take a numerical list and convert it into bins
* __oneHotEncoding__: convert categorical vector into a set of vectors for each category with a 0/1
* __targetEncoding__: replace categorical value with its average of another numerical column
* __lag__: create new vector shifted down by lagnum with NaN filling missing locations added to table/map
    * Input
        * table - [map or array of array]  data
        * lagnum - int of number of places to lag data
    * Params
        * axis - the orientation of the table
            * default=0
    * Output - [map]

_String Processing_:
* __date__: (year,month,day, etc.) extract date information from string
    * Input
        * data - [string]
            * Optional=False
    * Params
        * format - [string]
            * Optional=True
            * Default=””  We will get the proper format
    * Output - [datetime object]  (datatime object includes properties, month etc.)
* __phoneNumber__: Extract phone number from string
* __geoEncoding__:Convert string to Geo coords 
* __address__: (number, street,city, state, etc.) extract data information from string
* __concat__: join strings together
    * Input
        * s0 [string] - first string
        * s1 [string] - second string
    * Output - [string]
* __contains__:  whether substring exists in string
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * Output - [boolean]
* __count__:returns the number of non-overlapping instances of substring in string
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * Output - [int]
* __decodestring__: returns a string from a base64 encoded input string 
    * Input
        * s [string] - string
    * Output - [string]
* __encodestring__: returns a base64 encoded string from an input string 
    * Input
        * s [string] - string
    * Output - [string]
* __index__: Index returns the index of the first instance of substr in s, or -1 if substr is not present in s
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * Output - [int]
* __indexany__: IndexAny returns the index of the first instance of any Unicode code point from chars in s, or -1 if no Unicode code point from chars is present in s
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * Output - [int]
* __lastindex__: LastIndex returns the index of the last instance of substr in s, or -1 if substr is not present in s
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * Output - [int]
* __matchregex__: Match input against regular expression
    * Input
        * s0 [string] - regex
        * s1 [string] - string
    * Output - [boolean]
* __repeat__: Repeat returns a new string consisting of count copies of the string s
    * Input
        * s [string] - string
        * i [integer] - the number of repeats
    * Output - [string]
* __replace__: Replace returns a copy of the string s with the first n non-overlapping instances of old replaced by new. If n < 0, there is no limit on the number of replacements
    * Input
        * s0 [string] - string
        * s1 [string] - string to be replaced
        * s2 [string] - string to replace with
        * i [integer] - number of possible replacements
    * Output - [string]
* __replaceall__: ReplaceAll returns a copy of the string s with all non-overlapping instances of old replaced by new.
* __replaceregex__: Replace data in a string based on a regular expression match	
* __split__: Split slices s into all substrings separated by sep and returns a slice of the substrings between those separators
* __tolower__: ToLower returns a copy of the string s with all Unicode letters mapped to their lower case
* __toupper__: ToUpper returns a copy of the string s with all Unicode letters mapped to their upper case
* __trim__: Trim returns a slice of the string s with all leading and trailing Unicode code points contained in cutset removed
* __trimleft__:TrimLeft returns a slice of the string s with all leading Unicode code points contained in cutset removed
* __trimright__: TrimRight returns a slice of the string s with all trailing Unicode code points contained in cutset removed
* __trimprefix__: TrimPrefix returns s without the provided leading prefix string. If s doesn't start with prefix, s is returned unchanged
* __trimsuffix__: TrimSuffix returns s without the provided trailing suffix string. If s doesn't end with suffix, s is returned unchanged
* __uuid__: UUID generates a random UUID according to RFC 4122
    * Output - [string]

_NLP_:
* __Tokenization__: separate text into tokens / words / punctuation
* __Word2embedding__: convert words from list to array of wordlist x numerical embedding
* __Embedding2word__: convert list of embedding to closest words
* __removeStop__: given text and list of (stop) words - removes those words from text.
* __stem__: produces the stem of a word (i.e. running -> run)

_Image Processing_:
* __resize__: change dimensions of image
* __removeAlpha__:  Most images have 4 values per pixel r,b,g,alpha, where alpha is something like transparency - alpha is not used in most ML cases
* __Grayscale__: Convert color image to grayscale
* __subSectionToImage__: takes a portion of an image and makes it an independent image (i.e. for selecting out a face)
* __addBoxLabel__: Add box and Label to an image given location (FOR POST PROCESSING)
* __img2tensor__: Converts an image type to a mathematical tensor (i.e. an array of any number of dimentions)
    * Input
        * image - [image]
    * Output - [array of array or arrays (3D matrix)]


_Custom Operations_:
* Language specific method for defining a custom operation (i.e. in go using go get)

### Outputs:


The structure of the “output” object of a feature preparation specification structure is intended to allow for the construction of complicated output object ranging from a string to a full JSON type mix of maps and lists.  The “output” object should allow for values to include both objects defined in “operations”, “inputs”, hand values, AND further “output” objects (i.e. output objects can be nested/recursive).  The “output” object has two fields “type”, and “data” where the type defined in “type” determines how “data” is constructed.  If a hash table object (map or data frame) is used for type then data is built as a JSON object. If type is a list object ”data” is built as an array of data values.  If "type" does not match "data" and error should be raised.

* __output__: [map object] a JSON object defining the output
    * "Type": [string]
    * "Data": data of defined type constructed from inputs and operation ids.

Constructed as an object from hand defined keys and data references. 
