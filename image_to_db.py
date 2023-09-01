import mysql.connector as msc 
import pandas as pd
from bizcard import *


def main():
    conn = msc.connect( host = 'localhost',
                        user ='root',
                        password ='karthi123',
                        port = '3306',
                        db ='business')  

    if conn:
        print("Database connected successfully")
    try:        
        database = conn.cursor(buffered=True)
        # database.execute('CREATE DATABASE business IF NOT EXIST')
        database.execute('''CREATE TABLE IF NOT EXIST business_card_details
                    (id INT NOT NULL AUTO_INCREMENT,
                    comapny_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(20),
                    email TEXT, 
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pincode VARCHAR(20),
                    image LONGBLOB)''')
        # Prepare the INSERT statement with placeholders for the values
        insert_query1 = """
                    INSERT INTO business_card_details(id,company_name,card_holder,designation,mobile_number,email,website,area,city,state,pincode,image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
        # Iterate over each row in the DataFrame and execute the INSERT statement
        for i, row in df.iterrows():
            values = tuple(row)  # Convert the row to a tuple of values
            database.execute(insert_query1, values)
    except Exception as e:
        print(f"The Error found is {str(e)}")
                    
    conn.commit()
    print("Database Uploaded and disconnected successfully")
    
    
    
    
if __name__ == "__main__":
    main()