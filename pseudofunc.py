import random
import string
from queries import queries as query
class pseudofunc:
    def __init__(self):
        pass
    @staticmethod
    def add_item(key_path, value,sendToDb):
        current_dict = sendToDb
        for key in key_path[:-1]:
            if key not in current_dict:
                current_dict[key] = {}
                
            current_dict = current_dict[key]
        current_dict[key_path[-1]] = value

    @staticmethod
    def check_figure_existence(Model, Model_Example, Figure ,data):
        if 'Model' in data and Model in data['Model'] and Model_Example in data['Model'][Model]:
            gensal_model = data['Model'][Model][Model_Example]
            if Figure in gensal_model:
                return 'Yes'
        return 'No'


    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_letters+string.digits
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    @staticmethod
    def processFormData(json_data,json_image,sendToDb):
        Fig = "Figure"
        count = 0
        while pseudofunc.check_figure_existence(json_data['model'],json_data['name'],Fig,sendToDb) == "Yes":
            Fig = Fig + str(count)
            count+=1
        if('busIDTable' in json_data):
            for item in json_data['busIDTable']:
                if item['bus'] != '':
                    pseudofunc.update_value(item['bus'],int)
                else:
                    item['bus'] = 0
                if item['id'] != '':
                    pseudofunc.update_value(item['id'],int)
                else:
                     item['id'] = 0
            pseudofunc.add_item(['Model',json_data['model'],json_data['name'],Fig,'bus'],json_data['busIDTable'],sendToDb)
        if('conTable' in json_data):
            for item in json_data['conTable']:
                if item['col4'] != '':
                    pseudofunc.update_value(item['col4'],float)
                else:
                    item['col4'] = 0
            pseudofunc.add_item(['Model',json_data['model'],json_data['name'],Fig,'con'],json_data['conTable'],sendToDb)
        if('iconTable' in json_data):
            for item in json_data['iconTable']:
                if item['col4'] != '':
                    pseudofunc.update_value(item['col4'],float)
                else:
                    item['col4'] = 0
            pseudofunc.add_item(['Model',json_data['model'],json_data['name'],Fig,'icon'],json_data['iconTable'],sendToDb)
        if(json_image is not None):
            pseudofunc.add_item(['Model',json_data['model'],json_data['name'],Fig,'image'],json_image,sendToDb)
        else:
            pseudofunc.add_item(['Model',json_data['model'],json_data['name'],Fig,'image'],"Empty",sendToDb)
   
    @staticmethod
    def login_successful(myDb,Bcrypt,username, password):
        user_id = query.login_id(myDb,username, password)
        if int(user_id[0]) != 0:
            if(Bcrypt.check_password_hash(user_id[2], password)):
                return "confirmed"
        return "unconfirmed"
    
    @staticmethod
    def are_elements_str(data, dataType):
        updated_data = []
        for item in data:
            pseudofunc.update_value(item,dataType)
            updated_data.append(item)
        return updated_data
    
    @staticmethod
    def update_value(item,dataType):
        if not isinstance(item, dataType):
            item = dataType(item)