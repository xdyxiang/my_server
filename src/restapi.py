from flask_restful import Resource,Api
from src.db_modle.petobj import Pet, Category,db
from flask import request,Blueprint


api_bp = Blueprint('api', __name__, url_prefix='/api')
restapi = Api(api_bp)


@restapi.resource('/pet')
class PetAPI(Resource):
    def get(self):
        """
        获取单只宠物的信息
        It works also with swag_from, schemas and spec_dict
        ---
        tags:
          - Pet
        parameters:
          - in: query
            name: pet_id
            type: string
        responses:
          200:
            description: "成功"
          201:
            description: "失败"
        """
        pet_id = request.args.get("pet_id")
        if pet_id:
            pet = Pet.query.filter_by(id=pet_id).first()
            if pet:
                clist = []
                for c in pet.category:
                    cdict = {"sx_name":c.sx_name,"sx_value":c.sx_value}
                    clist.append(cdict)
                result = {'code': 200, 'msg': "success","data":[{"id":pet.id,"name":pet.name,"photoUrls":pet.photoUrls,"status":pet.status,
                                                                      "task":pet.task,"category":clist}]}
            else:
                result = {'code': 202,'msg': '宠物不存在!'}
        else:
            petlist = Pet.query.all()
            if petlist:
                datalist = []
                for pet in petlist:
                    clist = []
                    for c in pet.category:
                        cdict = {"sx_name":c.sx_name,"sx_value":c.sx_value}
                        clist.append(cdict)
                    tempdata = {"id":pet.id,"name":pet.name,"photoUrls":pet.photoUrls,"status":pet.status,
                                                                          "task":pet.task,"category":clist}
                    datalist.append(tempdata)

                result = {'code': 200, 'msg': "success", "data":datalist}

            else:
                result = {'code': 202, 'msg': '宠物不存在!'}

        return result,200


    def post(self):
        """
        设置宠物信息
        It works also with swag_from, schemas and spec_dict
        ---
        tags:
          - Pet
        parameters:
          - in: "body"
            name: "body"
            description: "add pet这是一个body的描述"
            required: true
            schema:
              $ref: "#/definitions/Pet"
        definitions:
          Pet:
            type: "object"
            required:
              - "name"
              - "photoUrls"
            properties:
              category:
                type: "array"
                items:
                  type: "object"
                  properties:
                        sx_name:
                          type: "string"
                          example: "sx_name"
                        sx_value:
                          type: "string"
                          example: "sx_value"
              task:
                type: "string"
                example: "tasklaji"
              name:
                type: "string"
                example: "doggie"
              photoUrls:
                type: "string"
                example: "doggie"
              status:
                type: "string"
                description: "pet status in the store"
                enum:
                - "available"
                - "pending"
                - "sold"
        responses:
          200:
            description: "成功"
          201:
            description: "失败"
          400:
            description: "Invalid user supplied"
          404:
            description: "User not found"

        """
        reqdata = request.json
        if reqdata:
            pet = Pet(name=reqdata["name"],photoUrls=reqdata["photoUrls"],status=reqdata["status"],task=reqdata["task"])
            for c in reqdata["category"]:
                temc = Category(sx_name=c["sx_name"],sx_value=c["sx_value"])
                pet.category.append(temc)
            db.session.add(pet)
            db.session.commit()

            return {'code': 200,'msg': '数据添加成功'},200

        return {'code': 203,'msg': '校验提交的宠物数据！！'},200



    def delete(self):
        """
        删除宠物
        It works also with swag_from, schemas and spec_dict
        ---
        tags:
          - Pet
        parameters:
          - in: query
            name: pet_id
            type: string
            description: "修改一只宠物的信息"
            required: true
        responses:
          200:
            description: "成功"
          201:
            description: "失败"
          400:
            description: "Invalid user supplied"
          404:
            description: "User not found"

        """
        pet_id = request.args.get("pet_id")
        pet = Pet.query.filter_by(id=pet_id).first()
        if pet:
            db.session.delete(pet)
            db.session.commit()
            return {'code': 200, 'msg': '删除宠物成功!'}, 200
        else:
            return {'code': 202,'msg': '宠物不存在!'},200



    def put(self):
        """
        修改宠物
        It works also with swag_from, schemas and spec_dict
        ---
        tags:
          - Pet
        parameters:
          - in: query
            name: pet_id
            type: string
            required: true
          - in: body
            name: body
            type: string
            required: true
            schema:
              $ref: "#/definitions/Pet"
        definitions:
          Pet:
            type: "object"
            required:
              - "name"
              - "photoUrls"
            properties:
              category:
                type: "array"
                items:
                  type: "object"
                  properties:
                        sx_name:
                          type: "string"
                          example: "sx_name"
                        sx_value:
                          type: "string"
                          example: "sx_value"
              task:
                type: "string"
                example: "tasklaji"
              name:
                type: "string"
                example: "doggie"
              photoUrls:
                type: "string"
                example: "doggie"
              status:
                type: "string"
                description: "pet status in the store"
                enum:
                - "available"
                - "pending"
                - "sold"
        responses:
          200:
            description: "成功"
          201:
            description: "失败"
          400:
            description: "Invalid user supplied"
          404:
            description: "User not found"

        """
        reqdata = request.json
        petid = request.args.get("pet_id")
        if reqdata and petid:
            pet = Pet.query.filter_by(id=petid).first()
            if pet:
                pet.name=reqdata["name"]
                pet.photoUrls=reqdata["photoUrls"]
                pet.status=reqdata["status"]
                pet.task=reqdata["task"]
                pet.category.clear()
                if reqdata["category"]:
                    for c in reqdata["category"]:
                        temc = Category(sx_name=c["sx_name"], sx_value=c["sx_value"])
                        pet.category.append(temc)
                db.session.add(pet)
                db.session.commit()
                return {'code': 200,'msg': '修改宠物数据成功'},200
            else:
                return {'code': 202, 'msg': '宠物不存在！！'}, 200

        return {'code': 204,'msg': '请提交的宠物数据！！'},200

@restapi.resource('/username/<username>')
class Username(Resource):
    def get(self, username):
        """
        This examples uses FlaskRESTful Resource
        It works also with swag_from, schemas and spec_dict
        ---
        parameters:
          - in: path
            name: username
            type: string
            required: true
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
         """
        return {'username': username}, 200
