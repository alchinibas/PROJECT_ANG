from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

model = Flask(__name__)
model.config['SQLALCHEMY_DATABASE_URI']="sqlite:///ang.db"
model.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(model)

class Information(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40), nullable=True)
    email=db.Column(db.String(100),nullable=True)
    age=db.Column(db.Integer,nullable=False)
    gender=db.Column(db.String(10),nullable=False)
    image=db.Column(db.String(100),nullable=False)

    def __repr__(self)->str:
        return f'{self.name}'

class Users(db.Model):
    email=db.Column(db.String(100),primary_key=True)
    session_started=db.Column(db.DateTime,default=datetime.utcnow)
    key=db.Column(db.String(128),nullable=False)

    def __repr__(self)->str:
        return f'{self.email}'

if __name__=="__main__":
    print("This is not a run file")
