# Docebo test for Data Engineer Analytics position

## Exercise 1

### Database setup
In *exercise_1/* folder you can find the docker-compose file with it's *.env* file associated. 
You can launch the container (in this case is a Postgresql container) with the simple command:

```bash
docker-compose -d up
```

where *-d* option stands for 'detached'.

When finished, don't forget to close everything with 

```bash
docker-compose down
```

### Table creation and data upload
In the *code/* folder, you can find all the python scripts to create and populate the table described in *sources/dataset.json* file. 

In details:
- main.py - contains the main execution of the script
- setup.py - contains some variables to set up in order to change the execution 
- utils.py - is a collection of functions
- classes/databaseConfigManager.py - is a simple class to manage the database configurations
- log/docebo-test.log - is the log file (overwritten for each execution)

I've used a virtualenv to execute everything but all the requirements could be installed with [pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```

#### Setup parameters

```python
HOST = 'localhost'  # database hostname
USER = 'username'   # database username
PASSWORD = 'password'   # database password
DATABASE = 'docebo_database'   # database name
DROP_STMT = 'DROP TABLE IF EXISTS '   # drop table statement to use
TYPE_CONVERTER_DICT = {'number':'FLOAT', 'text':'VARCHAR', 'meta_data': 'VARCHAR(1000)'}   # database datatypes to assign for different .json datatypes
SPECIFIC_FIELDS_TYPE_CONVERTER_DICT = {'created_at':'INTEGER', 'updated_at':'INTEGER'}   # specific datatypes for certain fields
INTEGER_COLUMNS = ['created_at', 'updated_at']   # list of columns who needs to be converted into sqlalchemy integers
USELESS_COLUMNS_TO_DROP = ['sid', 'id', 'position', 'meta', 'created_meta', 'updated_meta']   # list of columns to drop from the table
DROP_RECORD_IF_NULL_FIELDS = ['StateName', 'ReportYear', 'Value', 'MeasureName', 'CountyName']   # list of columns to clean NULL values 
DROP_TABLE_BEFORE_CREATE = True   # true - if the table needs to be dropped before creation / false - if it's the first load
ZERO_VALUE_RECORDS_REMOVAL = True   # true - if you want to remove records where value = 0
```

## Exercise 2
In the *exercise_2* folder you can find the .sql script containing all the requested queries.
