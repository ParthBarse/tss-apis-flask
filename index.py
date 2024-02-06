from flask import Flask
from flask_login import login_user
from flask import request, session
from pymongo import MongoClient
from flask import Flask, request, jsonify, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
# from datetime import datetime
# from datetime import datetime, timedelta
import datetime
import random
import json
from email.mime.text import MIMEText
import smtplib
import uuid
import re
import os

app = Flask(__name__)
CORS(app)

client = MongoClient(
    'mongodb+srv://harsh:Harsh9945khosla@cluster0.osfevs6.mongodb.net/test')
app.config['MONGO_URI'] = 'mongodb+srv://harsh:Harsh9945khosla@cluster0.osfevs6.mongodb.net/test'
app.config['SECRET_KEY'] = 'a6d217d048fdcd227661b755'
db = client['test']
# db2 = client['BnB_all_customers']
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "ic2023wallet@gmail.com"
app.config['MAIL_PASSWORD'] = "irbnexpguzgxwdgx"

host = ""


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def home():
    return 'home page'


# ------------------------------------------------------------------------------------------------------------

@app.route('/updateStudent', methods=['PUT'])
def update_student():
    try:
        data = request.form

        # Check if sid is provided
        if 'sid' not in data:
            raise ValueError("Missing 'sid' in the request.")

        # Find the student based on sid
        students_db = db["students_db"]
        student = students_db.find_one({"sid": data['sid']})

        if not student:
            return jsonify({"error": f"No student found with sid: {data['sid']}"}), 404  # Not Found

        # Update the student information with the received data
        for key, value in data.items():
            if key != 'sid':
                student[key] = value

        # Update the student in the database
        batches_db = db["batches_db"]
        batch = batches_db.find_one({"batch_id":data.get("batch_id")}, {"_id":0})
        if batch:
            if int(batch["students_registered"]) <= int(batch["batch_intake"]):
                students_db.update_one({"sid": data['sid']}, {"$set": student})
                return jsonify({"message": f"Student with sid {data['sid']} updated successfully"})
            else:
                return jsonify({"message": "Batch is Already Full !"},400)
        else:
            return jsonify({"message": "Batch not Found !"},400)
            
        # students_db.update_one({"sid": data['sid']}, {"$set": student})
        # return jsonify({"message": f"Student with sid {data['sid']} updated successfully"})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    

#-----------------------------------------------------------------------------------
    
UPLOAD_FOLDER = '/var/www/html/tss_files/All_Files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from io import BytesIO
def generate_unique_filename(file):
    ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
    return str(uuid.uuid4()) + '.' + ext

@app.route('/upload', methods=['POST'])
def upload_files():
    slider_photos = request.files.getlist('files')
    if not slider_photos:
        return jsonify({"error": "Please send Files to Store."})
    
    slider_filenames = [generate_unique_filename(photo) for photo in slider_photos]

    for i, photo in enumerate(slider_photos):
        photo.save(os.path.join(UPLOAD_FOLDER, slider_filenames[i]))

    return jsonify({"urls": ["http://64.227.186.165/tss_files/All_Files/" + filename for filename in slider_filenames]}), 200




@app.route('/addProducts_inventory', methods=['POST'])
def addProducts_inventory():
    try:
        import uuid
        collection = db['products_inventory']
        data = request.get_json()  # Use get_json() instead of request.json

        # Check if data is a valid dictionary
        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid JSON format. Expected a dictionary.',"success":False}), 400
        
        pid = uuid.uuid4().hex

        data['pid'] = pid

        # Save the modified data to MongoDB
        collection.insert_one(data)

        return jsonify({'message': 'Data stored successfully.',"success":True}), 200

    except Exception as e:
        return jsonify({'error': str(e),"success":False}), 500
    



@app.route('/editProduct', methods=['PUT'])
def edit_product():
    try:
        import uuid
        collection = db['products_inventory']
        data = request.get_json()

        # # Check if data is a valid dictionary
        # if not isinstance(data, dict):
        #     return jsonify({'error': 'Invalid JSON format. Expected a dictionary.', "success": False}), 400

        # Extracting common information
        pid = data.get('pid')
        if pid is None:
            return jsonify({'error': 'Missing "pid" parameter in the request data.', "success": False}), 400

        # Update the student's resume data in MongoDB
        result = collection.update_one({'pid': pid}, {'$set': data})

        # Check if the update was successful
        if result.modified_count > 0:
            return jsonify({'message': 'Data updated successfully.', "success": True}), 200
        else:
            return jsonify({'error': 'No document found for the provided pid.', "success": False}), 404

    except Exception as e:
        return jsonify({'error': str(e), "success": False}), 500
    

    

@app.route('/getAllProducts', methods=['GET'])
def get_all_students_resume():
    try:
        collection = db['products_inventory']
        # Retrieve all students' resumes from MongoDB
        all_resumes = list(collection.find({}, {'_id': 0}))
        return jsonify({'resumes': all_resumes, "success":True}), 200

    except Exception as e:
        return jsonify({'error': str(e),"success":False}), 500
    

@app.route('/getProduct', methods=['GET'])
def get_product():
    try:
        collection = db['products_inventory']
        pid = request.args.get("pid")
        # Retrieve all students' resumes from MongoDB
        resume = collection.find_one({"pid":pid}, {'_id': 0})
        return jsonify({'resume': resume,"success":True}), 200

    except Exception as e:
        return jsonify({'error': str(e),"success":False}), 500



# -------------------------------------------     Chat Module      ---------------------------------------------------------
from datetime import date
from datetime import datetime
from werkzeug.utils import secure_filename
import random
from datetime import date
from datetime import datetime

