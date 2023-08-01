from flask import Flask, render_template, url_for, request, redirect,jsonify,send_file,send_from_directory,session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from database import Database
from queries import queries
from datetime import datetime, timedelta      
import json
import os
from FloatingPointConverter import FloatingPointConverter
from pseudofunc import pseudofunc

global myDb
global data 
global converter

app = Flask(__name__, static_url_path='/static')
bcrypt = Bcrypt(app)
app.template_folder = "templates"
app.static_folder = 'static'
UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.secret_key = os.urandom(24)  

data = json.load(open('model.json'))

# Connect to the database
myDb = Database()
myDb.connectDB()
# myDb.createTables()
# myDb.fillTables(data)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://MH504623\\SQLEXPRESS/GENERATOR_DATA?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SESSION_TYPE'] = 'sqlalchemy'
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db  
sess = Session(app)

with app.app_context():
    db.create_all()

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Change to Integer column type
    data = db.Column(db.LargeBinary)
    expiry = db.Column(db.DateTime)
    __table_args__ = {'extend_existing': True}

converter = FloatingPointConverter()


count = 0

# with app.app_context():
#     # Create the session table in the database
#     db.create_all()

@app.route('/uploads/<filename>')
def serve_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# HOME PAGE
# When you go to localhost:3000/ - The server will generate the home page. This supposed to be a login page but right now it is ADMIN and USER
@app.route('/', methods=['GET', 'POST'])
def admin():
        session.clear()
        return render_template('loginpage.html')

