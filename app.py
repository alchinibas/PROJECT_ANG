from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from models.models import Information, Users
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///models/ang.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


messages=[]
def message(msg):
    messages.append(msg)
    return messages


@app.route("/", methods=['GET','POST'])
def home():
    return render_template("home/home.html", messages=messages)

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
        user = Users(email=email,key=ids)
        db.session.add(user)
        db.session.commit()
        messages=message({"type":"success","message":"Email submitted successfully. You key is sent via your email."+ids})
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