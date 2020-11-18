import psycopg2
from assistant_secrets import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_PORT
)

try:
    connection = psycopg2.connect(user=DATABASE_USER,
                                  password=DATABASE_PASSWORD,
                                  host=DATABASE_HOST,
                                  port=DATABASE_PORT,
                                  database=DATABASE_NAME)

    cursor = connection.cursor()
    cursor.execute("SELECT name from shoppinglist_product;")
    print(cursor.fetchall())
except (Exception, psycopg2.Error) as error:
    print("Error while accessing to products", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("Finished")
