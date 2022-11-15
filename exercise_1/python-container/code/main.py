import pandas as pd
import json
import logging
import utils
import setup
import time
from classes.databaseConfigManager import databaseConfigManager as db_config_manager

if __name__ == '__main__':
    utils.logger_setup()
    logging.info("Docebo-test app is starting")
    logging.debug("Database connection params setup")
    postgres_config_manager = db_config_manager(setup.HOST, setup.USER, setup.PASSWORD, setup.DATABASE)
    postgres_config_params = postgres_config_manager.database_connection_info

    with open('./sources/dataset.json') as catalog:
        logging.debug("Uploading the dataset")
        dataset = json.load(catalog)
    
    table_name = dataset['meta']['view']['name']
    table_name = utils.transform_table_name(table_name)
    logging.info(f'Uploading table {table_name}')
    columns_metadata = dataset['meta']['view']['columns']
    headers = [column['name'] for column in columns_metadata]
    data = dataset['data']
    logging.debug("Creating the pandas dataframe")
    dataframe = pd.DataFrame(data, columns=headers)

    if len(setup.USELESS_COLUMNS_TO_DROP) != 0:
        dataframe, columns_metadata = utils.remove_useless_dataframe_columns(columns_metadata, dataframe)

    logging.debug("Converting dataframe columns to its own type")
    dataframe = dataframe.astype(utils.extract_columns_datatype(columns_metadata))

    if setup.DROP_TABLE_BEFORE_CREATE:
        logging.debug("Drop and create statements setup")
        drop_table_stmt = setup.DROP_STMT + table_name
        create_table_stmt = utils.create_table_statement_setup(table_name, columns_metadata)
        utils.drop_and_create_table(create_table_stmt, drop_table_stmt, postgres_config_params)
    else:
        logging.debug("Create table without dropping it before")
        drop_table_stmt = None
        create_table_stmt = utils.create_table_statement_setup(table_name, columns_metadata)
        utils.drop_and_create_table(create_table_stmt, drop_table_stmt, postgres_config_params)

    if setup.ZERO_VALUE_RECORDS_REMOVAL:
        dataframe.drop(dataframe.index[dataframe['Value'] == 0], inplace=True)

    dataframe.dropna(subset=setup.DROP_RECORD_IF_NULL_FIELDS, inplace=True, how='any')
    
    columns_datatypes_dict = utils.dataframe_datatype_for_insert(columns_metadata)

    dataframe.columns = map(str.lower, dataframe.columns)
    utils.insert_data(dataframe, columns_datatypes_dict, table_name)

    time.sleep(setup.WAIT_TO_END)

    




