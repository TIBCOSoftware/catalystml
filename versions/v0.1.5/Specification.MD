# Feature Preperation Specification

## Introduction

The purpose of this specification is to facilitate the easy transformation of data from an input source such that it is ready for input into an ML model.  A related secondary purpose is to transform data from an ML model into a final presentable format.  This specification will be defined in a JSON format so that it is language agnostic with the expectation that language specific implementations can interpret the specification and process incoming data.  This document seeks to lay out the expected structure and behavior of such interpreters.  A single JSON document is intended to represent a single Preparation structure.

## General Structure

The specification will be represented within a JSON format.  The first level of the JSON format will contain:
1. __General information of the specification__ - i.e. name for the feature processing structure, version, target model metadata, ...
 
2. __Inputs__ - a list describing the data to be processed types, labels, etc.
3. __Structure__ - a list of the functions to operate on the data
4. __Outputs__ - describing how the processed data is to be output

## Types and Data Structures

Throughout the specification (especially in Inputs and Outputs) data types and structures are used to represent data.  Here we define and discuss the supported data types.  The types fall into two categories structures and types.  Structures are object types (lists, maps, data frames) that can be constructed with values that are either data types or other data structures.  "Any" is added for ease in constructing output data.

* data structures:
    * "list" - is an array of objects (we also use matrix and array of array interchangably below)
    * "map" - a hash table of key value pairs - values are data types or structures
    * "image" - a type that holds all image data, should support at least png, gif, jpeg types
    * "datetime" - structure to contain date and time
    * "any" - any of the other types or structure 
* data types:
    * "string"
    * "int32"
    * "int64"
    * "float32"
    * "float64"
    * "boolean"

Since strings and data references are both surrounded by quotes to distinguish between them data references have a “$” at the beginning of the label.  Likewise, to reserve keywords to be referenced within a specific operation (i.e. item in Apply) use "&" in front of the keyword (.i.e. "&item").  If a "$" or "&" should be included in a string the escape character "\\" should preceed the "$" or "&".

Dataframes are a common data structure when dealing with data processing.  While dataframes are not addressed outside this section, the idea of dataframes is incorporated in how to manipulate data.  In this context a datframe is considered to be a map with values that correspond to arrays.

## Object Names:

When an object is defined either within input or as the output of an operation the object is given the name corresponding to the value associated with the “label” key.  This name can then be used to refer to this object in either another operation’s input or as a component of the structure output.  Collisions of labels should raise a warning during structure build time, but still allow for data overwrite.  Indeed, an operation output can be labeled with a pre-existing object component (map or array compnent as described next) to overwrite that compnent. For maps and lists the columns/keys can be reference by appending the column/key (in single quotes for maps) to the end of the object name surrounded by square brackets.  For example a map object named df with columns/keys “col0”, “col1”, etc could have its first column called with “df['col0']”.  Similarly, list objects can have their components referred by their index number by appending the index to the end of the object name surrounded by square brackets.  For multi-dimensional list each index would be within their own brackets.  For example a list of lists (2D) named “matrix” could refer to a component as “matrix[0][3]” .  Indexes for lists begin at 0.

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
* _Model_- [json object] The metadata for a model (tag/etc.) containing the following parameters - NOT FULLY IMPLEMENTED - SUBJECT TO CHANGE
	* _Framework_ - [string] - target model framework (Tensorflow, PyTorch, etc.)
	* _inputTensorName_ - [string] - the names of the input tensors
    * _Tags_ - [string] - TF model descriptor
    * _SignatureDef_ - [string] - TF model descriptor

### Inputs:
* __Input__: [array of objects] defines a list containing all inputs 

