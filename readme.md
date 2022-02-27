# Jason M's Entry
This ETL solution takes data from provided csvs and formats it then inserts it into a postgres database

This solution provides a postgres database to run locally
## System Requirements
You will need to have docker installed on your system. Make sure that docker is running before following the steps to start the solution

Also, you may need a database tool in order to execute some sql code

Ports 5432 and 8008 will need to be available on your system


## Starting the solution
* From the command line, navigate to this current directory
* Run the following command to start the database
```
docker-compose up postgres -d
```
* You can optionally remove '-d' if you would like to view the logs
* Connect to the database using sa:Password123. Postgres is running on port 5432
* Run the sql in "create_tables.sql" to create the tables
* Once the tables are created, navigate back to the cli and run the following command
```
docker-compose up backend -d
```

## Running ETL job 
### via Browser
* In your browser, you can navigate to localhost:8008/api, where a swagger file is set up to test the endpoints
* Using the endpoint **/listings/import/{provider}/{csvname}**, you will be able to test the job
    * **provider** currently takes either 1 or 2, for the current providers available
    * **csvname** is the name of the csv file (without extension) to import

### via Unix based CLI
* Run the collowing command:
```
curl -X 'GET' \
  'http://localhost:8008/api/listings/import/{provider}/{csvname}' \
  -H 'accept: application/json'
```
### via Powershell CLI
* Run the collowing command:
```
 Invoke-WebRequest -Uri http://localhost:8008/api/listings/import/{provider}/{csvname}
```

## Clearing the database
I also added a quick way to reset the data in the database in case retrying is needed. You can use the **/listings/clear** endpoint

### via Unix based CLI
```
curl -X 'GET' \
  'http://localhost:8008/api/listings/clear' \
  -H 'accept: application/json'
```
### via Powershell CLI
```
 Invoke-WebRequest -Uri http://localhost:8008/api/listings/clear
```