import pandas as pd
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



data_file = 'DB_data.xlsx'

# try:
#     # Подключение к существующей базе данных
#     conn = psycopg2.connect(user="postgres",
#                                   # пароль, который указали при установке PostgreSQL
#                                   password="1234",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database='test_db')
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     # Курсор для выполнения операций с базой данных
#     cursor = conn.cursor()

    # Создание ДБ
    # sql_create_database = 'create database test_db'
    # cursor.execute(sql_create_database)

    # create_addr_table = """ CREATE TABLE IF NOT EXISTS Address
    #                                       (id INT PRIMARY KEY NOT NULL,
    #                                       Address_Code INT UNIQUE NOT NULL,
    #                                       Region VARCHAR(255),
    #                                       City VARCHAR(255),
    #                                       Postal_Code INT,
    #                                       Street VARCHAR(255),
    #                                       House VARCHAR(255));  """
    # cursor.execute(create_addr_table)
    # print("Таблица Addresses успешно создана")


    # create_pt_table = """ CREATE TABLE IF NOT EXISTS PaymentTerms
    #                                       (id INT PRIMARY KEY NOT NULL,
    #                                       Pay_term VARCHAR UNIQUE NOT NULL,
    #                                       PT_description VARCHAR(255));  """
    # cursor.execute(create_pt_table)
    # print("Таблица PaymentTerms успешно создана")

    # create_lob_table = """ CREATE TABLE IF NOT EXISTS LoB
    #                                       (id INT PRIMARY KEY NOT NULL,
    #                                       LoB VARCHAR UNIQUE NOT NULL);  """
    # cursor.execute(create_lob_table)
    # print("Таблица LoB успешно создана")


    # create_stl_table = """ CREATE TABLE IF NOT EXISTS STLs
    #                                       (id INT PRIMARY KEY NOT NULL,
    #                                       STL VARCHAR UNIQUE NOT NULL);  """
    # cursor.execute(create_stl_table)
    # print("Таблица STLs успешно создана")


    # create_am_table = """ CREATE TABLE IF NOT EXISTS Managers
    #                                       (id INT PRIMARY KEY NOT NULL,
    #                                       Sales_Grp VARCHAR UNIQUE NOT NULL,
    #                                       AM_name VARCHAR NOT NULL,
    #                                       SO_code VARCHAR NOT NULL,
    #                                       STL_id INT,
    #                                       LoB_id INT,
    #                                       FOREIGN KEY (STL_id) REFERENCES STLs (id),
    #                                       FOREIGN KEY (LoB_id) REFERENCES LoB (id)
    #                                       );  """
    # cursor.execute(create_am_table)
    # print("Таблица Managers успешно создана")
    # conn.commit()


    # update Addresses
addr_data = pd.read_excel(data_file, sheet_name="Addresses")
# addr_data.to_sql(name='Address', con=conn, if_exists='replace', index=False)
#print(addr_data)
addr_info = []
for row in addr_data:
    address = {
        'Address_Code': row['Address_Code'],
        'Region': row['Region'],
        'City': row['City'],
        'Postal_Code': row['Postal_Code'],
        'Street': row['Street'],
        'House': row['House']
    }
    addr_info.append(address)
print(addr_info)


# except (Exception, Error) as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     if conn:
#         cursor.close()
#         conn.close()
#         print("Соединение с PostgreSQL закрыто")