The root level key value “input” is used to define the data that is passed into the specification.  Since multiple data objects can be passed to the specification “input” is a JSON list of objects containing the following key words:
* type - [string]
* dimensions - [array]- if relevant
* shape - [array]-  if relevant
* label - [string] if labeling full input, [array] if providing labels for each component using "_" to skip assigning labels if desired, [map] is providing labels for components of a map.  Errors are thrown if labels are given for non-existing data references (i.e. arr[9] if the array is only length 5, or if key1 in {"key1":"label3"} doesn't exist).


### Operations:

#### Structure of Operations
The structure key in the JSON specification defines the interactions and order of execution between operations and includes the list of operations used.  The order in which operations are executed is specified to be in the order in which the operations are  listed.  However, optimization can be left to the implementation.  For example, any operations that may not have dependencies on prior operation output that have not been run can be run in parallel, etc.  The structure (and the basic structure for operations) is defined as:

structure: [array of objects] defines a list containing all operations - the operations objects are of the form:
* Operation- [string] name of operation (i.e. norm, scale, etc.)
    * Input -  [map object] describes the inputs:
        * Data: value of a labeled variable or a list of values
        * Other keys specific to operation possible
    * Params - object containing operation specific parameters (optional)
    * OutputType - type of output
    * Output - a label or list of labels,  the label or pre-existing label's component to reference the output value of the operation by the User (i.e. datatemp['age'], datatemp)

Below are a list of operations supported by this specification by category with their expected results and their operation specific keywords.

#### Tests of Operations
A directory exists within the github repository titled 'tests' that includes unit tests for various operations.  This directory is further subdivided by the same categories as the below operations. Then each operation will consist of its own directory (directory name sharing the name of the operation).  Each test in an operations directory will consist of three files: the operation inputs and parameters as they would be entered into a structure, an input file, and an output file where each operation can have multiple tests.  Each test will be numbered starting from 0.  The format of the names for the tests of operation _OperationName_, test number _X_, and with input as a _jpeg_ and output as a _csv_ is as follows:
*   _OperationNameX.json_ - for the operation structure ($input designates in the input variable)
*   _OperationNameX.in.jpeg_ - for the operation input
*   _OperationNameX.out.csv_ - for the operation output

#### Supported Operations:
_Math_:
* __norm__: determine the geometric length of a vector - output is a float.  If matrix determines magnitude of vectors based upon axis selected - output array of floats.
    * Input
        * Data - [array or array of arrays]
            * Optional=False
    * Params
        * Axis - [int] (0=vertical/column, 1=horizontal/row)
            * Optional=True
            * Default=0
    * OutputType - [array of floats] (array of length 1 if needed)
* __normalize__: divide all values of array by value (i.e. x/value), if minvalue is given applies (x-minval)/(value-minvalue) where x is the data 
    * Input
        * Data - [array or array of arrays]
            * Optional=False
        * value - [int, float] 
            * Optional=False
        * minvalue - [int,float]
            * Optional=True
    * OutputType - [array of floats]
* __scale__: multiply every value of a matrix by a scalar
    *Input
        * Data - < array of arrays> 
            * Optional=False
        * scaler - [float] value to scale by
            * Optional=False
    * Params
        * None
    * OutputType - [array of arrays] (same size as input)
* __mean__: average of an array - axis of matrix can be selected
    * Input
        * Data - [array or array of arrays]
            * Optional=False
    * Params
        * Axis - [int] (0=vertical/column, 1=horizontal/row)
            * Optional=True
            * Default=0
    * OutputType - [array of floats]
* __multPairWise__:for matrices of the same shape multiply corresponding values
   * Input
        * matrix0 - [array of arrays]
            *Optional=False
        * matrix1 - [array of arrays]
            * Optional=False
    * Params
        * None
    * OutputType - [array of arrays] (same size as inputs)
* __addPairWise__:for matrices of the same shape add corresponding values
    * Input
        * matrix0 - [array of arrays] first matrix 
            *Optional=False
        * matrix1 - [array of arrays] second matrix
            * Optional=False
    * Params
        * None
    * OutputType - [array of arrays] (same size as inputs)
* __divPairWise__: for matrices of the same shape divide corresponding values
    * Input
        * matrix0 - [array of arrays] first matrix (numerator)
            * Optional=False
        * matrix1 - [array of arrays] second matrix (denominator)
            * Optional=False
    * Params
        * None
    * OutputType - [array of arrays] (same size as inputs)
* __add__: add two numbers
    * Input
        * a0 - [int,string,float,etc] 
            * Optional=False
        * a1 - [int,float] 
            * Optional=False
    * OutputType - [int,float]
* __multi__: multiply two numbers
    * Input
        * a0 - [int,float] 
            * Optional=False
        * a1 - [int,float] 
            * Optional=False
    * OutputType - [int,float]
* __divide__: divide two numbers
    * Input
        * num - [int,float] 
            * Optional=False
        * denom - [int,float] 
            * Optional=False
    * OutputType - [int,float]

_Cleaning_:
* __replaceValue__: Given a map replaces data (key) with map value 
    * Input
        * data - [array or map]
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
        * Axis - [int] (0=vertical/column, 1=horizontal/row)
            * Optional=True
            * Default=0
        * Col - [string] 
            * Optional=True
            * Default=’index’
    * OutputType - [array or map] (same type as inputs)
* __removeOutliers__: negatives or values vastly outside range of data
    * Input
        * Data - [array of arrays or map]
			* Optional=False
        * Col - [string/int or array ]map key or column number
    * Params
        * outlierType [string]
			* Optional=True
			* Default = “Negatives”
			* Accepted Values - “Negatives”,
    * OutputType - [array or map] (same type as inputs)
* __sort__:  sort a matrix/map based on given columns
    * Input
        * Data - [array of arrays or map]
			* Optional=False
    * Params
        * Ascending - [boolean]
	        * Optional = TRUE
	        * Default = False
        * Axis - [int] 
            * Optional = TRUE
            * Default = 0,
            * Allowed = (0:vertical/column, 1:horizontal/row),
        * nilPosition - [string] 
            * Optional = False
            * Allowed = ["first", "last"],
        * by - [array] sort by elements
            * Optional = False
				* string array : sort by the conlumns (with configured column label), 
				* int array (0 means first column) : sort by the columns (whith configured column number)
    * OutputType - [array of arrays or map]
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
        * Axis - [int] (0=vertical/column, 1=horizontal/row)
            * Optional=True
            * Default=0
        * Col - [string]
            * Optional=True
            * Default=’index’
    * OutputType - [array or map] (same type as inputs)
* __binning__: take a numerical list and convert it into bins
* __oneHotEncoding__: convert categorical vector into a set of vectors for each category with a 0/1.  The rest of the data in the map/matrix is kept but column used is removed unless keepOrig is true. Collisions of column names are resolved, but append an intger after an "_" starting at 1 for the new column, for example "col_1", "col_2", "col_3", ...
    * Input
        * data - [array of arrays or map] 2D table to be converted to map
    * Params
        * inputColumns - [array of strings] the columns to which one Hot Encodding should be applied
            Optional = false
        * outputColumns - [array of strings] list of keys that should be turned into new columns
            * Optional = true
            * Default = those that exist in data
        * keepOrig - [bool] The rest of the data in the map/matrix is kept but column used is removed unless keepOrig is true.
            * Optional = true
            * default = false
    * OutputType - [map]
* __targetEncoding__: replace categorical value with its average of another numerical column
* __lag__: create new vector shifted down by lagnum with NaN filling missing locations added to table/map
    * Input
        * table - [map or array of array]  data
        * lagnum - int of number of places to lag data
    * Params
        * axis - the orientation of the table (0=vertical/column, 1=horizontal/row)
            * default=0
    * OutputType - [map]
* __set__: [array] takes an array and removes duplicates, result is unordered (SHOULD WE RENAME THIS TO removeDups INSTEAD?)
    * Input
        * array - [array]
    * OutputType - [array]
* __ifIn__: Given 2 arrays returns the new array with the elements of the first array only if they appear in the second array as well.
    * Input
        * arr0 - [array]  first array, the one to compare to the "in" list
            * Optional=False
        * arr1 - [array]  the array for the "in" of if in.
            * Optional=False
    * OutputType - [array]
* __ifNotIn__:Given 2 arrays returns the new array with the elements of the first array only if they DO NOT appear in the second array as well.
    * Input
        * arr0 - [array]  first array, the one to compare to the "not in" list
            * Optional=False
        * arr1 - [array of data variables]  the array for the "not in" of if not in.
            * Optional=False
    * OutputType - [array]
* __apply__: apply a function to every value in a vector or key in a map
    * Input
        * data - [map or array] data to be operated on
        * function - [json object] - the operator to be used as the function, "&item" to be used as the variable taken from the data variable when defining inputs and params (instance of the loop), output not included in this object since output is in the apply object
    * Params
        * mapOrArray - [string] determines whether the output is an array or a map (input value as key,  response as value)
            * Options: "map", "array"
            * Optional=true
            * default=array
    * OutputType - [array]


_Restructuring_:
* __valToArray__: casts single value to array or array of arrays of given shape
    * Input
        * value - [int,float,etc] 
            * Optional=False
        * shape - [array of ints] - array determines shape of output ([2,3] means a 2x3 matrix)
            * Optional=False
    * Params
        * None
    * OutputType - [array of arrays] (same size as inputs)
* __dropCol__:  remove cols from matrix or map
    * Input
        * data - [matrix or map] original data set
            * optional = False
        * cols - [strings, ints, array] indices or key for column in map or matrix to be removed
    * OutputType - [matrix or map]
* __groupBy__:  group by a given column in an axis and aggregate the value of another column (like SQL)
    * Input
        * Data - [array or map] data to group
            * Optional=False
        * groupKeys [array] - Column by which to group
    * Params
        * asIndex - [boolean]
        * axis - [int] (0=vertical/column, 1=horizontal/row)
            * optional = true
            * default = 0
    * OutputType - [array or map]
* __pivot__:  reshape a matrix or map by re-indexing like the pivot function in pandas
    * Input
        * data - [array or map] Column(s) to use for populating new frame’s values.
    * Params
        * index - [array of strings] Name of columns which value to be used to make new frame’s index.
            *optional= false
        * Columns - [array of strings] : Name of columns which value to be used to make new frame’s columns.
            *optional = false
        * Aggregate - [map[string]string] : Map key is groupKey, map value is aggregate function. Currently support Sum, Count, Mean, Min, Max
            * allowed= Sum, Count, Mean, Min, Max
            * optional= false
    * OutputType - [DataFrame]
* __transpose__:  transpose a matrix
    * Input
        * data [array,map]- Matrix to be transposed
            * Optional=False
* __join__:  join two data objects like the Left Join command in SQL
    * Input
        * Data0 - [array,map]  contains matrices or maps of inputs
            * Optional=False
        * Data1 - [array,map]  contains matrices or maps of inputs
            *Optional=False
    * Params
        * on - [array of strings]  - either index or the col name/number
            * Optional=True???
            * Default= array of “index”
        * how - [string]
            * Options: left, right, inner, outer
            * Optional=False
    * OutputType - [matrix or map]
* __flatten__: reduce multidimensional lists to single dimension
    * Input
        * matrix - [matrix] matrix to be flattened
    * OutputType - [array]
* __addCol2Table__: add a new column to a matrix from a given array (matrix is assumed to be 2-D list)
    * Input
        * matrix - [map or array] matrix to be expanded
        * col - [array]  col to be added of same length as matrix's second dimention
    * OutputType - [matrix]
* __reShape__: change the dimensionality of a matrix without changing the underlying data
   * Input
        * data - [array] data to be reshaped
        * shape - [array]  array of integers where: 1) length of array  number of  output dimensions and 2) each integer specifies the number of values for a given dimension.  If the integer is -1 that dimension is sized to fit the data. i.e. [-1,2,3] for a 24 value array means a 4x2x3 matrix
    * OutputType - [matrix]
