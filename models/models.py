from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


model = Flask(__name__)
model.config['SQLALCHEMY_DATABASE_URI']="sqlite:///ang.db"
model.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(model)

class Information(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40), nullable=False)
    email=db.Column(db.String(100),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    gender=db.Column(db.String(10),nullable=False)

    def __repr__(self)->str:
        return f'{self.name}'

if __name__=="__main__":
    print("This is not a run file")