@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'GET':
        return render_template('landing.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if isinstance(username, str) and isinstance(password, str):
        if pseudofunc.login_successful(myDb, bcrypt, username, password) == "confirmed":

            session['sendToDb'] = {
                'about_report': {'role': queries.get_user_role(myDb, username),'LoginID': queries.login_id(myDb, username, password)[0]}
            }
            redirect_url = determine_redirect_url(session['sendToDb']['about_report']['role'])
            session['logged_in'] = True
            return jsonify({'redirect_url': redirect_url}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

    
def determine_redirect_url(role):
    sendToDb = session.get('sendToDb', {})
    if role == 1:
        sendToDb['about_report'].update({
            'access': ["Interconnection Request", "AS-Built", "NERC"]
        })
        session['sendToDb'] = sendToDb
        return '/choose'
    elif role == 2:
        sendToDb['about_report'].update({
            'access': ["Preliminary"]
        })
        session['sendToDb'] = sendToDb
        return '/choose'
    else:
        sendToDb['about_report'].update({
            'access': ["user"]
        })
        session['sendToDb'] = sendToDb
        return '/generate_dyr'
    

# Choosing Generation Station Page
# When you go to localhost:3000/ - The server will generate the home page.
@app.route('/generation-station', methods=['GET', 'POST'])
def generate_station():
    sendToDb = session.get('sendToDb', {})
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'POST':
        location = request.form.get('location')
        generator = request.form.get('generator-owner')
        consultant= request.form.get('consultant')
        initials = request.form.get('initials')
        revision = request.form.get('revision-date')
        effective = request.form.get('effective-date')
        entry = request.form.get('entry-type')
        if isinstance(location,str) and location in data['Location'] and isinstance(generator,str) and isinstance(consultant,str) and isinstance(initials,str):
            sendToDb['about_report'].update({
                'location': location,
                'generator_owner' : generator,
                'consultant': consultant,
                'initials' : initials,
                'entry-type' : entry
            })
            # Validate the date
            try:
                selected_date = datetime.strptime(effective, '%Y-%m-%d').date()
                revision_date = datetime.strptime(revision, '%Y-%m-%d').date()
                current_date = datetime.now().date()
                
                if (selected_date < current_date) and (revision_date < current_date):
                    sendToDb['about_report'].update({
                        'effective_date':effective,
                        'revision_date' : revision
                    })
                else:
                    error_message = "Invalid date. Please choose a past date."
                    return render_template('error.html', error_message=error_message), 401
            except ValueError:
                error_message = "Invalid date format. Please use YYYY-MM-DD."
                return render_template('error.html', error_message=error_message), 401
        else:
            error_message = "Location is required."
            return render_template('error.html', error_message=error_message), 401
        session['sendToDb'] = sendToDb
        return jsonify({'redirect_url': url_for('bus')})
    else:
        return render_template('generation_station.html',access = sendToDb['about_report']['access'])


# BUS PAGE: Selecting Buses We Will be working with 
# In the /bus page
@app.route('/bus', methods=['GET', 'POST'])
def bus():
    sendToDb = session.get('sendToDb', {})
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    if request.method == 'GET':
        location = sendToDb.get('about_report').get('location')
        if location is not None:
            return render_template('bus.html', location=location)
        else:
            return render_template('landing.html')  
    elif request.method == 'POST':
        bus_data = json.loads(request.form.get('data'))
        bus_numbers = bus_data['busNumbers']
        reportNotes = repr(bus_data['reportNotes'].replace("\n", "\\n"))
        report_url = ""
        if 'reportImage' in request.files:
            report_url = photo_upload(request.files['reportImage'])
        if isinstance(bus_numbers, list) and isinstance(reportNotes,str) and isinstance(report_url,str):
            bus_numbers = pseudofunc.are_elements_str(bus_numbers, int)
            sendToDb['report_container'] = {
                'busNumbers': bus_numbers,
                'reportNotes': reportNotes,
                'legendImage': "legend_url",
                'reportImage': report_url
            }
            session['sendToDb'] = sendToDb
            return jsonify({'redirect_url': url_for('generate_machine_seq')})
        else:
            return render_template('landing.html')  # Redirect to a route where the user can choose a location


# MACHINE SEQUENCE PAGE : Fill the Machine Sequence Page 
@app.route('/machine_sequence', methods=['GET', 'POST'])
def generate_machine_seq():
    sendToDb = session.get('sendToDb', {})
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'GET':
        bus_num = sendToDb.get('report_container').get('busNumbers')
        if bus_num is not None:
            return render_template('machine_positive_sequence.html', busNumbers=bus_num)
        else:
            return redirect(url_for('generate_machine_seq'))
    elif request.method == 'POST':
        data = request.get_json()
        data_values = data['values']
        footnote_values = repr(data['notes'].replace("\n", "\\n"))
        if isinstance(data_values,list) and isinstance(footnote_values,str):
            for item in data_values:
                if isinstance(item,list):
                    pseudofunc.update_value(item[0],int)    #should be integer
                    pseudofunc.update_value(item[1],int)    #should be integer
                    for i in range (2,len(item)):
                        pseudofunc.update_value(item[i],float)  #should be float/decimal.
                    sendToDb.update({
                        'machine_seq_table' : {'data':data_values,
                                               'footnote':footnote_values}
                    })
                    session['sendToDb'] = sendToDb
                    return jsonify({'redirect_url': '/two_winding'})
        else:
            return redirect(url_for('generate_machine_seq')) #Fix it

# TWO WINDING PAGE : Fill the Two Winding Page.
@app.route('/two_winding', methods=['GET', 'POST'])
def get_two_winding_page():
    sendToDb = session.get('sendToDb', {})
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'GET':
        if sendToDb.get('machine_seq_table') is not None:
            return render_template('two_winding.html', busNumbers=sendToDb.get('report_container').get('busNumbers'))
        else:
            return redirect(url_for('get_two_winding_page')) 
    elif request.method == 'POST':
        data = request.get_json()
        data_values = data['values']
        footnote_values = repr(data['notes'].replace("\n", "\\n"))
        if isinstance(data_values,list) and isinstance(footnote_values,str):
            for item in data_values:
                if isinstance(item,list):
                    pseudofunc.update_value(item[0],int)    #should be integer
                    pseudofunc.update_value(item[1],int)    #should be integer
                    pseudofunc.update_value(item[2],int)    #should be integer
                    for i in range (4,len(item)):
                        pseudofunc.update_value(item[i],float)  #should be float/decimal.
                    sendToDb.update({
                        'two_winding_table': {'data':data_values,
                                               'footnote':footnote_values}
                    })
                    session['sendToDb'] = sendToDb
                    return jsonify({'redirect_url': '/choose-table'})
            else:
                return redirect(url_for('get_two_winding_page'))

# CON_ICON PAGE
@app.route('/choose-table', methods=['GET', 'POST'])    #Fix it
def CON_ICON():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'GET':
        return render_template('lookup-table.html')
    elif request.method == 'POST':
        model = request.form.get('model')
        name = request.form.get('name')
        if isinstance(model,str) and isinstance(name,str):
            return jsonify({'redirect_url': '/table?model=' + model + '&name=' + name})  # Return JSON response with redirect URL
        else:
            return redirect(url_for('CON_ICON'))

def photo_upload(file):
    filename = pseudofunc.generate_random_string(15) + ".jpg"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return url_for('serve_photo', filename=filename, _external=True)


# CON_ICON PAGE
@app.route('/table', methods=['GET', 'POST'])
def table():
    sendToDb = session.get('sendToDb', {})
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'GET':
        listV = None
        model = request.args.get('model')
        name = request.args.get('name')
        if isinstance(model,str) and isinstance(name,str):
            if model in data['Model']:
                if "prop" in data['Model'][model][name]:
                    listV = data['Model'][model][name]['prop']
                else:
                   return redirect(url_for('CON_ICON'))
            else:
                    return redirect(url_for('CON_ICON'))
            busNumbers = sendToDb.get('report_container').get('busNumbers')
            return render_template('input-table.html', name=name, model=model, busNumbers=busNumbers, list=listV)
        else:
            return redirect(url_for('CON_ICON'))
    elif request.method == 'POST':
        json_data = json.loads(request.form.get('data'))
        file_url =  ""
        if 'file' in request.files:
            file_url = photo_upload(request.files['file'])
        if request.headers.get('X-request-ID') == 'Submit':
            pseudofunc.processFormData(json_data,file_url,sendToDb)
            session['sendToDb'] = sendToDb
            return jsonify({'redirect_url': '/review'})
        elif request.headers.get('X-request-ID') == 'newTable':
            pseudofunc.processFormData(json_data,file_url,sendToDb)
            session['sendToDb'] = sendToDb
            return jsonify({'redirect_url': '/choose-table'})

#Review Page
@app.route('/review')
def review():
    sendToDb = session.get('sendToDb', {})
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    return render_template('review.html', send = sendToDb)


@app.route('/dyr')
def gen_dyr():
    sendToDb = session.get('sendToDb', {})
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    return render_template('dyr_generation.html')

@app.route('/view')
def view():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    report_dict = session.pop('report_dict', None)  
    return render_template('generate_report.html', send=report_dict)


@app.route('/checkout', methods=['POST'])
def complete():
    sendToDb = session.get('sendToDb', {})
    print(sendToDb)
   
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    try:
        if request.get_json().get('confirm') == 'Yes':
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
                queries.addTwoWind(myDb, converter, entry_num, sendToDb['two_winding_table']['data'])
                queries.addTableEntry(myDb,entry_num,data,converter,sendToDb['Model'])
                myDb.connection.commit()
                myDb.connection.autocommit = True
                session['message'] = "Report is created"  # Store the create message in the session
                return jsonify({'redirect_url': '/success'})
            else:
                print("Station does not exist. Thus we cannot insert")
    except Exception as e:
        # Rollback the transaction if an error occurs
        myDb.connection.rollback()
        print("Transaction rolled back. Error: {}".format(str(e)))
        error_message = "A problem occured while inserting data to database. ROLLBACK!"
        return render_template('error.html', error_message=error_message), 401
    
def createDict(report_note,mac_footnote,two_footnote):
    return {
        "reportNotes": report_note,
        "machine_seq_footnote" : mac_footnote,
        "two_winding_footnote":two_footnote  
    }

# Success Page
@app.route('/success')
def success():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    message = session.get('message', '')
    session.pop('message', None)
    return render_template('final.html', message=message)

@app.route('/generate_report', methods=['POST'])
def generateReport():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))

    generate_station = request.form.get('location')
    reportType = request.form.get('reportType')
    date = request.form.get('date')

    if not generate_station or not date:
        return 'Missing parameters', 400

    location = queries.getLocation(myDb, generate_station)
    entryType = queries.getEntryType(myDb, reportType)
    versionID = queries.getVersionID(myDb, date)
    session['report_placeholder'] = {
        "location" : location,
        "entry-type" : entryType,
        "version-id" : versionID
    }

    # Get the Entries_ID for the report entry
    entry_num_var = queries.getEntriesID(myDb, location, entryType, versionID)

    if len(entry_num_var) < 2:
        if entry_num_var:
            report_dict = queries.generate_report(myDb, location, converter, data, entry_num_var[0])
            if report_dict:
                # Report generation was successful
                session['report_dict'] = report_dict  # Store report_dict in session
                return jsonify({'redirect_url': '/view'})
            else:
                error_message = "Could not generate report"
        else:
            error_message = "The report does not exist"
        return render_template('error.html', error_message=error_message)
    else:
        # Store entry_num_var in session and return the redirect URL
        session['entry_num_var'] = entry_num_var
        return jsonify({'redirect_url': '/confirm_report'})

    