* __map2Table__: convert a map to a matrix
    * Input
        * map - [map]  contains map to be converted to table
            * Optional=False
        * colOrder - [array of strings] list of the columns to be merged into table (ORDER MATTERS)
            * Optional=False
    * Params
        * axis - [int] the orientation of the table, (0=vertical/column, 1=horizontal/row)
            * default=0
    * OutputType - [array of arrays]
* __table2Map__: convert a matrix to a map by adding a name to each column
    * Input
        * table - [array of arrays] 2D table to be converted to map
        * colKeys - [array of strings] list of keys for map that correspond to 0 to n columns in table
    * Params
        * axis - the orientation of the table (0=vertical/column, 1=horizontal/row)
            * default=0
    * OutputType - [map]
* __cast__: convert the base datatype of a data structure or datatype from one base type to another (i.e. [int32,int32] to [flat64,float64]), it is useful to note that maps of arrays are allowed and handle by the specification.
    * Input
        * data - [any datatype or data structure] input data to be cast.
        * toType - [string] string depicting which datatype to cast to.  Allowed: int64,float64,string,int32,float32,boolean.
    * OutputType - [any]
* __concatMap__: takes an array of maps and combines them into one.
    * Input
        * data - [array] array of maps to be combines into one
    * OutputType - [map]

