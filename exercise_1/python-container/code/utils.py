import logging
import setup
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, Integer, String, Float

def logger_setup():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='./log/docebo-test.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s %(asctime)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.getLogger().setLevel(logging.DEBUG)


def extract_columns_datatype(columns):
    '''
    :param columns: a dictionary containing metadata columns with their metadata
    :return: a dictionary containing for each metadata column its data type
    '''
    datatype_dict = {}
    for column in columns:
        if column['dataTypeName'] == 'number':
            datatype_dict[column['name']] = float
        else:
            datatype_dict[column['name']] = str
    return datatype_dict


def transform_table_name(table_name):
    '''
    :param table_name: a string containing the name of the table to upload
    :return: the same string but with '_' between words in it and in uppercase
    '''
    splitted_name = table_name.split()
    official_table_name = splitted_name[0].upper()
    splitted_name = splitted_name[1:]
    for name_part in splitted_name:
        official_table_name += "_" + name_part.upper()

    return official_table_name


def check_field_data_type(column_name, column_datatype, column_width, is_metadata):
    '''
    :param column_name: name of the column under evaluation 
    :param column_datatype: data type of the column under evaluation
    :param column_width: scale/precision of the datatype
    :return: a string part of the create statement 
    '''
    if column_name in setup.SPECIFIC_FIELDS_TYPE_CONVERTER_DICT:
        return setup.SPECIFIC_FIELDS_TYPE_CONVERTER_DICT[column_name] + ', \n'
    else:
        if is_metadata:
            return setup.TYPE_CONVERTER_DICT[column_datatype] + ', \n'
        elif column_datatype == 'text':
            return setup.TYPE_CONVERTER_DICT[column_datatype] + f'({column_width}), \n'
        else:
            return setup.TYPE_CONVERTER_DICT[column_datatype] + ', \n'


def is_metadata(column_datatype):
    '''
    :param column_datatype: the datatype column to check
    :return: true - if it's metadata; false - if it's not
    '''
    if column_datatype == 'meta_data':
        return True
    else:
        return False


def create_table_statement_setup(table_name, columns_metadata):
    '''
    :param table_name: the name of the table to create
    :param columns_metadata: a dictionary of metadata about table columns
    :return: stmt - a complete create table statement
    '''
    stmt = ''
    is_metadata_flg = False
    for column in columns_metadata:
        stmt = stmt + '\t' + column['name'] + '\t'
        is_metadata_flg = is_metadata(column['dataTypeName'])
        if(is_metadata_flg):
            stmt += check_field_data_type(column['name'], column['dataTypeName'], None, is_metadata_flg)
        else:
            stmt += check_field_data_type(column['name'], column['dataTypeName'], column['width'], is_metadata_flg)
        
    stmt = f'CREATE TABLE {table_name} \n (\n{stmt[:-3]}\n)'
    
    return stmt


def get_engine():
    '''
    :return: return a sqlalchemy engine to execute statements of the database 
    '''
    return create_engine(
        f'postgresql+psycopg2://{setup.USER}:{setup.PASSWORD}@{setup.HOST}/{setup.DATABASE}')


def drop_and_create_table(create_stmt, drop_stmt, connection_params):
    '''
    :param create_stmt: create statement to execute on the database
    :param drop_stmt: drop statement to execute on the database
    :param connection_params: connection parameters to connect to the database
    :return: -
    '''
    conn = None
    try:
        conn = psycopg2.connect(**connection_params)
        logging.info("Connection established with the db to create the table")
        cursor = conn.cursor()
        if setup.DROP_TABLE_BEFORE_CREATE == True:
            logging.debug(f'Executing: {drop_stmt}')
            cursor.execute(drop_stmt)
        logging.debug(f'Executing: \n {create_stmt}')
        cursor.execute(create_stmt)
        conn.commit()
        logging.debug("Transaction committed")
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as err:
        logging.error(err)
    finally:
        if conn is not None:
            conn.close()
            logging.info("Database connection closed")


def dataframe_datatype_for_insert(columns):
    '''
    :param columns: dictionary containing meta-data data of dataframe columns 
    :return: dictionary_data_datatype - a dictionary containig for each column it's datatype
    '''
    dictionary_data_datatype = {}
    for column in columns:
        column_name = column['name']
        column_datatype = column['dataTypeName']
        is_metadata_flg = is_metadata(column_datatype)
        if column_datatype == 'number':
            dictionary_data_datatype[column_name] = Float()
        elif is_metadata_flg:
            if column_name in setup.INTEGER_COLUMNS:
                dictionary_data_datatype[column_name] = Integer()
            else:
                dictionary_data_datatype[column_name] = String(1000)
        else:
            precision = column['width']
            dictionary_data_datatype[column_name] = String(precision)

    return dictionary_data_datatype

def insert_data(dataframe, columns_datatypes_dictionary, table_name):
    '''
    :param dataframe: the dataframe containing all the data 
    :param columns_datatypes_dictionary: a dictionary containing for each column of the dataframe, the relative datatype
    :param table_name: name of the destination table
    :return: -
    '''
    engine = get_engine()
    conn = None
    try:
        conn = engine.connect()
        logging.info("Connection established to insert data")
        dataframe.to_sql(name=table_name.lower(), con=conn, dtype=columns_datatypes_dictionary, if_exists='append', index=False)
        logging.info("Records inserted")
    except (Exception, psycopg2.DatabaseError) as err:
        logging.error(err)
    finally:
        if conn is not None:
            conn.close()
            logging.info("Database connection closed")
            
            
def remove_useless_dataframe_columns(columns, dataframe):
    '''
    :param columns: columns of the dataframe with associated meta-data 
    :return: the dataframe with just usefull columns and the updated list of columns
    '''
    logging.debug("Removal of useless metadata columns")
    columns = [column for column in columns if column['name'] not in setup.USELESS_COLUMNS_TO_DROP]
    dataframe_columns_names = [column['name'] for column in columns]
    dataframe = dataframe[dataframe_columns_names]
    return dataframe, columns
