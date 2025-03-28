
# Testing Scope

**Release Type**: Initial Test Deployment

**Release Features**: Log-in and sign-up functionality, Log-in recovery, data streaming of sensor readings, accurate projection of data to graphs, map display functionality, data correlation tool functionality.

**Prior Regressions areas**: 
> Stream processor was rewritten and remade.
> map and studio page were re-written from gorund up to be interactive,.
> data base schema has been rewritten multiple times and has moved from influx DB to postgres.
> rewritten authentication multiple times due to security vulnerabilities.

# Defining Test Objectives

**Security Testing**

> Test password hash encryption functionality

> ZAP security test

**Performance testing**:

> Lighthouse performance testing on each page 

**Functionality Testing**:

> Log/sign in functionality

> Password recovery functionality

> test the gradient function of the river display

> Map display settings
    
**Usability Testing**:

> Mobile display accessability

> Webpage display accessability
                                      