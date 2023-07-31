import random
import json
import os
import shutil
from datetime import datetime
from database import Database
import string
from queries import queries
from FloatingPointConverter import FloatingPointConverter

locations = ["Brandon", "Dorsey", "Grand Rapids", "Great Falls", "Jenpeg", "Kelsey", "Kettle", "Limestone", "Long Spruce", "McArthur", "Pine Falls", "Point du Bois", "Selkirk", "Seven Sisters", "St Joseph", "St Leon", "Wuskwatim"]
generator_owners = ["Manitoba Hydro Generation & Wholesale Business Unit", "BC Hydro", "Ontario Power Generation", "Alberta Power Ltd.", "Hydro-Québec"]
consultants = ["System Performance", "Energy Solutions", "Power Engineering", "Grid Optimization", "Renewable Energy"]
footnotes = ["Notes:\\n1. The first is the first of the first\\n2. The second is the second of the second", "Notes:\\n1. Random note is a random note of a random note\\n2. Another random note is not a particular random note", "Notes:\\n1. Footnote is a foot and note combined1\\n2. Footnote 2: here we have two foot notes", "Notes:\\n1. A\\n2. B", "Notes:\\n1. One\\n2. Two"]
generator_models = ["GENROU", "GENSAE", "GENSAL"]
stabilizer_models = ["IEEEST", "PSS2A"]
excitation_system_models = ["ESST1A", "IEEET1"]
turbine_governor_models = ["HYGOV2", "IEESGO", "PIDGOV"]

initials = ["M.A","A.C","B.A","T.A","S.S"]

current_date = datetime.now().strftime("%Y-%m-%d")
current_year = datetime.now().year

data = json.load(open('model.json'))

json_objects = []
def createDict(report_note,mac_footnote,two_footnote):
    return {
        "reportNotes": report_note,
        "machine_seq_footnote" : mac_footnote,
        "two_winding_footnote":two_footnote
    }

def generate_random_Mac(num):
    num_rows = random.randint(1, 10)  # Random number of rows (between 1 and 6)
    data = []
    for _ in range(num_rows):
        row = [str(random.randint(100000, 999999))] + [str(random.randint(1, 10))] + [str(round(random.uniform(-5, 10), random.randint(1, 5)))] + [str(round(random.uniform(-5, 10), random.randint(1, 5)))] + [str(random.randint(100000, 999999))] + [str(round(random.uniform(-5, 10), random.randint(1, 6))) for _ in range(num-7)] + [str(random.randint(1, 3))] + [str(random.randint(1, 3))]
        data.append(row)
    return data

def generate_random_Two(num):
    num_rows = random.randint(1, 10)  # Random number of rows (between 1 and 6)
    data = []
    for _ in range(num_rows):
        row = [str(random.randint(100000, 999999))] + [str(random.randint(100000, 999999))] + [random.randint(1, 10)] + [random.choice(string.ascii_uppercase) + str(random.randint(1, 10))] + [round(random.uniform(-5, 10), random.randint(1, 6)) for _ in range(num-4)]
        data.append(row)
    
    return data

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def copy_files_in_folder(source_folder, destination_folder, name_length=15):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    copied_files = []

    for filename in os.listdir(source_folder):
        if os.path.isfile(os.path.join(source_folder, filename)):
            random_name = generate_random_string(name_length) + os.path.splitext(filename)[1]
            source_file_path = os.path.join(source_folder, filename)
            destination_file_path = os.path.join(destination_folder, random_name)
            shutil.copy(source_file_path, destination_file_path)
            copied_files.append("http://localhost:3000/uploads/" + random_name)

    return copied_files

report_image = copy_files_in_folder('C:\\Users\\makintunde\\Desktop\\random data\\Report_Image', 'C:\\Users\\makintunde\\Desktop\\PSSE\\PSSE-TOOL\\Web Server\\uploads', name_length=15)
dyr_image = copy_files_in_folder('C:\\Users\\makintunde\\Desktop\\random data\\Model_Image', 'C:\\Users\\makintunde\\Desktop\\PSSE\\PSSE-TOOL\\Web Server\\uploads', name_length=15)