_String Processing_:
* __date__: (year,month,day, etc.) extract date information from string
    * Input
        * data - [string]
            * Optional=False
    * Params
        * format - [string]
            * Optional=True
            * Default=””  We will get the proper format
    * OutputType - [datetime object]  (datatime object includes properties, month etc.)
* __phoneNumber__: Extract phone number from string
* __geoEncoding__:Convert string to Geo coords 
* __address__: (number, street,city, state, etc.) extract data information from string
* __concat__: join two strings together or a list of strings.  It is possible to concat s0, s1, and slist together.
    * Input
        * s0 [string] - first string
        * s1 [string] - second string
        * slist [array of strings] - list of strings
    * OutputType - [string]
* __contains__:  whether substring exists in string
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * OutputType - [boolean]
* __count__:returns the number of non-overlapping instances of substring in string
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * OutputType - [int]
* __decodestring__: returns a string from a base64 encoded input string 
    * Input
        * s [string] - string
    * OutputType - [string]
* __encodestring__: returns a base64 encoded string from an input string 
    * Input
        * s [string] - string
    * OutputType - [string]
* __index__: Index returns the index of the first instance of substr in s, or -1 if substr is not present in s
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * OutputType - [int]
* __indexany__: IndexAny returns the index of the first instance of any Unicode code point from chars in s, or -1 if no Unicode code point from chars is present in s
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * OutputType - [int]
* __lastindex__: LastIndex returns the index of the last instance of substr in s, or -1 if substr is not present in s
    * Input
        * s0 [string] - string
        * s1 [string] - substring
    * OutputType - [int]
