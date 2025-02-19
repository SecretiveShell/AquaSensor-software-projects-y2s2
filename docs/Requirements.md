# Requirements

## Project Overview

The project aims to create a simple, scalable, and secure system for monitoring water quality in real time.

## Problem Statement

Water quality is a critical issue in many communities, and it is essential to monitor and maintain water quality levels. However, monitoring water quality in real time can be challenging due to the large amount of data that needs to be collected and analyzed. This project must a simple way to interpret and visualize water quality data in real time for casual users.

## Project Objectives

- view water quality over time
- visualize the data in the style of a river
- see current water quality at a glance
- interact with the data in an intuitive and visual way

## System Requirements

## Functional Requirements

| ID    | Theme         | Description                                                                               | Priority (MoSCoW) |
| ----- | ------------- | ----------------------------------------------------------------------------------------- | ----------------- |
| FR001 | Integration   | The system must integrate data streams using APIs and the MQTT protocol                   | Must              |
| FR002 | Visualization | The system must provide intuitive visualizations for dissolved oxygen and other metrics   | Must              |
| FR003 | Visualization | The system should show both location-based and parameter-based data changes               | Should            |
| FR004 | External Data | The system should integrate open-source geospatial and hydrological data                  | Should            |
| FR005 | Correlation   | The system should develop tools to correlate data                                         | Should            |
| FR006 | Application   | The system must include a user-friendly web application                                   | Must              |
| FR007 | Application   | The application should support real-time and historical data interaction                  | Should            |
| FR008 | Accessibility | The application must cater to a wide range of users, from ecologists to community members | Must              |
| FR009 | Integration   | The application could provide warnings about sudden drastic changes in water quality      | Could             |

## Non Functional Requirements

| ID     | Theme         | Description                                                              | Priority (MoSCoW) |
| ------ | ------------- | ------------------------------------------------------------------------ | ----------------- |
| NFR001 | Accessibility | The system must be mobile friendly                                       | Must              |
| NFR002 | Accessibility | The system must work with screen readers                                 | Should            |
| NFR003 | Accessibility | The system must be accessible to people with disabilities                | Should            |
| NFR004 | Usability     | The system must be simple and intuitive to use                           | Must              |
| NFR005 | Security      | The system must be secure                                                | Must              |
| NFR006 | Security      | All passwords must be hashed and salted                                  | Must              |
| NFR007 | Security      | All endpoints should have a rate limit if they have intensive operations | Should            |
| NFR008 | Security      | All endpoints that deal with personal data should be authenticated       | Should            |
| NFR009 | Security      | All transport must support SSL                                           | Must              |
| NFR010 | Scalability   | The system must be scalable horizontally                                 | Must              |
| NFR011 | Scalability   | The system must be reliable                                              | Must              |
| NFR012 | Scalability   | The system should include health checks                                  | Should            |
