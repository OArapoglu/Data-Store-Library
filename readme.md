 # DATA STORE LIBRARY API TASK #
This task includes data storing operations which are put, update, delete, filter as well as tests in pytest.  
<br />
The fundamental modules and their definitions are as follows:
- app.py: It is the main file of Flask.
- db.db_service: It includes DB configurations and connections in singleton pattern.
- orm.orm_service: It includes ORM classes of the DB tables in singleton pattern.
- data.destination: It includes destination files in factory design pattern.
- data.format: It includes format files in factory design pattern.
- data.data_service.py It manages all data storage operations according to the request in singleton pattern.
- tests.test_api.py: It includes the test scenarios for data store operations in Pytest.

### How to Run Program ###
Activate virtual environment.
<br/>
Below code for Windows.
```commandline
. env/scripts/activate
```

In this API, PostgreSQL is used for DB and SqlAlchemy for ORM.
In order to change DB, configure DB settings of get_database_uri() function in db.db_service.

Flask Migrate Commands after configuring DB.
```commandline
flask db init
flask db migrate
```

Run Flask API operations.
```commandline
flask run
```

Run pytest
```commandline
python -m pytest
```

### API Endpoints ###
```commandline
Endpoint URL: /put
    Inputs:
        - api_key: str)
        - records: list[dict{key:value}]
        - files: list[dict{key:value}]
        - destinations: list[dict{key:value}]
        
Endpoint URL: /delete
    Inputs:
        - api_key: str)
        - record_keys: list[]

Endpoint URL: /update
    Inputs:
        - api_key: str)
        - records: list[dict{key:value}]

Endpoint URL: /filter_records
    Inputs:
        - api_key: str)
        - value: str
        - limit: Optional(int)
        - offset: Optional(int)
    Returns:
        list(dict{name, path, file_format, file_destination})
JSON Return Codes
    - 200: Successful
    - 400: Syntax Error
    - 500: Critical Error
```





