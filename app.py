from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models.models import Information
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///models/ang.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home/home.html")

@app.route("/fv/", methods=['GET','POST'])
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
        messages.append({"type":"success","message":"Form recorded successfully"})
    return render_template("fv/home.html", messages=messages)

@app.route("/gov/")
def gov_home():
    return render_template("gov/dashboard.html")

if __name__=="__main__":
    app.run(debug=True, port=8000)