import configparser
from sqlalchemy import create_engine

def connection(user: str, pwd: str):
    """
    Reads db connection parameters from config file and returns connection cursor to db

    :param
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    db_config = config['DATABASE']  # get section responsible for db connection
    db_host = db_config['Host']
    db_name = db_config['DBName']
    db_port = db_config['Port']

    conn = create_engine('postgresql://{usr}:{pwd}@{host}:{port}/{db}'.\
        format(usr=user,
               pwd=pwd,
               host=db_host,
               port=db_port,
               db=db_name))
    
    return conn
