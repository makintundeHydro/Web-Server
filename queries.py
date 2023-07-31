class queries:
    def __init__(self):
        pass

    def add_item(key_path, value,sendToDb):
        current_dict = sendToDb
        for key in key_path[:-1]:
            if key not in current_dict:
                current_dict[key] = {}
                
            current_dict = current_dict[key]
        current_dict[key_path[-1]] = value

    def fetch_con_icons_list(model_example, converter, con_results,data):
        con_list = []
        for row in con_results:
            col2_value = [sub[1] for sub in data['Model'][model_example[0]][model_example[1]]['prop']['con'] if sub[0] == row[0]]
            col2 = col2_value[0] if col2_value else "N/A"
            col3_value = [sub[2] for sub in data['Model'][model_example[0]][model_example[1]]['prop']['con'] if sub[0] == row[0]]
            col3 = col3_value[0] if col3_value else "N/A"
            con_data = {
                "col1": row[0],
                "col2" : col2,
                "col3": col3,
                "col4": str(converter.int_bits_to_float(int(row[1])))
            }
            con_list.append(con_data)
        return con_list

    def getEntriesID(myDb,location, entryType, versionID):
        # Get the Entries_ID for the report entry
        query = "SELECT * FROM Entries WHERE GS_ID = ? AND Type_ID = ? AND Version_ID = ?"
        myDb.cursor.execute(query, (location, entryType, versionID))
        return myDb.cursor.fetchall()
    
    def getEntriesIDOne(myDb, location, entryType, versionID, Consultant, Date, genOwner, Inititials):
        # Get the Entries_ID for the report entry
        query = "SELECT * FROM Entries WHERE GS_ID = ? AND Type_ID = ? AND Version_ID = ? AND Generator_Owner = ? AND Consultant = ? AND Effective_Date = ? AND Initials = ? "
        myDb.cursor.execute(query, (location, entryType, versionID, genOwner,Consultant,Date, Inititials))
        return myDb.cursor.fetchone()
    
    def getTableEntriesID(myDb,entry_num_variable):
        # Find the Table_Entries_ID in Table_Entries table for the entry above. 
        query = "SELECT Table_Entries_ID,Example_ID,Image_Location FROM Table_Entries WHERE Entries_ID = ?"
        myDb.cursor.execute(query, entry_num_variable)
        return myDb.cursor.fetchall()
    
    def getModelExample(myDb,example_variable):
        myDb.cursor.execute(f"""
                    SELECT Model_Name,Model_Example_Name
                    FROM PSSE_MODELS
                    JOIN MODEL_EXAMPLE
                    ON PSSE_MODELS.PSSE_MODEL_ID = MODEL_EXAMPLE.PSSE_MODEL_ID
                    WHERE Example_ID = {example_variable}
                    """)
        return myDb.cursor.fetchone()

    def getBusResult(myDb,table_variable): 
        myDb.cursor.execute(f"""
                                SELECT BUS.Bus_Number,BUS.Bus_ID
                                FROM Entries_relate_bus
                                JOIN BUS
                                ON BUS.Bus_Key = Entries_relate_bus.Bus_Key
                                WHERE Entries_relate_bus.Entries_ID = {table_variable}
                                """)
        return myDb.cursor.fetchall()   

    def fetch_con_icons(myDb,table_variable, con_icon_type_key):
        myDb.cursor.execute(f"SELECT CON_ICON_Name,CON_ICON_Value,CON_ICON_Type_Key FROM CON_ICON WHERE Tables_Entries_ID = {table_variable} AND CON_ICON_Type_Key = {con_icon_type_key}")
        return myDb.cursor.fetchall()
    
    def merger_con_icon(converter, con_icon_results):
        iconPrint = ""
        if(len(con_icon_results)> 0):
            iconPrint = ", ".join(
                str(converter.int_bits_to_float(int(data[1])))
                for data in con_icon_results
            )
        return iconPrint

    def getAllMachine(myDb,entry_num_variable):
        query = "SELECT * FROM Machine_PowerFlow_Data WHERE Entries_ID = ?"
        myDb.cursor.execute(query, entry_num_variable)
        return myDb.cursor.fetchall()
    
    def getAllTwoWind(myDb,entry_num_variable):
        query = "SELECT * FROM Two_Wind_Transformer WHERE Entries_ID = ?"
        myDb.cursor.execute(query, entry_num_variable)
        return myDb.cursor.fetchall()

    def getBusDetails(myDb,bus_num):
        query = "SELECT Bus_Number, Bus_ID FROM Bus WHERE Bus_Key = ?"
        myDb.cursor.execute(query, bus_num)
        return myDb.cursor.fetchone()
    
    def delete(myDb,table, parameter, value):
        query = f"DELETE FROM {table} WHERE {parameter} = ?"
        myDb.cursor.execute(query, (value,))

    @staticmethod
    def getVersionID(myDb,date):
        query = f"SELECT Version_ID FROM Version WHERE Version_History = '{date}'"
        myDb.cursor.execute(query)
        versionID = myDb.cursor.fetchone()

        if versionID is None:
            query = f"INSERT INTO Version (Version_History) OUTPUT INSERTED.Version_ID VALUES ('{date}')"
            myDb.cursor.execute(query)
            versionID = myDb.cursor.fetchone()[0]
            myDb.connection.commit()
        else:
            versionID = versionID[0]
        
        return versionID


    @staticmethod
    def insertBusKey(myDb,bus, id):
        query = f"SELECT Bus_Key FROM BUS WHERE Bus_Number = '{bus}' AND Bus_ID = '{id}'"
        myDb.cursor.execute(query)
        bus_id = myDb.cursor.fetchone()

        if bus_id is None:
            query = f"INSERT INTO BUS (Bus_Number,Bus_ID) OUTPUT INSERTED.Bus_Key VALUES ('{bus}','{id}')"
            myDb.cursor.execute(query)
            bus_id = myDb.cursor.fetchone()[0]
            myDb.connection.commit()
        else:
            bus_id = bus_id[0]
        return bus_id
    
     #GS_ID,Example ID,Version_ID,Image_Location,Approved,Entry_Type
    @staticmethod
    def insertEntriesData(myDb,example_id,image,entry):
        query = f"""INSERT INTO Table_Entries (Example_ID,Image_Location,Entries_ID) OUTPUT INSERTED.Table_Entries_ID VALUES ({example_id},'{image}',{entry})"""
        myDb.cursor.execute(query)
        entries = myDb.cursor.fetchone()[0]
        return entries

    @staticmethod
    def CON_ICON_Entry(myDb,entryTable_id,con_icon_name,con_icon_value,con_icon_type):
        query = f"INSERT INTO CON_ICON (Tables_Entries_ID,CON_ICON_Name,CON_ICON_Value,CON_ICON_Type_Key) VALUES ({entryTable_id},'{con_icon_name}',{con_icon_value},{con_icon_type})"
        myDb.cursor.execute(query)


    @staticmethod
    def entry_to_bus(myDb,entries,bus_key):
        query = f"INSERT INTO Entries_relate_bus (Entries_ID, Bus_Key) VALUES ({entries},{bus_key})"
        myDb.cursor.execute(query)
        myDb.connection.commit()

    @staticmethod
    def find_station(myDb,station):
        query = f"SELECT GS_ID FROM Location WHERE GS_Loc LIKE '{station}'"
        myDb.cursor.execute(query)
        return myDb.cursor.fetchone()[0]

    @staticmethod
    def fill_located_table(myDb,entry,location):
        query = f"INSERT INTO Located (GS_ID_Location,GS_ID_Entries) VALUES {location,entry}"
        myDb.cursor.execute(query)
        myDb.connection.commit()


    @staticmethod
    def loginaccessentry(myDb,entry,loginID):
        query = f"INSERT INTO Access (Entries_ID,Login_ID) VALUES ({entry},{loginID})"
        myDb.cursor.execute(query)
        myDb.connection.commit()

    def login_id(myDb,username, password):
        myDb.cursor.execute(f"SELECT * FROM Login WHERE UserName = '{username}'")
        id = myDb.cursor.fetchone()
        if id is not None:
            return id
        return [0]
    
    def getDates(myDb, location, report_type):
        query = f"""
            SELECT Version_History
            FROM Location
            JOIN Entries ON Location.GS_ID = Entries.GS_ID
            JOIN Version ON Entries.Version_ID = Version.Version_ID
            JOIN Entry_Type ON Entry_Type.Type_ID = Entries.Type_ID
            WHERE Location.GS_Loc LIKE '{location}'
            AND Entry_Type.Type_Name LIKE '{report_type}'
        """
        myDb.cursor.execute(query)
        results = myDb.cursor.fetchall()
        dates = set(row[0] for row in results)  # Using set comprehension to extract unique dates
        unique_dates = list(dates)
        return unique_dates
    
    def getExampleID(myDb,model, example):
        query = f"SELECT Example_ID FROM MODEL_EXAMPLE WHERE PSSE_MODEL_ID = '{model}' AND Model_Example_Name LIKE '{example}'"
        myDb.cursor.execute(query)
        data = myDb.cursor.fetchone()[0]
        return data
    
    def getModels(myDb,model):
        query = f"SELECT PSSE_MODEL_ID FROM PSSE_MODELS WHERE Model_Name LIKE '{model}'"
        myDb.cursor.execute(query)
        data = myDb.cursor.fetchone()[0]
        return data

    def get_user_role(myDb,username):
        myDb.cursor.execute(f"SELECT Role FROM Login WHERE UserName LIKE '{username}'")
        return myDb.cursor.fetchone()[0]
    

    def getEntryType(myDb,entry):
        myDb.cursor.execute(f"SELECT Type_ID FROM Entry_Type WHERE Type_Name LIKE '{entry}'")
        return myDb.cursor.fetchone()[0]
    
    def getLocation(myDb,location):
        myDb.cursor.execute(f"SELECT GS_ID FROM Location WHERE GS_Loc LIKE '{location}'")
        return myDb.cursor.fetchone()[0]
    
    def getLocationName(myDb,location):
        myDb.cursor.execute(f"SELECT GS_Loc FROM Location WHERE GS_ID LIKE '{location}'")
        return myDb.cursor.fetchone()[0]

    def addEntry(myDb,version_id,entry_type,approved,aboutReport,reportContainer):
        query = f"""INSERT INTO Entries (GS_ID, Type_ID, Generator_Owner, Consultant, Date, Revision_Date, Initials, Effective_Date, Legend_Image, Report_Image, Approved, Version_ID) OUTPUT INSERTED.Entries_ID VALUES   {queries.getLocation(myDb,aboutReport['location']),entry_type,aboutReport['generator_owner'],aboutReport['consultant'],aboutReport['effective_date'],aboutReport['revision_date'],
                            aboutReport['initials'],aboutReport['effective_date'],reportContainer['legendImage'],reportContainer['reportImage'], approved, version_id}"""
        myDb.cursor.execute(query)
        return myDb.cursor.fetchone()[0]
    
    def addNotes(myDb, notes, entry_num):
        for note_type, note_val in notes.items():
            # Correct the replacement pattern to use four backslashes for each backslash in the original string
            note_val_replaced = note_val.replace(r'\\n', '\n')
            sql = "INSERT INTO Notes (Note_Val, Note_Type, Entries_ID) VALUES (?, ?, ?)"
            myDb.cursor.execute(sql, (note_val_replaced, note_type, entry_num))
            

    def addMacseq(myDb, converter, entries_id, values):
        for row in values:
            converted_values = [str(converter.float_to_int_bits(float(value))) for value in row[5:12]]
            query = f"""INSERT INTO Machine_PowerFlow_Data (Entries_ID, Bus_Num,  Nominal_Voltage, Scheduled_Voltage, Remote_Bus, Pmax, Pmin,
              Qmax, Qmin,  Mbase, Impedance_R, Impedance_X, Wind_Machine_Control, Wind_Power_Control)
                        VALUES ({entries_id}, {queries.insertBusKey(myDb, row[0], row[1])}, {str(converter.float_to_int_bits(float(row[2])))}, {str(converter.float_to_int_bits(float(row[3])))}, {row[4]},{','.join(converted_values)} ,{row[12]} ,{row[13]})"""
            myDb.cursor.execute(query)

    def addTwoWind(myDb, converter, entries_id, values):
        for row in values:
            converted_values = [str(converter.float_to_int_bits(float(value))) for value in row[4:]]
            query = f"""INSERT INTO Two_Wind_Transformer (Entries_ID, From_Bus_Num, Bus_Num, Name_Val, Metered_Bus, Wind_Side, Controlled_BUS, Wind_1_Num_Pos, Wind_1_Cont_Mode, Wind_1_Auto, Wind_1_Control_Vmax, Wind_1_Control_Vmin, Wind_1_Tap_Vmax, Wind_1_Tap_Vmin, Imp_R, Imp_X, MVA_A, MVA_B, MVA_C, Mag_G, Mag_B, Wind_MVA_Base, Wind_Angle_Degree, Wind_1_Nominal, Wind_1_Tap, Wind_2_Nominal, Wind_2_Tap, Wind_Connect_Angle, Load_R, Load_X, Imp_Corr_Table)
                        VALUES ({entries_id}, {row[0]}, {queries.insertBusKey(myDb, row[1], row[2])}, '{row[3]}', {','.join(converted_values)})"""
            myDb.cursor.execute(query)

    def addTableEntry(myDb,entry_num,data,converter,model_data):
        for models in list(model_data):
            for examples in list(model_data[models]): 
                example_id = queries.getExampleID(myDb,queries.getModels(myDb,models), examples)
                for fig in list(model_data[models][examples]):
                    for rows in list(model_data[models][examples][fig]):
                        if rows == "bus":
                            entries = queries.insertEntriesData(myDb,example_id,model_data[models][examples][fig]['image'],entry_num) 
                            for bus_info in model_data[models][examples][fig]['bus']:
                                bus_key = queries.insertBusKey(myDb,bus_info['bus'], bus_info['id'])
                                queries.entry_to_bus(myDb,entries,bus_key)
                        else:
                                if rows == "con": 
                                    if len(model_data[models][examples][fig]['con']) == data["Model"][models][examples]['con_number']:
                                        for con in model_data[models][examples][fig]['con']:
                                            val = 0
                                            if con['col4'] != 0:
                                                val = converter.float_to_int_bits(float(con['col4']))
                                            queries.CON_ICON_Entry(myDb,entries,con['col1'],val,1)
                                    else:
                                        print("The amount con for this model is not equal")
                                elif rows == "icon":
                                    if len(model_data[models][examples][fig]['con']) == data["Model"][models][examples]['icon_number']:
                                        for icon in model_data[models][examples][fig]['icon']:
                                            val = converter.float_to_int_bits(float(icon['col4']))
                                            queries.CON_ICON_Entry(myDb,entries,icon['col1'],val,2)
                                    else:
                                        print("The amount con for this model is not equal")
    
    
    def getDetailEntriesID(myDb, location, entryType, versionID, selected_entry_id):
        # Get the Entries_ID for the report entry in detail
        query = "SELECT * FROM Entries WHERE GS_ID = ? AND Type_ID = ? AND Version_ID = ? AND ID = ?"
        myDb.cursor.execute(query, (location, entryType, versionID, selected_entry_id))
        return myDb.cursor.fetchone()

    def getDetailEntriesID(myDb, location, entryType, versionID,selected_entry_id):
        # Get the Entries_ID for the report entry in detail
        query = "SELECT * FROM Entries WHERE GS_ID = ? AND Type_ID = ? AND Version_ID = ? AND ID = ?"
        myDb.cursor.execute(query, (location, entryType, versionID, selected_entry_id))
        return myDb.cursor.fetchone()

    

    def generate_dyr(myDb,converter,data,entry_num_variable):
        file_path = "output.txt"
        with open(file_path, "w") as file:
            try:
                table_variables = queries.getTableEntriesID(myDb,entry_num_variable[0])

                #For each dynamic table in the report
                for table_variable_val in table_variables:
                    if table_variable_val:
                        table_variable = table_variable_val[0]  # Extract the Table_Entries_ID from the result
                        example_variable = table_variable_val[1]

                        model_example = queries.getModelExample(myDb,example_variable)
                        bus_results = queries.getBusResult(myDb,table_variable)

                        fetch_con = queries.fetch_con_icons(myDb,table_variable, 1)
                        fetch_icon = queries.fetch_con_icons(myDb,table_variable, 2)

                        conPrint = queries.merger_con_icon(converter, fetch_con)
                        iconPrint = queries.merger_con_icon(converter, fetch_icon)                    

                        placeholder = data['Model'][model_example[0]][model_example[1]]['PlaceHolder']
                        for result in bus_results:
                            line = (str(result[0]) + ","+ placeholder.replace("ID",str(result[1])) + iconPrint + conPrint) + "/"+ "\n"
                            file.write(line)
                    else:
                        print("Table_Entries entry not found.")
                return file_path
            except Exception as e:
                # Rollback the transaction if an error occurs
                myDb.cursor.rollback()
                print("An error occurred:", str(e))

    def delete_Report(myDb, entry_num_variable):

        if entry_num_variable:
            entry_num_variable = entry_num_variable[0]  # Extract the Entries_ID from the result

            try:
                # Start a database transaction
                myDb.autocommit = False

                # Delete entry in Two Wind Transformer table
                queries.delete(myDb,"Two_Wind_Transformer", "Entries_ID", entry_num_variable)

                # Delete entry in Machine Power Flow Data table
                queries.delete(myDb,"Machine_PowerFlow_Data", "Entries_ID", entry_num_variable)

                # Delete entry in Notes
                queries.delete(myDb,"Notes", "Entries_ID", entry_num_variable)

                # Delete entry in Access
                queries.delete(myDb,"Access", "Entries_ID", entry_num_variable)

                # Find the Table_Entries_ID in Table_Entries table
                table_variables = queries.getTableEntriesID(myDb,entry_num_variable)

                for table_variable in table_variables:
                    if table_variable:
                        table_variable = table_variable[0]  # Extract the Table_Entries_ID from the result

                        # Delete all entries in CON_ICON table where Table_Entries_ID = Table_Variable
                        queries.delete(myDb,"CON_ICON","Tables_Entries_ID",table_variable)

                        #Delete the relations with Bus and Bus ID 
                        queries.delete(myDb,"Entries_relate_bus","Entries_ID",table_variable)
                    
                    else:
                        print("Table_Entries entry not found.")

                # Delete entry in Table_Entries table
                queries.delete(myDb,"Table_Entries","Entries_ID",entry_num_variable)

                # Delete entry
                queries.delete(myDb,"Entries","Entries_ID",entry_num_variable)

                # Commit the transaction if all queries are successful
                myDb.cursor.commit()
                myDb.autocommit = True
                return True

            except Exception as e:
                # Rollback the transaction if an error occurs
                myDb.cursor.rollback()
                print("An error occurred:", str(e))
                return False

                
        else:
            print("Report entry not found.")





    def generate_report(myDb,location,converter,data,entry_num_var):
        report_dict = {}


        if entry_num_var:
            entry_num_variable = entry_num_var[0]  # Extract the Entries_ID from the result

            try:
                about_report = {
                    "location": queries.getLocationName(myDb,location),
                    "generator_owner" : entry_num_var[3],
                    "consultant" : entry_num_var[4],
                    "initials" : entry_num_var[7],
                    "revision_date" : entry_num_var[6],
                    "effective_date" : entry_num_var[8]
                }
                
                # Delete entry in Notes
                query = "SELECT Note_Type,Note_Val FROM Notes WHERE Entries_ID = ?"
                myDb.cursor.execute(query, entry_num_variable)
                notes_array = myDb.cursor.fetchall()
                # Convert the notes_array into the desired dictionary format
                notes_dict = {}
                for row in notes_array:
                    note_type = row[0]
                    note_val = row[1]
                    notes_dict[note_type] = note_val
                
                report_container = { 
                    "reportImage" : entry_num_var[10],
                    "legendImage" : entry_num_var[9],
                    "reportNotes" : repr(notes_dict["reportNotes"].replace("\n", "\\n"))
                }

                two_wind_array = queries.getAllTwoWind(myDb,entry_num_variable)
                data_two_wind = []
                for row in two_wind_array: 
                    data_two_wind_array = []    
                    data_two_wind_array.append(row[2])
                    data_two_wind_array.append(queries.getBusDetails(myDb,row[3])[0])
                    data_two_wind_array.append(queries.getBusDetails(myDb,row[3])[1])
                    data_two_wind_array.append(row[4])                    
                    for element in row[5:]:
                        data_two_wind_array.append(str(converter.int_bits_to_float(int(element))))
                data_two_wind.append(data_two_wind_array)

                # Delete entry in Machine Power Flow Data table
                two_mac_array = queries.getAllMachine(myDb,entry_num_variable)
                two_mac_power = []
                for row in two_mac_array:
                    two_mac_power_array = []
                    two_mac_power_array.append(queries.getBusDetails(myDb,row[2])[0])
                    two_mac_power_array.append(queries.getBusDetails(myDb,row[2])[1])
                    two_mac_power_array.append(str(converter.int_bits_to_float(int(row[3]))))
                    two_mac_power_array.append(str(converter.int_bits_to_float(int(row[4]))))
                    two_mac_power_array.append(row[5])
                    for element in row[6:13]:
                        two_mac_power_array.append(str(converter.int_bits_to_float(int(element))))
                    two_mac_power_array.append(row[13])
                    two_mac_power_array.append(row[14])
                    two_mac_power.append(two_mac_power_array)

                # Create the report dictionary
                report_dict = {
                    "about_report" : about_report,
                    "report_container" :  report_container,
                    "two_winding_table": {
                        "data": data_two_wind,
                        "footnote" : repr(notes_dict["two_winding_footnote"].replace("\n", "\\n"))
                    },
                    "machine_seq_table":{
                        "data": two_mac_power,
                        "footnote" : repr(notes_dict["machine_seq_footnote"].replace("\n", "\\n"))
                    }
                }

                table_variables = queries.getTableEntriesID(myDb,entry_num_variable)

                #For each dynamic table in the report
                for table_variable_val in table_variables:
                    if table_variable_val:
                        table_variable = table_variable_val[0] 
                        example_variable = table_variable_val[1]

                        model_example = queries.getModelExample(myDb,example_variable)
                        bus_results = queries.getBusResult(myDb,table_variable) 

                        bus_list = []
                        for row in bus_results:
                            bus_data = {
                                "bus": row[0],
                                "id":  row[1]
                            }
                            bus_list.append(bus_data)

                        con_results =   queries.fetch_con_icons(myDb,table_variable, 1)
                        con_list = queries.fetch_con_icons_list(model_example,converter, con_results, data)

                        icon_results =  queries.fetch_con_icons(myDb,table_variable, 2)
                        icon_list = queries.fetch_con_icons_list(model_example,converter, icon_results, data)

                    tab = {
                            "bus" :bus_list,
                            "con" : con_list,
                            "icon" : icon_list,
                            "image_variable" : table_variable_val[2]
                        }
                    queries.add_item(['Model',model_example[0],model_example[1],"Figure"],tab,report_dict)

                return report_dict
            except Exception as e:
                # Rollback the transaction if an error occurs
                myDb.cursor.rollback()
                print("An error occurred:", str(e))