keys = ['Generator_Owner', 'Consultant', 'Date', 'Revision', 'Initials', 'Effective_Date']

def arrJson(keys,entry_num_var):
    dictio = {}
    for i,entry in enumerate(entry_num_var):
        entryV ={}
        for j,key in enumerate(keys):
            entryV[key] = entry[3+j]
        dictio[i] = entryV
    return dictio

@app.route('/confirm_report', methods=['GET', 'POST'])
def confirmReport():
    if request.method == 'GET':
        entry_num_var = session.get('entry_num_var')
        if not entry_num_var:
            return 'No entry_num_var found in session', 400
        keys = ['Generator_Owner', 'Consultant', 'Date', 'Revision', 'Initials', 'Effective_Date']
        return render_template('choose_report.html',entries = arrJson(keys,entry_num_var))

    elif request.method == 'POST':
        result = request.json
        report_placeholder = session['report_placeholder']
        
        # Get the Entries_ID for the report entry in details
        entry_num_var = queries.getEntriesIDOne(myDb, report_placeholder["location"], report_placeholder["entry-type"], report_placeholder["version-id"], result['Consultant'], result['Date'], result['Generator_Owner'], result["Initials"])
        if entry_num_var:
            report_dict = queries.generate_report(myDb, report_placeholder["location"], converter, data, entry_num_var)
            if report_dict:
            # Report generation was successful
                session['report_dict'] = report_dict  # Store report_dict in session
                return jsonify({'redirect_url': '/view'})
            else:
                error_message = "Could not generate report"
        else:
            error_message = "The report does not exist"
        return render_template('error.html', error_message=error_message)

