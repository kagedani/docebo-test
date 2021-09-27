# Docebo test for Data Engineer Analytics position

## Exercise 1

### Database setup
In *exercise_1/* folder you can find the docker-compose file with its *.env* file associated. 
The docker-compose contains two containers:
1. the first one is for the postgresql database instance
2. the second one contains the python script to create the table and insert data into it

You can launch both with the simple command:

```bash
docker-compose up -d
```

where *-d* option stands for 'detached'.

When finished, don't forget to close everything with 

```bash
docker-compose down
```

### Table creation and data upload
In the *python-container/code/* folder, you can find all the python scripts to create and populate the table described in *sources/dataset.json* file. 

In details:
- main.py - contains the main execution of the script
- setup.py - contains some variables to set up in order to change the execution 
- utils.py - is a collection of functions
- classes/databaseConfigManager.py - is a simple class to manage the database configurations
- log/docebo-test.log - is the log file (overwritten for each execution)

If you use the docker-compose command, the *main.py* script will be executed automatically and it keeps going for 10 minutes after the data insertion, for log checks purpose.

If you prefere to install all dependencies right into your local machine, you can use [pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```

After the required libraries installation the program can be launched with 

```bash
python main.py
```

before doing so, I would suggest to have a look at the following section to eventually change some of the parameters of the script.

#### Setup parameters

```python
HOST = 'docebo-postgres'  # database hostname, needs to be set to 'localhost' in case of local execution
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
WAITING_TO_END = 600 # seconds to wait until the python container closure
```

If you are planning to use the docker-compose command and want to do multiple executions with different parameters, don't forget to launch 

```bash
docker-compose up -d --build
```

otherwise the changes would not be received by the python container.

**N.B.** if the table exists and you put the ```DROP_TABLE_BEFORE_CREATE``` parameter to *False*, it will return an error.

**N.B.2** in the parameter ```USELESS_COLUMNS_TO_DROP``` needs to be specified columns names that are not inserted into ```DROP_RECORD_IF_NULL_FIELDS```, otherwise the program would give an error not finding the column to check **null** values.


## Exercise 2
In the *exercise_2* folder you can find the .sql script containing all the requested queries.

## Exercise 3 
It is a PDF with all the answers to the third exercise proposed in the test.
