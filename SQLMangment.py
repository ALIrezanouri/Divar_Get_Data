import sqlite3
import logging
import sqlite3
import pandas as pd
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_database(db_name, table_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_type TEXT,
            fuel_type TEXT,
            engine_status TEXT,
            front_chassis TEXT,
            rear_chassis TEXT,
            body_status TEXT,
            insurance_deadline INTEGER,
            gearbox TEXT,
            base_price INTEGER,
            mileage INTEGER,
            model_year INTEGER,
            color TEXT,
            location TEXT,
            url TEXT UNIQUE
        );
        '''

        cursor.execute(create_table_query)
        conn.commit()
        conn.close()
        logging.info(f"Database {db_name} and table {table_name} created successfully.")

    except sqlite3.Error as e:
        logging.error(f"Error creating database or table: {e}")

def add_record(db_name, table_name, brand_type, fuel_type, engine_status, front_chassis, rear_chassis, body_status,
               insurance_deadline, gearbox, base_price, mileage, model_year, color, location, url):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        check_query = f"SELECT COUNT(*) FROM {table_name} WHERE url = ?"
        cursor.execute(check_query, (url,))
        result = cursor.fetchone()

        if result[0] > 0:
            logging.info(f"Record with URL {url} already exists.")
        else:
            insert_query = f'''
            INSERT INTO {table_name} (brand_type, fuel_type, engine_status, front_chassis, rear_chassis, body_status, insurance_deadline, gearbox, base_price, mileage, model_year, color, location, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            '''

            cursor.execute(insert_query, (
                brand_type, fuel_type, engine_status, front_chassis, rear_chassis, body_status, insurance_deadline, gearbox,
                base_price, mileage, model_year, color, location, url))

            conn.commit()
            logging.info(f"Record with URL {url} added successfully.")

        conn.close()

    except sqlite3.Error as e:
        logging.error(f"Error adding record to database: {e}")


def connect_to_pandas(table_name,db_name):
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df




def delete_record(db_name, table_name, brand_type=None, fuel_type=None, engine_state=None, front_chassis=None,
                  rear_chassis=None, body_status=None, insurance_deadline=None, gearbox=None, base_price=None,
                  mileage=None, model_year=None, color=None, location=None, url=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    conditions = []
    parameters = []
    if brand_type is not None:
        conditions.append("brand_type = ?")
        parameters.append(brand_type)
    if fuel_type is not None:
        conditions.append("fuel_type = ?")
        parameters.append(fuel_type)
    if engine_state is not None:
        conditions.append("engine_state = ?")
        parameters.append(engine_state)
    if front_chassis is not None:
        conditions.append("front_chassis = ?")
        parameters.append(front_chassis)
    if rear_chassis is not None:
        conditions.append("rear_chassis = ?")
        parameters.append(rear_chassis)
    if body_status is not None:
        conditions.append("body_status = ?")
        parameters.append(body_status)
    if insurance_deadline is not None:
        conditions.append("insurance_deadline = ?")
        parameters.append(insurance_deadline)
    if gearbox is not None:
        conditions.append("gearbox = ?")
        parameters.append(gearbox)
    if base_price is not None:
        conditions.append("base_price = ?")
        parameters.append(base_price)
    if mileage is not None:
        conditions.append("mileage = ?")
        parameters.append(mileage)
    if model_year is not None:
        conditions.append("model_year = ?")
        parameters.append(model_year)
    if color is not None:
        conditions.append("color = ?")
        parameters.append(color)
    if location is not None:
        conditions.append("location = ?")
        parameters.append(location)
    if url is not None:
        conditions.append("url = ?")
        parameters.append(url)
    if not conditions:
        return
    query = f"DELETE FROM {table_name} WHERE " + " AND ".join(conditions)
    cursor.execute(query, tuple(parameters))
    conn.commit()
    conn.close()