@app.route('/generate_dyr', methods=['GET','POST'])
def handle_generate_dyr():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'GET':
         return render_template('generate_dyr.html')
    elif request.method == 'POST':
        generate_station = request.form.get('location')
        reportType = request.form.get('reportType')
        date = request.form.get('date')
        
        if not generate_station or not date:
            return 'Missing parameters', 400
        
        location = queries.getLocation(myDb, generate_station)
        entryType = queries.getEntryType(myDb, reportType)
        versionID = queries.getVersionID(myDb, date)
        session['report_placeholder'] = {
            "location" : location,
            "entry-type" : entryType,
            "version-id" : versionID
        }

        # Get the Entries_ID for the report entry
        entry_num_var = queries.getEntriesID(myDb, location, entryType, versionID)

    if len(entry_num_var) < 2:
        dyr_file_path = queries.generate_dyr(myDb,converter,data,entry_num_var[0])
        
        if os.path.exists(dyr_file_path):
            return send_file(dyr_file_path, as_attachment=True, mimetype="application/octet-stream")
        else:
            error_message = 'Error generating DYR file'
            return render_template('error.html', error_message=error_message)
    else:
        # Store entry_num_var in session and return the redirect URL
        session['entry_num_var'] = entry_num_var
        return jsonify({'redirect_url': '/generate'})
    