* __matchregex__: Match input against regular expression
    * Input
        * s0 [string] - regex
        * s1 [string] - string
    * OutputType - [boolean]
* __repeat__: Repeat returns a new string consisting of count copies of the string s
    * Input
        * s [string] - string
        * i [integer] - the number of repeats
    * OutputType - [string]
* __replace__: Replace returns a copy of the string s with the first n non-overlapping instances of old replaced by new. If n < 0, there is no limit on the number of replacements.
    * Input
        * s0 [string] - string
        * s1 [string] - string to be replaced
        * s2 [string] - string to replace with
        * i [integer] - number of possible replacements, default all
    * OutputType - [string]
* __replaceall__: ReplaceAll returns a copy of the string s with all non-overlapping instances of old replaced by new.
* __replaceregex__: Replace data in a string based on a regular expression match	
* __split__: Split slices s into all substrings separated by sep and returns a slice of the substrings between those separators
    * Input:
        * str - [string] string to be seperated
        * sep - [string] strings to be seperated at .i.e. "," , "\t", etc.
    * OutputType: [array of strings]
* __tolower__: ToLower returns a copy of the string s with all Unicode letters mapped to their lower case
    * Input:
        * str- [string] string to be made all lower case
* __toupper__: ToUpper returns a copy of the string s with all Unicode letters mapped to their upper case
    * Input:
        * str- [string] string to be made all upper case
