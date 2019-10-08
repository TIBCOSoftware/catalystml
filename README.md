# CatalystML

## Overview

The purpose of CatalystML is to facilitate the transformation of data from an input source such that it is ready for input into an ML model.  A related secondary purpose is to transform data from an ML model into a final presentable format.  This specification will be defined in a JSON format so that it is language agnostic with the expectation that language specific implementations can interpret the specification and process incoming data.  This specification document seeks to lay out the expected structure and behavior of such interpreters.  A single JSON document is intended to represent a single Preparation Structure.

A catalyst in chemistry is chemical that allows a given chemical reaction occur more easily without fundamentally changing the reaction.  CatalystML seeks to make it easier to transform data especially wihtin a streaming real time production environment such that the transformed data can be input into Machine Learning models.

## Demos

The demos provided in the main directory of this repository with their inputs and outputs are always intended to work with the most recent version of the specification.

## Implementations

This specification is intended to demonstrate a language agnostic format for describing data processing.  However, to be used it needs to be implemented.  Currently, The following languages have an implementation of the specification:

* [Go/Flogo implementation](https://github.com/project-flogo/catalystml-flogo) (under developement)