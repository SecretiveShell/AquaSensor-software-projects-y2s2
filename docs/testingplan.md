
# Testing Scope

**Release Type**: Initial Test Deployment

**Release Features**: Log-in and sign-up functionality, Log-in recovery, data streaming of sensor readings, accurate projection of data to graphs, heat map display functionality.   

**Prior Regressions areas**: 
> Stream processor was rewritten and remade.
> map and studio page were re-written from gorund up to be interactive,.
> data base schema has been rewritten multiple times and has moved from influx DB to postgres.
> rewritten authentication multiple times due to security vulnerabilities.

# Defining Test Objectives

**Security Testing**

> Test password hash encryption functionality

> Token generation security

**Performance testing**:

> Requests per second

> Latency Testing 

> Webpage Ram Usage

**Functionality Testing**:

> Log/sign in functionality

> Password recovery functionality

> use test data to test the gradient function of the river display

**Usability Testing**:

> Mobile display accessability

> Webpage display accessability
