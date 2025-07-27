# INEAPIpy Folder Structure

## Documentation

Contains documentation about the INE API, this package, and INE API objects and relations diagrams, aswell as a diagram for quick undertanding of functions inputs and results.

## Models

Contains all pydantic models used in this package for checking inputs and results.

## urlrequestsmanagement

Submodule:
* Gitlab: https://gitlab.com/statssearchanalysis/statsapis/urlrequestsmanagement
* Github: https://github.com/VanceVisarisTenenbaum/URLRequestsManagement

## Bridge.py

Contains the classes that have the methods to make the requests and retreive the results from the API.

## The other files.

Except for Ine_functions.py, there is no need to use the other files. They simply contain functions to simplify the process of getting the data and making the urls.

### INE_functions.py

This file contains exactly the functions from INE API, they have some inputs, checke everything is correct and generate a url to make the request.
