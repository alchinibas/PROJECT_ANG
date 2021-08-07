from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from models.models import Information, Users
from flask_restful import Api, Resource, reqparse
from flask_mail import Mail
from data import data
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///models/ang.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=data['gmail'],
    MAIL_PASSWORD=data['password'],
)
mail=Mail(app)

db = SQLAlchemy(app)


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

@app.route("/gov/")
def gov_home():
    return render_template("gov/dashboard.html")

@app.route('/register/', methods=['POST'])
def register():
    messages=[]
    if request.method=="POST":
        email = request.form['email']

        import hashlib
        from datetime import datetime

        id1 = hashlib.md5(str(datetime.utcnow().strftime("%y%m%d%H%M%S%f")).encode(encoding="utf-8")).hexdigest()
        id2 = hashlib.md5(email.encode(encoding="utf-8")).hexdigest()
        ids = id1+id2
        check_existing = Users.query.filter_by(email=email).first()
        if check_existing:
            ids = check_existing.key
            messages=message({"type":"success","message":"Your email is already registered. Your api key is sent via your email."})
        else:
            user = Users(email=email,key=ids)
            db.session.add(user)
            db.session.commit()
            messages=message({"type":"success","message":"Email submitted successfully. You key is sent via your email. "})
        mail.send_message(
                "API key from PROJECT_ANG",
                sender=data['gmail'],
                recipients=[email,],
                html="<h2>Welcome to ANG</h2> Your api key is \n"+ids
            )
    return redirect('../')


###api
api=Api(app)
get_args = reqparse.RequestParser()
get_args.add_argument("name", type=str, required=False)
get_args.add_argument("email", type=str,required=False)
get_args.add_argument("age", type=int, help="Please specify the clients age",required=True)
get_args.add_argument("gender", type=str, help="Please provide the clients gender",required=True)
get_args.add_argument("photo", type=object,help="Please provide a photo", required=True)
get_args.add_argument("certificate", type=object,required=False)


class FormValidate(Resource):
    def get(self,api_key=1):
        if api_key:
            saved_api=Users.query.filter_by(key=api_key).first()
            if saved_api:
                print(saved_api)
                return {"your email":saved_api.email}, 200
            #update the accessor
            #load model
            else:
                return {"response":"not found"}, 404
        return {"you key":api_key}, 400

api.add_resource(FormValidate,"/getclass/<string:api_key>")

if __name__=="__main__":
    app.run(debug=True, port=8000)