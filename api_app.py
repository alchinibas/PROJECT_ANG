from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from models.models import Users

api_app = Flask(__name__)
api_app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///models/ang.db"
api_app.config['SQLALCHMEY_TRACK_MODIFICATIONS']=True
api=Api(api_app)
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
            return {"gread":"hogt itier"}, 200
            saved_api=Users.query.filter(key=api_key)[0]
            print(saved_api)
            if saved_api:
                return {"your email":saved_api.email}, 200
            #update the accessor
            #load model
            else:
                return {"response":"not found"}, 404
        return {"you key":api_key}, 400

api.add_resource(FormValidate,"/getclass/<string:api_key>")
