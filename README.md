# CatalystML

## Overview

The purpose of the CatalystML specification is to facilitate the easy transformation of data from an input source such that it is ready for input into an ML model.  A related secondary purpose is to transform data from an ML model into a final presentable format.  This specification will be defined in a JSON format so that it is language agnostic with the expectation that language specific implementations can interpret the specification and process incoming data.  This document seeks to lay out the expected structure and behavior of such interpreters.  A single JSON document is intended to represent a single Preparation Pipeline.

## Implementations

This specification is intended to demonstrate a language agnostic format for describing data processing.  However, to be used it needs to be implemented.  Currently, The following languages/frameworks have an implementation of the specification.

* Project Flogo®
