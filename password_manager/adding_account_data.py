import sqlite3
import pandas as pd
from datetime import datetime
from sqlalchemy import null

# connecting to database.
try:
    conn = sqlite3.connect(r'path\to\file\password_manager.db')
    cursor = conn.cursor()
    print('Connection succesful')
except:
    print('Connection failed')

# adding existing account data to database.
def add_data(host, username, email, password):

# sets the current date and time to the time a password is added.
    now = datetime.now().strftime('%Y-%m-%d-%H:%M')

# Inserts a website or app, username, email, and password a user provides.
# The date is added automatically at the time a user inserts their account data.
# insert or ignore prevents the script from adding duplicate data.
# the try-except block informs the user whether the data was added successfully.
    try:
        cursor.execute('insert or ignore into password_database (host, username, email, password, date) values (?, ?, ?, ?, ?);',
                   (host, username, email, password, now)
                       )
        conn.commit()
        print('Data inserted successfully')
    except sqlite3.Error as e:
        print(f'Database error: {e}')
    except:
        print('Data already exists')

# ensures the script returns all rows from the password database table.
pd.set_option('display.max_columns', None)

print(add_data('website or app', 'username', 'your@email.com', 'P@$sw0rD'))
print(pd.read_sql_query('select * from password_database', conn))

