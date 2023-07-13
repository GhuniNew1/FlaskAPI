# Server Side
from flask import Flask
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy,Model
app=Flask(__name__)

# #database
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database_data1.db"
api=Api(app)

class Data1Model(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    title=db.Column(db.String(100),nullable=False)
    imgurl=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Data1(name={name},title={title},imgurl={imgurl})"

db.create_all()

#Request Parser
data1_add_args=reqparse.RequestParser()
data1_add_args.add_argument("name",type=str,required=True,help="กรุณาระบุครับ")
data1_add_args.add_argument("title",type=str,required=True,help="กรุณาระบุครับ")
data1_add_args.add_argument("imgurl",required=True,type=str,help="กรุณาระบุครับ")

# #Update Request Parser
data1_add_args=reqparse.RequestParser()
data1_add_args.add_argument("name",type=str,help="กรุณาระบุที่ต้องการแก้ไข")
data1_add_args.add_argument("title",type=str,help="กรุณาระบุที่ต้องการแก้ไข")
data1_add_args.add_argument("imgurl",type=str,help="กรุณาระบุที่ต้องการแก้ไข")


resource_field={
    "id":fields.Integer,
    "name":fields.String,
    "title":fields.String,
    "imgurl":fields.String
}

# #design
class Data2Test(Resource):
    @marshal_with(resource_field)
    def get(self):
        result=Data1Model.query.all()
        return result
    
    @marshal_with(resource_field)
    def post(self):
        args=data1_add_args.parse_args()
        data1=Data1Model(name=args["name"],title=args["title"],imgurl=args["imgurl"])
        db.session.add(data1)
        db.session.commit()
        return data1,201
    
class Data1Test(Resource):

    @marshal_with(resource_field)
    def get(self,data1_id):
        result=Data1Model.query.filter_by(id=data1_id).first()
        if not result:
            abort(404,message="ไม่พบข้อมูลที่คุณร้องขอ")
        return result

    @marshal_with(resource_field)
    def post(self,data1_id):
        result=Data1Model.query.filter_by(id=data1_id).first()
        if result:
            abort(409,message="รหัสนี้เคยบันทึกไปแล้วนะครับ")
        args=data1_add_args.parse_args()
        data1=Data1Model(id=data1_id,name=args["name"],title=args["title"],imgurl=args["imgurl"])
        db.session.add(data1)
        db.session.commit()
        return data1,201
    
    @marshal_with(resource_field)
    def patch(self,data1_id):
        args=data1_add_args.parse_args()
        result=Data1Model.query.filter_by(id=data1_id).first()
        if not result:
           abort(404,message="ไม่พบข้อมูลที่จะแก้ไข")
        if args["name"]:
            result.name=args["name"]
        if args["title"]:
            result.title=args["title"]
        if args["imgurl"]:
            result.imgurl=args["imgurl"]

        db.session.commit()
        return result
    
    @marshal_with(resource_field)
    def delete(self,data1_id):
        result=Data1Model.query.filter_by(id=data1_id).first()
        db.session.delete(result)
        db.session.commit()

        return result
    
# #call
api.add_resource(Data1Test,"/api/<int:data1_id>")
api.add_resource(Data2Test,"/api")

if __name__ == "__main__":
    app.run(debug=True)