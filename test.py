# import random
# from datetime import datetime, timedelta
# from database import Database  # Assuming you have a Database module

# # Create an instance of the Database class
# db = Database()
# db.connectDB()


# {'role': 1, 'LoginID': 1, 'access': ['Interconnection Request', 'AS-Built'], 'location': 'Brandon', 'busNumbers': ['6534354', '65757'], 'machine_seq_table': [['6534354', '1', '62.3', '-43', '0.23', '0.0', '1', '2.4', '2', '3.5', '3.1', '1.2', '3', '3']], 'two_winding_table': [['609012', '6534354', '1', '5', '5.3', '2', '-1.1', '0.3', '1.2', '0.001', '2', '3.54', '2', '4.3', '2.2', '1', '1', '2.3', '3', '3', '2', '32', '23', '2', '23', '23', '23', '234', '23', '2', '3']], 'Model': {'Generator Models': {'GENSAL': {'Figure': {'bus': [{'bus': '6534354', 'id': '1'}], 'con': [{'col1': 'j', 'col2': 'D-Axis Opened Circuit Transient Time Constant', 'col3': "T'do (> 0)", 'col4': '4'}, {'col1': 'j+1', 'col2': 'D-Axis Opened Circuit Sub-transient Time Constant', 'col3': "T''do (> 0)", 'col4': '4'}, {'col1': 'j+2', 'col2': 'Q-Axis Opened Circuit Transient Time Constant', 'col3': "T'qo (> 0)", 'col4': '3'}, {'col1': 'j+3', 'col2': 'Inertia', 'col3': 'H', 'col4': '4'}, {'col1': 'j+4', 'col2': 'Speed Damping', 'col3': 'D', 'col4': '3'}, {'col1': 'j+5', 'col2': 'D-Axis Synchronous Reactance', 'col3': 'Xd', 'col4': '34'}, {'col1': 'j+6', 'col2': 'Q-Axis Synchronous Reactance', 'col3': 'Xq', 'col4': '4'}, {'col1': 'j+7', 'col2': 'D-Axis Transient Reactance', 'col3': "X'd", 'col4': '34'}, {'col1': 'j+8', 'col2': 'D/Q-Axis Sub-transient Reactance', 'col3': "X''d = X''q", 'col4': '34'}, {'col1': 'j+9', 'col2': 'Leakage Reactance', 'col3': 'Xl', 'col4': '34'}, {'col1': 'j+10', 'col2': 'Open Circuit Saturation Factor', 'col3': 'S(1.0)', 'col4': '34'}, {'col1': 'j+111', 'col2': 'Open Circuit Saturation Factor', 'col3': 'S(1.2)', 'col4': '34'}], 'image': ''}}}}, 'Entry_Type': 'Choose Report Type'}
# sendToDb = {}

# sendToDb['role'] = random.randint(1, 3)
# sendToDb['LoginID'] = random.randint(1, 3)
# if(sendToDb['role'] == 1):
#     sendToDb['access'] = ['Interconnection Request', 'AS-Built']
# elif(sendToDb['role'] == 2):
#     sendToDb['access'] = ["Preliminary"]
# elif(sendToDb['role'] == 3):
#     sendToDb['access'] = ["User"]
# sendToDb['busNumbers']=  [random.randint(60000, 70000) for _ in range(random.randint(1, 3))]

# print(sendToDb)


# # # Generate random role names, entry types, locations, and model names
# # roles = ['Super User', 'Admin', 'User']
# # entry_types = ['Type A', 'Type B', 'Type C']
# # locations = ['Location 1', 'Location 2', 'Location 3']
# # model_names = ['Model A', 'Model B', 'Model C']

# # # Generate random dates for versions
# # start_date = datetime(2021, 1, 1)
# # end_date = datetime(2022, 12, 31)
# # date_range = end_date - start_date

# # # Generate random bus numbers and IDs
# # bus_numbers = list(range(1, 1001))
# # bus_ids = list(range(1001, 2001))

# # # Generate random model example names, image locations, usernames, and passwords
# # example_names = ['Example 1', 'Example 2', 'Example 3']
# # image_locations = ['path/to/image1', 'path/to/image2', 'path/to/image3']
# # usernames = ['user1', 'user2', 'user3']
# # passwords = ['password1', 'password2', 'password3']

# # # Generate random CON_ICON names, values, and type keys
# # con_icon_names = ['CON_ICON 1', 'CON_ICON 2', 'CON_ICON 3']
# # con_icon_values = [100, 200, 300]
# # con_icon_type_keys = [1, 2]

# # # Begin transaction
# # db.cursor.execute("BEGIN TRANSACTION")

# # try:
# #     # Insert random data into each table
# #     for _ in range(1000):
# #         # Insert into Version table
# #         version_history = start_date + timedelta(days=random.randint(0, date_range.days))
# #         db.cursor.execute(f"INSERT INTO Version (Version_History) VALUES ('{version_history}')")