* __trim__: Trim returns a slice of the string s with all leading and trailing Unicode code points contained in cutset removed
* __trimleft__:TrimLeft returns a slice of the string s with all leading Unicode code points contained in cutset removed
* __trimright__: TrimRight returns a slice of the string s with all trailing Unicode code points contained in cutset removed
* __trimprefix__: TrimPrefix returns s without the provided leading prefix string. If s doesn't start with prefix, s is returned unchanged
* __trimsuffix__: TrimSuffix returns s without the provided trailing suffix string. If s doesn't end with suffix, s is returned unchanged
* __uuid__: UUID generates a random UUID according to RFC 4122
    * OutputType - [string]
* __levenshteinDistance__: Calculates the Levenshtein Distance between two strings (number of changes needed to conver one string to the other)
    * Inputs:
        * s0 [string] - first string for comparison
        * s1 [string] - second string for comparison
    * OutputType: [int]
* __levenshteinSimilarity__: Calculates the Levenshtein Similarity (the normalized Distance) between two strings (number of changes needed to conver one string to the other)
    * Inputs:
        * s0 [string] - first string for comparison
        * s1 [string] - second string for comparison
    * OutputType: [float32]

_NLP_:
* __tokenize__: separate text into tokens / words / punctuation
    * Input:
        * str - [string] string to tokenize
    * OutputType: [array of strings]
