from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from . models import Account , Annoncement
import jwt,datetime

#register

class Register(APIView):
    def post(self,request):
        try:
            data=request.data
            account=Account(email=data["email"],password=data["password"])
            account.save()
            return JsonResponse({
                "message": "Account Registered Successfully!",
                "success" : True
            })
        except Exception as e:
            return JsonResponse({
                "message": str(e),
                "success" : False
            })

#login

class Login(APIView):

    def post(self,request):
        try:
            data=request.data
            account=Account.objects.get(email=data['email'])
            if account is None:
                return JsonResponse({
                    "message" : "No matching account found",
                    "success" : False
                })
            if account.password != data["password"]:
                return JsonResponse({
                    "message" : "Incorrect Password !",
                    "success" : False
                })


            payload = {
                "email" : account.email,
                "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                "iat" : datetime.datetime.utcnow()
            }

            token = jwt.encode(payload,'secret',algorithm="HS256")

            response = JsonResponse({
                "message" : "Login Successfull",
                "success" : True
            })
            response.set_cookie(key='jwt',value=token,httponly=True)
            
            return response
        except Exception as e:
            return JsonResponse({
                "message": str(e),
                "success" : False
            })

#logout

class LogOut(APIView):
    def post(self,request):
        response=JsonResponse({
                "message" : "Logout Successfull",
                "success" : True
            })
        response.delete_cookie('jwt')

        return response

#create 

class Create(APIView):
    def post(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({
                "message": "Authentication Failed!",
                "success" : False
            })
        try: 
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
            try: 
                data=request.data
                new_ann = Annoncement()
                new_ann.announce=data['announce']
                if not (data['status']=='entered' or data['status']=='submitted'):
                    return JsonResponse({
                    "message": "Please Entered a valid status it can either be entred or submitted !",
                    "success" : False
                })
                if datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S.%f')<datetime.datetime.now() or datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S.%f')>=datetime.datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S.%f') or datetime.datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S.%f')<datetime.datetime.now() :
                        
                        return JsonResponse({
                            "message": "Invalid Start or End Date!",
                            "success" : False
                        })
                new_ann.start_time=datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S.%f')
                new_ann.end_time=datetime.datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S.%f')
                new_ann.creator=payload['email']
                new_ann.save()
                
                return JsonResponse({"values" :new_ann.values()})
            except:
                return JsonResponse({
                "message": "Invalid Request!",
                "success" : False
            })

        except:
            return JsonResponse({
                "message": "JWT signature expired!",
                "success" : False
            })

#read-all

class ReadAll(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({
                "message": "Authentication Failed!",
                "success" : False
            })

        try :
            announce = Annoncement.objects.all().values()
            return Response(announce)
        except Exception as e :
            return JsonResponse({
                "message" : str(e),
                "success" : False
            })

# update status

class ChangeStatus(APIView):
    pass