@app.route('/generate', methods=['GET', 'POST'])
def genReport():
    if request.method == 'GET':
        entry_num_var = session.get('entry_num_var')
        if not entry_num_var:
            return 'No entry_num_var found in session', 400
        keys = ['Generator_Owner', 'Consultant', 'Date', 'Revision', 'Initials', 'Effective_Date']
        return render_template('gen_report.html',entries = arrJson(keys,entry_num_var))

    elif request.method == 'POST':
        result = request.json
        report_placeholder = session['report_placeholder']
        
        # Get the Entries_ID for the report entry in details
        entry_num_var = queries.getEntriesIDOne(myDb, report_placeholder["location"], report_placeholder["entry-type"], report_placeholder["version-id"], result['Consultant'], result['Date'], result['Generator_Owner'], result["Initials"])
        if not entry_num_var:
            return 'No entry_num_var found in session', 400

        dyr_file_path = queries.generate_dyr(myDb,converter,data,entry_num_var)
        if os.path.exists(dyr_file_path):
            return send_file(dyr_file_path, as_attachment=True, mimetype="application/octet-stream")
        else:
            error_message = 'Error generating DYR file'
            return render_template('error.html', error_message=error_message)

@app.route('/delete-report', methods=['GET', 'POST'])
def delete_report():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    if request.method == 'GET':
         return render_template('delete_report.html')
    elif request.method == 'POST':
        generate_station = request.form.get('location')
        reportType = request.form.get('reportType')
        date = request.form.get('date')
        
        if not generate_station or not date:
            return 'Missing parameters', 400
        
        location = queries.getLocation(myDb, generate_station)
        entryType = queries.getEntryType(myDb, reportType)
        versionID = queries.getVersionID(myDb, date)

        session['report_placeholder'] = {
            "location" : location,
            "entry-type" : entryType,
            "version-id" : versionID
        }

        # Get the Entries_ID for the report entry
        entry_num_var = queries.getEntriesID(myDb, location, entryType, versionID)

        if len(entry_num_var) < 2:
            if entry_num_var:
                if queries.delete_Report(myDb, entry_num_var[0]):
                    session['message'] = "Report is deleted"  # Store the delete message in the session
                    return jsonify({'redirect_url': '/success'})
                else:
                        error_message = "Unable to delete the report."
            else:
                error_message = "Report entry not found."
            return render_template('error.html', error_message=error_message)
        else:
            # Store entry_num_var in session and return the redirect URL
            session['entry_num_var'] = entry_num_var
            return jsonify({'redirect_url': '/delete'})
            

@app.route('/delete', methods=['GET', 'POST'])
def deleteReport():
    if request.method == 'GET':
        entry_num_var = session.get('entry_num_var')
        if not entry_num_var:
            return 'No entry_num_var found in session', 400
        keys = ['Generator_Owner', 'Consultant', 'Date', 'Revision', 'Initials', 'Effective_Date']
        return render_template('delreport.html',entries = arrJson(keys,entry_num_var))

    elif request.method == 'POST':
        result = request.json
        report_placeholder = session['report_placeholder']
        
        entry_num_var = queries.getEntriesIDOne(myDb, report_placeholder["location"], report_placeholder["entry-type"], report_placeholder["version-id"], result['Consultant'], result['Date'], result['Generator_Owner'], result["Initials"])
        if not entry_num_var:
            return 'No entry_num_var found in session', 400

        if entry_num_var:
                if queries.delete_Report(myDb, entry_num_var[0]):
                    session['message'] = "Report is deleted"  # Store the delete message in the session
                    return jsonify({'redirect_url': '/success'})
                else:
                    error_message = "Unable to delete the report."
        else:
            error_message = "Report entry not found."
        return render_template('error.html', error_message=error_message)


@app.route('/dates', methods=['POST'])
def generate_dyr():
    location = request.form.get('location')
    report_type = request.form.get('reportType')

    dates = queries.getDates(myDb,location, report_type)

    data = {'dates': dates} if dates else {'dates': None}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True) 
