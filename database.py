import pyodbc
import json

class Database:
    connection = None
    cursor = None

    @staticmethod
    def connectDB():
        DRIVER_NAME = '{SQL Server}'
        SERVER_NAME = 'MH504623\\SQLEXPRESS'
        DATABASE_NAME = 'GENERATOR_DATA'
        try:
            # Connect to the database
            Database.connection = pyodbc.connect(
                f"DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};"
            )
            print("Database Connection successful!")
        except pyodbc.Error as e:
            print(f"Connection failed: {e}")

        # Create a cursor object with prepared statements enabled
        Database.cursor = Database.connection.cursor()

    @staticmethod
    def createTable(table_name, column_names):
        # Define the query with table and column names
        query = f"CREATE TABLE {table_name} ({','.join(column_names)});"

        try:
            # Execute the query
            Database.cursor.execute(query)
            Database.connection.commit()
            print(f"{table_name} table created")
        except Exception as e:
            print(f"Error: {e}")
                
    @staticmethod
    
    def insert(table_name, fields, values):
        try:
            placeholders = ', '.join('?' for _ in values)
            query = f"INSERT INTO {table_name} ({','.join(fields)}) VALUES ({placeholders})"
            send = Database.placeHolder(placeholders, query, values)
            Database.cursor.execute(send)
            return "Insertion successful!"
        except Exception as e:
            print("Insertion failed. Error message:", e)
            return "Insertion Unsuccessful"

    def placeHolder(place, query, values):
        placeholders = place.split(',')  # Split the placeholder string into individual placeholders
        for placeholder, value in zip(placeholders, values):
            value = "'"+str(value).replace("'", "")+"'"  # Remove single quotes from the value
            query = query.replace(placeholder, value, 1)  # Replace each placeholder with the corresponding value
            values = query.split(',')
        return query

    @staticmethod
    def select():
        # Select data from the table using a prepared statement
        select_query = "SELECT * FROM example WHERE age > ?;"
        age_threshold = 28
        Database.cursor.execute(select_query, (age_threshold,))
        rows = Database.cursor.fetchall()
        for row in rows:
            print(row)
    
    @staticmethod
    def delete():
        # Delete data from the table using a prepared statement
        delete_query = "DELETE FROM example WHERE age < ?;"
        age_threshold = 30
        Database.cursor.execute(delete_query, (age_threshold,))
        Database.connection.commit()
    
    @staticmethod
    def begin_transaction():
        # Begin the transaction
        Database.cursor.execute("BEGIN TRANSACTION")

    @staticmethod
    def commit_transaction():
            # Commit the transaction if everything is successful
            Database.cursor.execute("COMMIT TRANSACTION")
            # Database.cursor.close()

    @staticmethod
    def rollback_transaction():
        try:
            Database.connection.rollback()  # Roll back the transaction
            print("Transaction rolled back successfully.")
        except Exception as e:
            print("Failed to roll back the transaction: {}".format(str(e)))

    
    @staticmethod
    def dropTable(table_name):
        #Nuke a table. 
        for table_name in table_name:
            Database.cursor.execute(f"DROP TABLE {table_name}")
        Database.connection.commit()

    @staticmethod
    def endDB():
        # Close the cursor and connection
        Database.cursor.close()
        Database.connection.close()

    @staticmethod
    def fillTables(data):
        try:
            #We need to update Entry_Type, Roles, Location, MODEL_EXAMPLE, PSSE_MODELS
            Roles = ["Super User","Admin","User"]
            for role in Roles:
                Database.insert("Role",["Role_Name"],[role])
            Entry_Type = ["Preliminary","Interconnection Request","AS-Built","NERC"]
            for entry in Entry_Type:
                Database.insert("Entry_Type",["Type_Name"],[entry])
            for models in list(data['Model'].keys()):
                sql = f"INSERT INTO PSSE_MODELS (Model_name) OUTPUT inserted.PSSE_MODEL_ID VALUES ('{models}')"
                Database.cursor.execute(sql)
                generated_id = Database.cursor.fetchone()[0]
                for model_example in list(data['Model'][models].keys()):
                    Database.insert("MODEL_EXAMPLE",["PSSE_MODEL_ID","Model_Example_Name"],[generated_id,model_example])
            
            for location in data['Location']:
                Database.insert("Location",["GS_Loc"],[location])

        except pyodbc.Error as e:
            # Handle any errors that occur during the execution
            print("Error executing SQL statement:", e)
        finally:
            Database.connection.commit()

    @staticmethod
    def createTables():
        tables_to_drop = ["Two_Wind_Transformer","Machine_PowerFlow_Data","Entries_relate_bus","Access","Login","Bus","Role","CON_ICON","Table_Entries","MODEL_EXAMPLE","PSSE_MODELS","Notes","Entries","Version","Entry_Type","Location"]
        # Drop existing tables
        Database.dropTable(tables_to_drop)

        Database.createTable("Location",[
            "GS_ID INT IDENTITY(1,1) PRIMARY KEY",
            "GS_Loc TEXT NOT NULL"
        ])

        Database.createTable("Entry_Type",[
            "Type_ID INT IDENTITY(1,1) PRIMARY KEY",
            "Type_Name TEXT NOT NULL"
        ])

        Database.createTable("Version",[
            "Version_ID INT IDENTITY(1,1) PRIMARY KEY",
            "Version_History DATE NOT NULL UNIQUE"
        ])

        Database.createTable("Entries", [
            "Entries_ID INT IDENTITY(1,1) PRIMARY KEY",
            "GS_ID INT NOT NULL",
            "Type_ID INT NOT NULL",
            "Generator_Owner VARCHAR(255) NOT NULL ",
            "Consultant VARCHAR(255) NOT NULL ",
            "Date DATE NOT NULL",
            "Revision_Date DATE NOT NULL",
            "Initials VARCHAR(5) NOT NULL",
            "Effective_Date DATE NOT NULL",
            "Legend_Image TEXT",
            "Report_Image TEXT",
            "APPROVED BIT NOT NULL",
            "Version_ID INT NOT NULL",
            "FOREIGN KEY (GS_ID) REFERENCES Location (GS_ID)",
            "FOREIGN KEY (Type_ID) REFERENCES Entry_Type (Type_ID)",
            "FOREIGN KEY (Version_ID) REFERENCES Version(Version_ID)"
        ])

        Database.createTable("Notes",[
            "Note_ID INT IDENTITY(1,1) PRIMARY KEY",
            "Note_Type VARCHAR(255)",
            "Note_Val TEXT NOT NULL",
            "Entries_ID INT NOT NULL",
            "FOREIGN KEY (Entries_ID) REFERENCES Entries(Entries_ID)",

        ])

        Database.createTable("PSSE_MODELS",[
            "PSSE_MODEL_ID INT IDENTITY(1,1) PRIMARY KEY",
            "Model_Name TEXT NOT NULL"
        ])

        Database.createTable("MODEL_EXAMPLE",[
            "Example_ID INT IDENTITY(1,1) PRIMARY KEY",
            "PSSE_MODEL_ID INT NOT NULL",
            "Model_Example_Name TEXT NOT NULL",
            "FOREIGN KEY (PSSE_MODEL_ID) REFERENCES PSSE_MODELS(PSSE_MODEL_ID)"
        ])

        Database.createTable("Table_Entries",[
            "Table_Entries_ID INT IDENTITY(1,1) PRIMARY KEY",
            "Example_ID INT NOT NULL",
            "Image_Location TEXT",
            "Entries_ID INT NOT NULL",
            "FOREIGN KEY (Entries_ID) REFERENCES Entries(Entries_ID)",
            "FOREIGN KEY (Example_ID) REFERENCES MODEL_EXAMPLE(Example_ID)"
        ])


        Database.createTable("CON_ICON",[
            "CON_ICON_Key INT IDENTITY(1,1) PRIMARY KEY",
            "Tables_Entries_ID INT NOT NULL",
            "CON_ICON_Name TEXT NOT NULL",
            "CON_ICON_Value NUMERIC(38,0) NOT NULL",
            "CON_ICON_Type_Key INT NOT NULL CHECK (CON_ICON_Type_Key IN (1, 2))",
            "FOREIGN KEY (Tables_Entries_ID ) REFERENCES Table_Entries(Table_Entries_ID)"
        ])

        Database.createTable("Role",[
            "Role_ID INT IDENTITY(1,1) PRIMARY KEY",
            "Role_Name VARCHAR(20)"
        ])

        Database.createTable("Bus",[
            "Bus_Key INT IDENTITY(1,1) PRIMARY KEY",
            "Bus_Number INT NOT NULL",
            "Bus_ID INT NOT NULL"
        ])

        Database.createTable("Login",[
            "Login_ID INT IDENTITY(1,1) PRIMARY KEY",
            "UserName VARCHAR(255) NOT NULL UNIQUE",
            "Password VARCHAR(255) NOT NULL",
            "Role INT NOT NULL",
            "FOREIGN KEY (Role) REFERENCES Role(Role_ID)"
        ])

        Database.createTable("Access",[
            "Entries_ID INT NOT NULL",
            "Login_ID INT NOT NULL",
            "FOREIGN KEY (Entries_ID) REFERENCES Entries(Entries_ID)",
            "FOREIGN KEY (Login_ID) REFERENCES Login(Login_ID)"
        ])


        Database.createTable("Entries_relate_bus",[
            "Entries_ID INT NOT NULL",
            "Bus_Key INT NOT NULL",
            "FOREIGN KEY (Entries_ID) REFERENCES Table_Entries(Table_Entries_ID)",
            "FOREIGN KEY (Bus_Key) REFERENCES Bus(Bus_Key)"
        ])


        Database.createTable("Machine_PowerFlow_Data", [
            "M_ID INT IDENTITY(1,1) PRIMARY KEY",
            "Entries_ID INT NOT NULL",
            "Bus_Num INT NOT NULL",
            "Nominal_Voltage VARCHAR(30) NOT NULL",
            "Scheduled_Voltage VARCHAR(30) NOT NULL",
            "Remote_Bus INT NOT NULL",
            "Pmax VARCHAR(30) NOT NULL",
            "Pmin VARCHAR(30) NOT NULL",
            "Qmax VARCHAR(30) NOT NULL",
            "Qmin VARCHAR(30) NOT NULL",
            "Mbase VARCHAR(30) NOT NULL",
            "Impedance_R VARCHAR(30) NOT NULL",
            "Impedance_X VARCHAR(30) NOT NULL",
            "Wind_Machine_Control INT NOT NULL",
            "Wind_Power_Control INT NOT NULL",
            "FOREIGN KEY (Entries_ID) REFERENCES Entries(Entries_ID)"

        ])

        Database.createTable("Two_Wind_Transformer",[
            "Two_ID INT IDENTITY(1,1) PRIMARY KEY",
            "Entries_ID INT NOT NULL",           
            "From_Bus_Num INT NOT NULL",
            "Bus_Num INT NOT NULL",
            "Name_Val TEXT NOT NULL",
            "Metered_Bus VARCHAR(30) NOT NULL",
            "Wind_Side VARCHAR(30) NOT NULL",
            "Controlled_BUS VARCHAR(30) NOT NULL",
            "Wind_1_Num_Pos VARCHAR(30) NOT NULL",
            "Wind_1_Cont_Mode VARCHAR(30) NOT NULL",
            "Wind_1_Auto VARCHAR(30) NOT NULL",
            "Wind_1_Control_Vmax VARCHAR(30) NOT NULL",
            "Wind_1_Control_Vmin VARCHAR(30) NOT NULL",
            "Wind_1_Tap_Vmax VARCHAR(30) NOT NULL",
            "Wind_1_Tap_Vmin VARCHAR(30) NOT NULL",
            "Imp_R VARCHAR(30) NOT NULL",
            "Imp_X VARCHAR(30) NOT NULL",
            "MVA_A VARCHAR(30) NOT NULL",
            "MVA_B VARCHAR(30) NOT NULL",
            "MVA_C VARCHAR(30) NOT NULL",
            "Mag_G VARCHAR(30) NOT NULL",
            "Mag_B VARCHAR(30) NOT NULL",
            "Wind_MVA_Base VARCHAR(30) NOT NULL",
            "Wind_Angle_Degree VARCHAR(30) NOT NULL",
            "Wind_1_Nominal VARCHAR(30) NOT NULL",
            "Wind_1_Tap VARCHAR(30) NOT NULL",
            "Wind_2_Nominal VARCHAR(30) NOT NULL",
            "Wind_2_Tap VARCHAR(30) NOT NULL",
            "Wind_Connect_Angle VARCHAR(30) NOT NULL",
            "Load_R VARCHAR(30) NOT NULL",
            "Load_X VARCHAR(30) NOT NULL",
            "Imp_Corr_Table VARCHAR(30) NOT NULL",
            "FOREIGN KEY (Entries_ID) REFERENCES Entries(Entries_ID)"


        ])