* __word2embedding__: convert words from list to array of wordlist x numerical embedding
* __embedding2word__: convert list of embedding to closest words
* __getStopWords__: gets array of ([stop words](https://en.wikipedia.org/wiki/Stop_words)), by either using a default, or reading from a file.
    * Params:
        * lib - [string] - which library stopword list to load
            * Optional = True
            * allowed: ["nltk","none"]
            * default = "nltk"
        * lang - [string] The language to be used, based on [ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). For example: English='en'.
            * Optional = True
            * default = "en"
        * fileLoc - [string]- path to file that contains list of stop words (1 word per line)
            * Optional = True
        * merge -  [bool] Whether to merge list from file with file from library
            * Optional = True
            * default = False
    * OutputType - [array]
* __stem__: produces the stem of a word (i.e. running -> run)
    * Input:
        * str - [string] word to have endings removed
    * Params:
        * algo - [string]
            * Optional = True
            * default = "Porter"
            * allowed: ["Snowball","Porter"]
    * OutputType - [string or array]
* __segment__: Seperates a paragraph into sentences
    * Input:
        * str - [string]
    * OutputType: [array of strings]
* __posTag__: Part of speach tagger
    * Input:
        * str - [string]
    * OutputType: [array of arrays of strings]

_Image Processing_:
* __resize__: change dimensions of image
    * Input:
        * img - [image]
    * Params: at least oneof xsize/ysize must be included
        * xsize - [int] if only xsize included, xsize/ysize ratio is preserved
            * Optional - True
        * ysize - [int] if only ysize included, xsize/ysize ratio is preserved
            * Optional - True
        * algo - [string]
            * Optional - true
            * default - "Lanczos"
            * allowed: ["Lanczos","NearestNeighbor","Linear", "CatmullRom"]
    * OutputType - [image]
* __grayscale__: Convert color image to grayscale
    * Input:
        * img - [image]
    * OutputType - [image]
* __subSectionToImage__: takes a portion of an image and makes it an independent image (i.e. for selecting out a face).  If size from corner is larger than the image the subsection is returned up to the image edge.
    * Input
        * img - [image] image to be have subsection removed from
    * Params
        * size - [array of ints] the size of the subsection
        * lowerLeftCorner - [array of ints] the x,y coordinates (the corner with the lowest x,y vaules)
* __addBoxLabel__: Add box and Label to an image given location (FOR POST PROCESSING)
* __img2tensor__: Converts an image type to a mathematical tensor (i.e. an array of any number of dimentions) with value of integers ranging from 0 to 255
    * Input
        * img - [image]
    * Params
        * removeAlpha: [bool] Most images have 4 values per pixel r,b,g,alpha, where alpha is something like transparency - alpha is not used in most ML cases.  True means remove alpha while converting
            * default - False
            * Optional - True
        * includeBatch: [bool] Often ML requires a dimension for batch (multiple images), if true dimensions = 4 with first dimension the batch, otherwise this produces a 3-D tensor (width, height, color).
            * default - False
            * Optional - True
    * OutputType - [array of array or arrays (3D or 4D matrix)]
* __tensor2image__: Converts a mathematical tensor (i.e. an array of any number of dimentions, for an image usualy 3Ds used, x,y,color) into an image
    * Input
        * tensor [array]
    * Params
        * extenstion [string] - image type to convert too: jpg, png, bmp
    * OutputType

_Utils_
* __runCML__: Runs another CML data preperation structure within the current structure. Allows you to integrate other CML structures into your JSON and pass standardized processing between languages.
    * Input
        * data - [any/object] the input data for the CML structure
    * Params
        * cmlFileName - path to where the json file that contains the CML structure.
    * OutputType - [any]
* __applyToInputs__: Applies the name operation to the list of inputs and params.  This way you do not have to list oneHotEncoding (for example) 10 times for each of your catagorical data columns.
    * Input
        * operation/function [string] - operation to apply
        * inputs - [list of objects(defined in named operation)]
        * params - [list of objects(defined in named operation)]
    * Params
        * None
    * OutputType - [any]
    * Output - single string adds output to that variable, list of strings applies output of each input object to the corresponding outputlist item

#### Operations in implementaitons:

To aid in integrating implementations of this specification into GUI interfaces and IDEs every operation should be defined by a JSON.  All of the above operations are given in the operations directory.  The JSON to define an operation is define as follows, with mulitple objects allowed in the lists for "input" and "params":
```
{
    “title”:”title”,
    “desc”:”description”,
    "input":[
	        {
                "name":"name", 
                "type":"type", 
                "description":"description", 
                "optional":"boolean",
                "allowed":"list of allowed"
            }
	    ],
    "params":[
	        {
                "name":"name", 
                "type":"type", 
                "description":"description", 
                "optional":"boolean",
                "allowed":"list of allowed"
            }
    	],
    "output":"type"
}
```

### Outputs:


The structure of the “output” object of a feature preparation specification structure is intended to allow for the construction of complicated output object ranging from a string to a full JSON type mix of maps and lists.  The “output” object should allow for values to include both objects defined in “operations”, “inputs”, hand values, AND further “output” objects (i.e. output objects can be nested/recursive).  The “output” object has two fields “type”, and “data” where the type defined in “type” determines how “data” is constructed.  If a hash table object (map or data frame) is used for type then data is built as a JSON object. If type is a list object ”data” is built as an array of data values.  If "type" does not match "data" and error should be raised.

* __output__: [map object] a JSON object defining the output
    * "Type": [string] - data designation 
        * (i.e. "map[string]any", "array[int]", etc.)
    * "Data": data of defined type constructed from inputs and operation ids.

Constructed as an object from hand defined keys and data references. 