# #         # Insert into Bus table
# #         bus_number = random.choice(bus_numbers)
# #         bus_id = random.choice(bus_ids)
# #         db.cursor.execute(f"INSERT INTO Bus (Bus_Number, Bus_ID) VALUES ({bus_number}, {bus_id})")

# #         # Insert into Entries table
# #         example_id = random.randint(1, 348)
# #         version_id = random.randint(1, 348)
# #         image_location = random.choice(image_locations)
# #         type_id = random.randint(1, 1000)
# #         gs_id = random.randint(1, 1000)
# #         approved = random.choice([1, 0])
# #         db.cursor.execute(f"INSERT INTO Entries (Example_ID, Version_ID, Image_Location, Type_ID, GS_ID, APPROVED) "
# #                           f"VALUES ({example_id}, {version_id}, '{image_location}', {type_id}, {gs_id}, {approved})")

# #         # Insert into Login table
# #         username = random.choice(usernames)
# #         password = random.choice(passwords)
# #         role = random.randint(1, 20)
# #         db.cursor.execute(f"INSERT INTO Login (UserName, Password, Role) "
# #                           f"VALUES ('{username}', '{password}', {role})")

# #         # Insert into Access table
# #         entries_id = db.cursor.lastrowid
# #         login_id = db.cursor.lastrowid
# #         db.cursor.execute(f"INSERT INTO Access (Entries_ID, Login_ID) VALUES ({entries_id}, {login_id})")

# #         # Insert into CON_ICON table
# #         entries_id = db.cursor.lastrowid
# #         con_icon_name = random.choice(con_icon_names)
# #         con_icon_value = random.choice(con_icon_values)
# #         con_icon_type_key = random.choice(con_icon_type_keys)
# #         db.cursor.execute(f"INSERT INTO CON_ICON (Entries_ID, CON_ICON_Name, CON_ICON_Value, CON_ICON_Type_Key) "
# #                           f"VALUES ({entries_id}, '{con_icon_name}', {con_icon_value}, {con_icon_type_key})")

# #         # Insert into Entries_relate_bus table
# #         entries_id = db.cursor.lastrowid
# #         bus_key = random.randint(1, 1000)
# #         db.cursor.execute(f"INSERT INTO Entries_relate_bus (Entries_ID, Bus_Key) VALUES ({entries_id}, {bus_key})")

# #     # Commit the transaction
# #     db.cursor.execute("COMMIT")
# # except:
# #     # Rollback the transaction if an error occurs
# #     db.cursor.execute("ROLLBACK")
# #     raise

# # # Close the database connection
# # db.disconnectDB()






# import json

# entry_num_var = [
#     (4547, 2, 3, 'Manitoba Hydro Generation & Wholesale Business Unit', 'System Performance', '2019-06-03', '2024-03-31', 'T.A', '2019-06-03', 'http://localhost:3000/uploads/legend.png', 'http://localhost:3000/uploads/I9vWQ4evFG8YrCT.jpg', True, 1),
#     (4751, 2, 3, 'Manitoba Hydro Generation & Wholesale Business Unit', 'Grid Optimization', '2019-06-03', '2023-11-30', 'T.A', '2019-06-03', 'http://localhost:3000/uploads/legend.png', 'http://localhost:3000/uploads/I9vWQ4evFG8YrCT.jpg', True, 1)
# ]

# # Convert the list of tuples to a list of dictionaries
# keys = ['Generator_Owner', 'Consultant', 'Date', 'Revision', 'Initials', 'Effective_Date']

# def arrJson(keys,entry_num_var):
#     dictio = {}
#     for entry in entry_num_var:
#         for i,key in enumerate(keys):
#             dictio[key] = entry[3+i]
#     return dictio



# print(arrJson(keys,entry_num_var))

import random
import string

num_rows = 10
num = 14

for _ in range(num_rows):
    row = [str(random.randint(100000, 999999))] + [str(random.randint(1, 10))] + [str(round(random.uniform(-5, 10), random.randint(1, 5)))] + [str(round(random.uniform(-5, 10), random.randint(1, 5)))] + [str(random.randint(100000, 999999))] + [str(round(random.uniform(-5, 10), random.randint(1, 5))) for _ in range(num-7)] + [str(random.randint(1, 3))] + [str(random.randint(1, 3))]
    print(row)
num = 31
for _ in range(num_rows):
    row = [str(random.randint(100000, 999999))] + [str(random.randint(100000, 999999))] + [random.randint(1, 10)] + [random.choice(string.ascii_uppercase) + str(random.randint(1, 10))] + [round(random.uniform(-5, 10), random.randint(1, 5)) for _ in range(num-4)]
    print(row)
