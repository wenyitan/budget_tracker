from config import TABLE_NAME

create_transaction_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTO INCREMENT,
        amount REAL NOT NULL,
        person TEXT NOT NULL,
        date TEXT NOT NULL, 
        FOREIGN KEY (category_id) REFERENCES categories(id),
        description TEXT default '',
        shared INTEGER default 1
    );
"""    # date stored as 'DD-MMM-YYYY' for example '12-Apr-2025', shared is boolean where 1 is true and 0 is false

create_categories_table_query = f"""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTO INCREMENT,
        category TEXT UNIQUE NOT NULL
    );
"""    

create_table_queries = [create_categories_table_query, create_transaction_table_query]