# Feature Preperation Specification

## Introduction

The purpose of this specification is to facilitate the easy transformation of data from an input source such that it is ready for input into an ML model.  A related secondary purpose is to transform data from an ML model into a final presentable format.  This specification will be defined in a JSON format so that it is language agnostic with the expectation that language specific implementations can interpret the specification and process incoming data.  This document seeks to lay out the expected structure and behavior of such interpreters.  A single JSON document is intended to represent a single Preparation Pipeline.

## General Structure

The specification will be represented within a JSON format.  The first level of the JSON format will contain:
1. __General information of the specification__ - i.e. name for the feature processing pipeline, version, target model metadata, ...
 
2. __Inputs__ - a list describing the data to be processed types, labels, etc.
3. __Pipeline__ - a list of the functions to operate on the data
4. __Outputs__ - describing how the processed data is to be output

## Types and Structures

Throughout the specification (especially in Inputs and Outputs) data types and structures are used to represent data.  Here we define and discuss the supported data types.  The types fall into two categories structures and types.  Structures are object types (lists, maps, data frames) that can be constructed with values that are either data types or other data structures.

* data structures:
    * "list" - is an array of objects
    * "map" - a hash table of key value pairs - values are data types
    * "dataframe" - a hash table of key value pairs - values are lists (constrained type?)
* data types:
    * "string"
    * "int32"
    * "int64"
    * "float32"
    * "float64"
    * "boolean"

Since strings and data references are both surrounded by quotes to distinguish between them data references have a “$” at the beginning of the label.

## Object Names:

When an object is defined either within input or as the output of an operation the object is given the name corresponding to the value associated with the “label” key.  This name can then be used to refer to this object in either another operation’s input or as a component of the pipeline output.  Collisions of labels should raise a warning during pipeline build time, but still allow for data overwrite. For maps, dataframes, and lists the columns/keys can be reference by appending the column/key to the end of the object name surrounded by square brackets.  For example a dataframe object named df with columns “col0”, “col1”, etc could have its first column called with “df[col0]”.  Similarly, list objects can have their components referred by their index number by appending the index to the end of the object name surrounded by square brackets.  For multi-dimensional list each index would be within their own brackets.  For example a list of lists (2D) named “matrix” could refer to a component as “matrix[0][3]” .  Indexes for lists begin at 0.

## Structure Specification:

### General Information:

General information describes several key:value pairs within the first level of the Preparation Pipeline JSON that contains information and metadata for the Pipeline.  These values are optional.


* _Name_ - [string] - General name for the Pipeline i.e. AccelerometerProcessing
* _Description_ -  [string] - A note that describes the purpose/use case of the pipeline
* _Version_- [string] - Version of pipeline i.e. 0.8.3
* _createdDate_: [string] - the date the pipeline was created
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

### Pipeline Operations:
The pipeline key in the JSON specification defines the list of operations that define the pipeline Operations are to be executed in the order listed in the Operations list.  The pipeline structure (and the basic structure for operations) is defined as:

Pipeline: [array of objects] defines a list containing all operations - the operations objects are of the form:
* Operation- [string] name of operation (i.e. norm, scale, etc.)
    * Input -  [map object] describes the inputs:
        * Data: value of a labeled variable or a list of values
        * Other keys specific to operation possible
    * Params - object containing operation specific parameters (optional?)
    * Output: - name of the output of the operation

Below are a list of operations (and their expected results) supported by this specification by category.


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

_Cleaning_:
* __replaceValue__: Given a map replaces data (key) with map value 
    * Input
        * Data - [array or dataframe]
            * Optional=False
        * Value - [int, float, string, NaN]
	        * Optional=True
	        * Default=NaN
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
        * Data - [array of arrays or dataframe]
			* Optional=False
        * Col - map key or column number
    * Params
        * outlierType [string]
			* Optional=True
			* Default = “Negatives”
			* Accepted Values - “Negatives”,
    * Output - [array or map] (same type as inputs)
* __arrange/sort__:  sort a matrix/dataframe based on given columns
* __filter__:  keep/remove rows with certain values
    * Input
        * Data - [array or dataframe]
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
* __pivot__:  reshape a matrix or dataframe by re-indexing like the pivot function in pandas
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
* __map2Table__: convert a map/dataframe to a matrix
* __table2Map__: convert a matrix to a map/dataframe by adding a name to each column

_Categorical_:
* __binning__: take a numerical list and convert it into bins
* __oneHotEncoding__: convert categorical vector into a set of vectors for each category with a 0/1
* __targetEncoding__: replace categorical value with its average of another numerical column

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


_NLP_:
* __Tokenization__: separate text into tokens / words / punctuation
* __Word2embedding__: convert words from list to array of wordlist x numerical embedding
* __Embedding2word__: convert list of embedding to closest words
* __removeStop__: given text and list of (stop) words - removes those words from text.

_Image Processing_:
* __resize__: change dimensions of image
* __removeAlpha__:  Most images have 4 values per pixel r,b,g,alpha, where alpha is something like transparency - alpha is not used in most ML cases
* __Grayscale__: Convert color image to grayscale
* __subSectionToImage__: takes a portion of an image and makes it an independent image (i.e. for selecting out a face)
* __addBoxLabel__: Add box and Label to an image given location (FOR POST PROCESSING)

_Custom Operations_:
* Language specific method for defining a custom operation (i.e. in go using go get)

### Outputs:
* __output__: [map object] a JSON object defining the output

The structure of the “output” object of a feature preparation specification pipeline is intended to allow for the construction of complicated output object ranging from a string to a full JSON type mix of maps and lists.  The “output” object should allow for values to include both objects defined in “operations”, “inputs”, hand values, AND further “output” objects (i.e. output objects can be nested/recursive).  The “output” object has two fields “type”, and “data” where the type defined in “type” determines how “data” is constructed.  If a hash table object (map or data frame) is used for type then data is built as a JSON object. If type is a list object ”data” is built as an array of data values.
* “Type”: the type of data object out
* “Data”: is of the type defined in the “Type” key.  Constructed as an object from hand defined keys and data references. 