for _ in range(1000):
    revision_year = random.randint(current_year-10, current_year)
    effective_year = random.randint(current_year - 15, current_year)

    revisions = [ f"{revision_year}-01-01",f"{revision_year}-12-31",f"{revision_year}-02-28",f"{revision_year}-11-30",f"{revision_year}-03-31"]

    effective_dates = [f"{effective_year}-10-04",f"{effective_year}-05-12",f"{effective_year}-08-20",f"{effective_year}-11-15",f"{effective_year}-06-03"]
   
    report_notes = ["Note that not all equipment shown on the Point Of Interconnection diagram in the Interconnection Operating Agreement or other Facility Electrical Single Line Diagrams can represented in the powerflow model.\n1.) The powerflow representation drops the character ‘G’ in\n      the generator unit identifier.\n2.)  With cooling the transformer ratings are,\n       90/120/150 MVA with ONAN/ONAF/ONAF.","Note that not all equipment shown on the Point Of Interconnection diagram in the Interconnection Operating Agreement or other Facility Electrical Single Line Diagrams can represented in the powerflow model.\n1.) The powerflow representation drops the character ‘G’ in\n      the generator unit identifier.\n2.)  With cooling the transformer ratings are,\n       72/96/120 MVA with ONS/ONP/ONPP.","Note that not all equipment shown on the Point Of Interconnection diagram in the Interconnection Operating Agreement or other Facility Electrical Single Line Diagrams can represented in the powerflow model.\n1.) The powerflow representation drops the character ‘G’ in\n      the generator unit identifier.\n2.)  With cooling the transformer ratings are,\n       37.5 MVA with ONW.\n3.)  With cooling the transformer ratings are,\n       13.5/18 MVA with ONAN/ONAF."]
    mac_note = ["*      The PSSE machine’s bus base voltage must match the machine nominal voltage.\n**    Pmax represents the maximum power output at rated power factor of 0.95.\n***   Pmin represents the minimum output level the unit is allowed to operate at under typical conditions (as provided by the system operator); the unit may be capable of\n       lower output.\n**** Machine powerflow impedance must equal the sub-transient reactance for some generator dynamics models.","*      The PSSE machine’s bus base voltage must match the machine nominal voltage.\n**     Machine powerflow impedance must equal the sub-transient reactance for some generator dynamics models.\n","*      The PSSE machine’s bus base voltage must match the machine nominal voltage. \n**    Pmax represents the maximum power output at 0.9 operating power factor. (The nameplate rated power factor is 0.9 for Unit 1 and 0.8 for all other units.)\n***   Pmin represents the minimum output level the unit is allowed to operate at under typical conditions.\nb**** Machine powerflow impedance must equal the sub-transient reactance for some generator dynamics models.\n***** Units 3, 5, 7 and 11 are officially retired and physically removed. Unit 4 is not connected to the system."]
    two_note = ["*    Typical operating tap position required. Generator is to provide details if there is more than one typical value.\n**   If Auto Adjust is set to ‘No’, any values are acceptable for these fields. The PSSE default in this case is 1.5 to 0.51 pu. \n*** Winding 2 tap ratio can be used to represent an off-load tap which cannot be adjusted during a PSSE simulation. If it exists details of this tap must be provided in the transformer data submission."]




    model_categories = random.sample(["Generator Models", "Stabilizer Models", "Excitation System Models", "Turbine-Governor Models"], random.randint(2, 3))
    models = {}
    bus_numbers = [str(random.randint(100000, 999999)) for _ in range(6)]  # Generate bus numbers
    for category in model_categories:
        if category == "Generator Models":
            generator_model = random.choice(generator_models)
            variables = []
            selected_bus_numbers = random.sample(bus_numbers, random.randint(3, 6))  # Randomly select bus numbers
            for bus_number in selected_bus_numbers:
                variables.append({
                    "bus": bus_number,
                    "id": random.randint(1, 11)
                })
            con_variables = []
            icon_variables = []
            if 'prop' in data['Model'][category][generator_model]:
                prop = data['Model'][category][generator_model]['prop']
                if 'con' in prop:
                    con_data = prop['con']
                    for i, row in enumerate(con_data):
                        col1 = row[0]
                        col2 = row[1]
                        col3 = row[2]
                        col4 = round(random.uniform(-5, 10), random.randint(1, 5))
                        con_variables.append({"col1": col1, "col2": col2, "col3": col3, "col4": col4})
                if 'icon' in prop:
                    icon_data = prop['icon']
                    for i, row in enumerate(icon_data):
                        col1 = row[0]
                        col2 = row[1]
                        col3 = row[2]
                        col4 = round(random.uniform(-5, 10), random.randint(1, 5))
                        icon_variables.append({"col1": col1, "col2": col2, "col3": col3, "col4": col4})

                con = con_variables
                icon = icon_variables
                models["Generator Models"] = {
                    generator_model: {
                        "Figure": {
                            "bus": variables,
                            "con": con,
                            "icon": icon,
                            "image" : random.choice(dyr_image)
                        }
                    }
                }
        elif category == "Stabilizer Models":
            stabilizer_model = random.choice(stabilizer_models)
            variables = []
            selected_bus_numbers = random.sample(bus_numbers, random.randint(1, 6))  # Randomly select bus numbers
            for bus_number in selected_bus_numbers:
                variables.append({
                    "bus": bus_number,
                    "id": random.randint(1, 100)
                })

            con_variables = []
            icon_variables = []
            if 'prop' in data['Model'][category][stabilizer_model]:
                prop = data['Model'][category][stabilizer_model]['prop']
                if 'con' in prop:
                    con_data = prop['con']
                    for i, row in enumerate(con_data):
                        col1 = row[0]
                        col2 = row[1]
                        col3 = row[2]
                        col4 = random.uniform(-10, 10)
                        con_variables.append({"col1": col1, "col2": col2, "col3": col3, "col4": col4})
                if 'icon' in prop:
                    icon_data = prop['icon']
                    for i, row in enumerate(icon_data):
                        col1 = row[0]
                        col2 = row[1]
                        col3 = row[2]
                        col4 = random.uniform(-10, 10)
                        icon_variables.append({"col1": col1, "col2": col2, "col3": col3, "col4": col4})


                con = con_variables
                icon = icon_variables
                models["Stabilizer Models"] = {
                    stabilizer_model: {
                        "Figure": {
                            "bus": variables,
                            "con": con,
                            "icon": icon,
                            "image" : random.choice(dyr_image)
                        }
                    }
                }
        elif category == "Excitation System Models":
            excitation_model = random.choice(excitation_system_models)
            variables = []
            selected_bus_numbers = random.sample(bus_numbers, random.randint(1, 6))  # Randomly select bus numbers
            for bus_number in selected_bus_numbers:
                variables.append({
                    "bus": bus_number,
                    "id": random.randint(1, 100)
                })
            con_variables = []
            icon_variables = []
            if 'prop' in data['Model'][category][excitation_model]:
                prop = data['Model'][category][excitation_model]['prop']
                if 'con' in prop:
                    con_data = prop['con']
                    for i, row in enumerate(con_data):
                        col1 = row[0]
                        col2 = row[1]
                        col3 = row[2]
                        col4 = random.uniform(-10, 10)
                        con_variables.append({"col1": col1, "col2": col2, "col3": col3, "col4": col4})
                if 'icon' in prop:
                    icon_data = prop['icon']
                    for i, row in enumerate(icon_data):
                        col1 = row[0]
                        col2 = row[1]
                        col3 = row[2]
                        col4 = random.uniform(-10, 10)
                        icon_variables.append({"col1": col1, "col2": col2, "col3": col3, "col4": col4})

            con = con_variables
            icon = icon_variables
            models["Excitation System Models"] = {
                excitation_model: {
                    "Figure": {
                        "bus": variables,
                        "con": con,
                        "icon": icon,
                         "image" : random.choice(dyr_image)
                    }
                }
            }
            
        elif category == "Turbine-Governor Models":
            turbine_model = random.choice(turbine_governor_models)
            variables = []
            selected_bus_numbers = random.sample(bus_numbers, random.randint(1, 6))  # Randomly select bus numbers
            for bus_number in selected_bus_numbers:
                variables.append({
                    "bus": bus_number,
                    "id": random.randint(1, 100)
                })
            con_variables = []
            icon_variables = []
            if 'prop' in data['Model'][category][turbine_model]:
                prop = data['Model'][category][turbine_model]['prop']
                if 'con' in prop:
                    con_data = prop['con']
                    for i, row in enumerate(con_data):
                        col1 = row[0]
                        col2 = row[1]
                        col3 = row[2]
                        col4 = random.uniform(-10, 10)
                        con_variables.append({"col1": col1, "col2": col2, "col3": col3, "col4": col4})
                if 'icon' in prop:
                    icon_data = prop['icon']
                    for i, row in enumerate(icon_data):
                        col1 = row[0]
                        col2 = row[1]
                        col3 = row[2]
                        col4 = random.uniform(-10, 10)
                        icon_variables.append({"col1": col1, "col2": col2, "col3": col3, "col4": col4})

            con = con_variables
            icon = icon_variables
            models["Turbine-Governor Models"] = {
                turbine_model: {
                    "Figure": {
                        "bus": variables,
                        "con": con,
                        "icon": icon,
                        "image" : random.choice(dyr_image)
                    }
                }
            }

    access_options = {
        1: ["Interconnection Request", "AS-Built", "NERC"],
        2: ["Preliminary"]
    }

    selected_role = random.randint(1, 2)

    selected_entry_type = random.choice(access_options[selected_role])

    report = {
        "about_report": {
            "role": selected_role,
            "LoginID" : 1,
            "access" : access_options[selected_role],
            "location": random.choice(locations),
            "generator_owner": random.choice(generator_owners),
            "consultant": random.choice(consultants),
            "initials": random.choice(initials),
            "entry-type" : selected_entry_type,
            "revision_date": random.choice(revisions),
            "effective_date": random.choice(effective_dates)
        },
        "report_container": {
            "reportImage": random.choice(report_image),
            "legendImage": "static/legend.png",
            "reportNotes": random.choice(report_notes),
            "busNumbers": bus_numbers
        },
        "machine_seq_table" : {
            "data": generate_random_Mac(14),
            "footnote": random.choice(mac_note)
        },
        "two_winding_table" : {
            "data": generate_random_Two(31),
            "footnote": random.choice(two_note)
        },
        "Model": models
    }
    json_objects.append(report)

