# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from scrapy.conf import settings
from sqlalchemy.orm import sessionmaker


def sql_engine(database=None, pool_size=10, server='postgresql'):

    host = settings['SQL_HOST']
    user = settings['SQL_USER']
    password = settings['SQL_PASSWORD']

    if server == 'postgresql':

        template = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}?client_encoding=utf8'
        port = 5432
        return create_engine(
            template.format(user=user,
                            password=password,
                            host=host,
                            database=database,
                            port=port), pool_size=pool_size)

    elif server == 'mysql':

        template = 'mysql://{user}:{password}@{host}:{port}/{database}'
        port = 3306
        return create_engine(
            template.format(user=user,
                            password=password,
                            host=host,
                            database=database,
                            port=port), pool_size=pool_size)

    elif server == 'mssql':

        template = 'mssql+pymssql://{user}:{password}@{host}:{port}/{database}'
        port = 1433
        return create_engine(
            template.format(user=user,
                            password=password,
                            host=host,
                            database=database,
                            port=port), pool_size=pool_size)

if __name__ == "__main__" :

    engine= sql_engine(database='dev_main')
    session = sessionmaker(bind=engine)



