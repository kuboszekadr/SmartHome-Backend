# SmartHome-Backend

## About

This component is responsible for transferring data between data to/from database. At the moment following endpoints are available:

- api/data_collector - here data are being send from sensors and pushed into database,
- api/date - returns current server timestamp,
- api/chart_data - endpoint for front-end to get dashboard data.

There are arduino-legacy endpoint, but they will be deprecated once new version of aquarium driver will be released.

You can specify on which port application shall run in the _Dockerfile_.

## Endpoints

### data_collector 