# Create the global dictionary
global_dict = {}

# Append each JSON object to the global dictionary
for i, obj in enumerate(json_objects):
    global_dict[f"JSON_Object_{i+1}"] = obj

# Write the global dictionary to the file
with open("randomtest.json", "w") as file:
    json.dump(global_dict, file, indent=4)
    print("Completed")


data = json.load(open('model.json'))

myDb = Database()
myDb.connectDB()
myDb.createTables()
myDb.fillTables(data)

query = "INSERT INTO Login (UserName, Password, Role) VALUES ('steve', 'steve-hydro', 1)"
myDb.cursor.execute(query)
myDb.connection.commit()


converter = FloatingPointConverter()
sendToDbs = json.load(open('randomtest.json'))
for i,sendToDb in enumerate(sendToDbs.values()):
    try:
        myDb.connection.autocommit = False
        #Get the Server Current Date. 
        version_id = queries.getVersionID(myDb,sendToDb['about_report']['effective_date'])
        #Get the Entry Type.
        entry_type = queries.getEntryType(myDb,sendToDb['about_report']['entry-type'])
        #Find if the Generation Station and Make sure it exist. 
        station_number = queries.find_station(myDb,sendToDb['about_report']['location'])
        if(station_number != None):
            entry_num = queries.addEntry(myDb,version_id,entry_type,1,sendToDb['about_report'],sendToDb['report_container'])
            queries.loginaccessentry(myDb,entry_num,sendToDb['about_report']['LoginID'])
            queries.addNotes(myDb,createDict(sendToDb['report_container']['reportNotes'],sendToDb['machine_seq_table']['footnote'],sendToDb['two_winding_table']['footnote']),entry_num)            #There is a problem here. 
            queries.addMacseq(myDb,converter,entry_num,sendToDb['machine_seq_table']['data'])
            queries.addTwoWind(myDb,converter,entry_num, sendToDb['two_winding_table']['data'])
            queries.addTableEntry(myDb,entry_num,data,converter,sendToDb['Model'])
            myDb.connection.commit()
            myDb.connection.autocommit = True
            print(f"Completed {i+1}")
        else:
            print("Station does not exist. Thus we cannot insert")
    except Exception as e:
        # Rollback the transaction if an error occurs
        print(e)
