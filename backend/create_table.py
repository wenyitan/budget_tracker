from database import Database

# Initialize the database
db = Database()

# Drop table
drop_table_query = "DROP TABLE IF EXISTS transactions;"

db.execute(drop_table_query)

# Create the transactions table
create_table_query = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL,
    person TEXT NOT NULL
);
"""



db.execute(create_table_query)

# Close the connection
db.close()