@app.route("/createticket", methods=["POST"])
def createticket():
    try:
        tickets_db = db["tickets_db"]
        data = request.get_json()
        today = date.today()
        now = datetime.now()
        date1 = today.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")
        # tid = random.getrandbits(32)
        tid = data['uid']
        cid = random.getrandbits(32)

        if not tickets_db.find_one({"tid": tid},{"_id":0}):
            data1 = {
                "tid": tid,
                "metadata": {
                    "usname": data['usname'],
                    "subj": data["subj"],
                    "uid": data['uid'],
                    "status": "open"
                },
                "msgs": [{
                    "cid": cid,
                    "msg": data["msg"],
                    "date": date1,
                    "time": time,
                    "role":data["role"]
                }]
            }
            tickets_db.insert_one(data1)
            return json.dumps({'success': True, "tid": tid}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False, "error": "Ticket already exist"}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'success': False, "error": str(e)}), 200, {'ContentType': 'application/json'}


@app.route("/getticket", methods=["GET", "POST"])
def getticket():
    try:
        tickets_db = db["tickets_db"]
        # user_db = db["members_db_crm"]
        data = request.get_json()
        # uid = data['uid']
        tid = data['tid']
        # all_data = []
        if tickets_db.find_one({"tid": tid}):
            find_data = tickets_db.find({"tid": tid},{"_id":0})
            all_data = list(find_data)
            # print(all_data)
            return jsonify({'success': True, "data": all_data[0],"tid":tid}), 200, {'ContentType': 'application/json'}
        else:
            return jsonify({'success': False, "error": "Ticket not found"}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return jsonify({'success': False, "error": e}), 200, {'ContentType': 'application/json'}
    

@app.route("/getticketlist", methods=["GET"])
def getticketlist():
    try:
        tickets_db = db["tickets_db"]
        user_db = db["members_db_crm"]
        all_data = []
        find_data = tickets_db.find({},{"_id":0})
        all_data = list(find_data)
        return json.dumps({'success': True, "data": all_data}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'success': False, "error": e}), 200, {'ContentType': 'application/json'}
    
@app.route("/replyticket", methods=["POST"])
def replyticket():
    try:
        tickets_db = db["tickets_db"]
        user_db = db["members_db_crm"]
        data = request.get_json()
        # tid = int(data['tid'])
        uid = data["uid"]
        tid = data["tid"]
        if tickets_db.find_one({"tid":tid},{"_id":0}):
            find_data = tickets_db.find_one({"tid":tid},{"_id":0})
            # user_info = user_db.find_one({"uid":uid})
            prev_msgs = find_data["msgs"]
            new_msg = {
                "cid":random.getrandbits(32),
                "msg": data["msg"],
                "date":data["date"],
                "time":data["time"],
                "role":data["role"],
                "uid":uid
            }
            prev_msgs.append(new_msg)
            tickets_db.update_one(
                    {"tid": tid}, {"$set": {"msgs": prev_msgs}})
            return json.dumps({'success': True, "data": new_msg}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False, "error": "Ticket not found"}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'success': False, "error": e}), 200, {'ContentType': 'application/json'}
    
@app.route("/closeticket", methods=["GET", "POST"])
def closeticket():
    try:
        import uuid
        tickets_db = db["tickets_db"]
        # user_db = db["members_db_crm"]
        data = request.get_json()
        tid = data['tid']
        if tickets_db.find_one({"tid": tid}):
            find_data = tickets_db.find_one_and_delete({"tid": tid})
            find_data["metadata"]["status"] = "Closed"
            find_data["tid"] = str(uuid.uuid4().hex)
            tickets_db.insert_one(find_data)
            return json.dumps({'success': True, "error": "Ticket cliosed Successfully"}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False, "error": "Ticket not found"}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'success': False, "error": e}), 200, {'ContentType': 'application/json'}
    



import geoip2.database
def get_location_from_ip_local(ip):
    database_path = 'GeoLite2-City.mmdb'
    reader = geoip2.database.Reader(database_path)
    try:
        response = reader.city(ip)
        city = response.city.name
        region = response.subdivisions.most_specific.name
        country = response.country.name
        latitude = response.location.latitude
        longitude = response.location.longitude
        location = {"city":city, "region":region, "country":country, "latitude":latitude, "longitude":longitude}
        return location
    except geoip2.errors.AddressNotFoundError:
        return "IP address not found in the database"
    finally:
        reader.close()
    

@app.route("/convertIPtoAddress", methods=["POST"])
def convertIPtoAddress():
    try:
        data = request.get_json()
        ip = data['ip']
        if ip:
            ip_address = ip
            location = get_location_from_ip_local(ip_address)
            return json.dumps({'success': True, "address":location}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'success': False, "error": e}), 200, {'ContentType': 'application/json'}
    
# import pandas as pd
# df = pd.read_excel('your_excel_file.xlsx')
# json_data = df.to_json(orient='records')
# with open('output.json', 'w') as f:
#     f.write(json_data)
    
import pandas as pd
@app.route("/exportProducts", methods=["GET"])
def exportProducts():
    try:
        products = db['products']
        all_products = products.find({})
        df = pd.DataFrame(all_products)
        df.to_excel('output.xlsx', index=False)
        save_path = '/var/www/html/tss_files/All_Files/products_list.xlsx'
        df.to_excel(save_path, index=False)
        if os.path.exists(save_path):
            return send_file(save_path, as_attachment=True)
        else:
            return "File could not be found at: {}".format(save_path)
    except Exception as e:
        return json.dumps({'success': False, "error": e}), 200, {'ContentType': 'application/json'}

    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)





