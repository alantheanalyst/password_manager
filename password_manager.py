import random
import string
import sqlite3
import pandas as pd
from datetime import datetime

# creating and connecting to database,
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

# creating the table and determining if it already exists every time the code is executed.
# autoincrement ensures a unique identifier is generated each time a user stores a password.
# unique ensures that duplicate data isn't inserted everytime the script is executed.
try:
    cursor.execute('''
create table if not exists password_database (
ID integer primary key autoincrement,
host varchar (223),
username varchar (223),
email varchar (223),
password varchar(223),
date date,
unique(host, username, email)
);
''')
    conn.commit()
    print('table created successfully')
except:
    print('table already exists')

def password_generator():

# setting the length of the password between 14-16 characters.
    length = random.randint(14, 16)

# ensures the password is at least 14 characters long.
    if length < 14:
        return 'Password is to short. Needs to be at least 14 characters'

# creates a password that includes upper-case and lower-case letters, numbers, and special characters.
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k = length))

# iterates over the password to check if it includes at least 1 upper-case letter, lower-case letter, number, and special character.
    has_upper = any(i.upper() for i in password)
    has_lower = any(i.lower() for i in password)
    has_numeric = any(i.isnumeric for i in password)
    has_special = any(i in string.punctuation for i in password)

# determines if the password has at least 1 upper-case letter, lower-case letter, number, and special characters.
# if all conditions are met the user receives a message indicating the password is strong.
# If at least 1 condition isn't met, the user if informed of the missing requirement and asked to fill it via user input.
    if all([has_upper, has_lower, has_numeric, has_special]):
        return password
        print('Strong password')
    elif not has_upper:
        return password + input('Password requires an upper-case letter: ')
    elif not has_lower:
        return password + input('Password requires a lower-case letter: ')
    elif not has_numeric:
        return password + input('Password requires a numeric value: ')
    elif not has_special:
        password + input('Password requires a special character: ')

    return password

def password_manager(host, username, email):

# stores the generated password from the previous function in another variable.
    gen_password = password_generator()

# sets the date and time to the current date and time a user stores a password.
    now = datetime.now().strftime('%Y-%m-%d-%H-%M')

# inserts the generated password alongside the website or app a user is creating an account for, their email address, and the date they created the account.
# the try-except block informs the use whether the data was inserted successfully or not and the type of error that occurs.
    try:
        cursor.execute('insert or ignore into password_database (host, username, email, password, date) values (?, ?, ?, ?, ?);',
                  (host, username, email, gen_password, now)
                  )
        conn.commit()
        print(f'{gen_password} added successfully on {now}')
    except sqlite3.Error as e:
        print(f'database error: {e}')
    except:
        print('data already exists')

# ensures all columns of the table are returned when the script is executed.
pd.set_option('display.max_columns', None)

print(password_generator())
print(password_manager('test_app', 'test_name', 'test@mail.com'))
print(password_generator())
print(password_manager('test_app.2', 'test_name.2', 'test2@mail.com'))
print(password_generator())
print(password_manager('test_app.3', 'test_name.3', 'test3@mail.com'))
print(pd.read_sql_query('select * from password_database;', con = conn))