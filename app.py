from flask import Flask, render_template, request,redirect, Response,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models.models import Information, Users, Result, Admin,db
from data import data
import csv
import json
import hashlib
from os import listdir, path
from PIL import Image
from flask_socketio import SocketIO, emit      
from io import BytesIO
import base64
from datetime import datetime

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///models/ang.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['FILE_UPLOADS']='upload/'
app.config['SECRET_KEY']='debian'
# app.config['SERVER_NAME']="127.0.0.1:8000"
app.config['DEBUG']=True

sio=SocketIO(app)
db = SQLAlchemy(app)


def admin_authenticated():
    if session:
        if session['user']:
            return True
    else:
        return False

messages=[]
def message(msg):
    messages.append(msg)
    return messages


@app.route("/", methods=['GET','POST'])
def home():
    return render_template("home/home.html", messages=messages)

@app.route("/help",methods=['GET','POST'])
def api_help():
    return render_template("home/using_api.html")


@sio.on('input image',namespace="/")
def get_Image(response=False):
    image_data = response.split(',')[1]
    stream = BytesIO(base64.b64decode(image_data))
    img = Image.open(stream)

    #img is an image file Do image processing here

    
    # with open("static/upload/result_image/"+img_name+".jpg","w") as f:
    save=False
    #     f.write(image_data)
    if save:
        img_name = datetime.utcnow().strftime("%y%m%d%H%M%S%f")
        img.save(f'static/upload/result_image/{img_name}.jpeg')

    #if result image is image binary: convert to base64 
    base64Image = base64.b64encode(stream.getvalue()).decode()
    # print(image_data[:50])
    # print(base64Image)
    #if result image is base64:
    image_data = f"data:image/jpeg;base64, {base64Image}"
    emit('output image', {"image_data":image_data}, namespace="/")
    


@app.route("/fv/", methods=['GET'])
def fv_home():
    messages=[]
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        gender=request.form['gender']
        email=request.form['email']
        info=Information(name=name,age=age,gender=gender,email=email)
        db.session.add(info)
        db.session.commit()
        messages=message({"type":"success","message":"Form recorded successfully"})
    return render_template("fv/home.html", messages=messages)

@app.route("/admin/")
def admin_home():
    if admin_authenticated():
        age_groups={}
        for data in Result.query.all():
            key1 = data.age_group

            if key1 not in age_groups.keys():
                age_groups[key1]={}
                age_groups[key1][data.gender]=1
            else:
                if data.gender not in age_groups[key1].keys():
                    age_groups[key1][data.gender]=1
                else:
                    age_groups[key1][data.gender]+=1
        return render_template("admin/dashboard.html", bardata=json.dumps(age_groups))
    else:
        return redirect('/')


@app.route("/dataupload", methods=['POST'])
def data_upload():
    if admin_authenticated:
        if request.method=="POST":
            csv_file = request.files['file']
            csv_read=csv.DictReader(csv_file.filename)
            # # print(dir(csv_file),csv_file)
            filepath=path.join(app.config['FILE_UPLOADS'],csv_file.filename)
            with open(filepath,"r") as f:
                read_file = csv.DictReader(f)
                for lines in read_file:
                    tmp = Result(age_group=str(lines['age_group']),gender=lines['gender'])
                    db.session.add(tmp)
                    db.session.commit()
        return redirect('../admin/')
    else:
        messages=message({"type":"danger","message":"Unauthenticated"})
        return redirect ('/'), 401

@app.route('/admin/login', methods=['GET'])
def login():
    if request.method=='GET':
        return render_template('admin/login.html')


@app.route('/admin/login/submit', methods=['POST'])
def login_authenticate():
    messages=[]
    if request.method=="POST":
        if request.form['email']:
            email = request.form['email']
        else:
            messages=message({"type":"danger","message":"Email Required"})
            return redirect('/admin/login')
        if request.form['password']:
            password=request.form['password']
        else:
            messages=message({"type":"danger","message":"Password Required"})
            return redirect('/admin/login')
        check = Admin.query.filter_by(email=email).first()
        if check.password==password:
            session['user']=email
            return redirect('/admin/')

    return redirect('/admin/login')

@app.route('/admin/gallery')
def admin_gallery():
    file_path='static/upload/result_image'
    files =listdir(file_path) 
    print(listdir(file_path))
    return render_template('admin/gallery.html', images = files)


@app.route('/admin/logout')
def admin_logout():
    session.pop('user')
    return redirect('../../')
@app.route('/register/', methods=['POST'])
def register():
    messages=[]
    if request.method=="POST":
        email = request.form['email']

        check_existing = Users.query.filter_by(email=email).first()
        if check_existing:
            messages=message({"type":"success","message":"Your email is already registered. Your api key is sent via your email."})
        else:
            user = Users(email=email,key="good")
            db.session.add(user)
            db.session.commit()
            messages=message({"type":"success","message":"Email submitted successfully. "})
    return redirect('../')



if __name__=="__main__":
    sio.run(app, debug=True, port=8000)