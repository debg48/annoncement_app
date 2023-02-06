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
                if str(data['announce']).strip() == '' :
                    return JsonResponse({
                        "message": "Please Entered a valid announcement it cannot be blank",
                        "success" : False
                    })
                new_ann.announce=data['announce']
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

# read pages

class Read(APIView):
    def get(self,request,pk):
        token=request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({
                "message": "Authentication Failed!",
                "success" : False
            })
        try:
            list= []
            for i in range((10*(pk-1)),(((10*pk)+1))):
                try:
                    announce = Annoncement.objects.get(id=i)
                    list.append(announce.values())
                except: 
                    pass
            if list == [] :
                return JsonResponse({
                    "success" : False,
                    "message" : "No mathching request"
                })
            return JsonResponse({
                "success" : True,
                "Data" : list
            })
        except Exception as e : 
            return JsonResponse({
                "success" : False,
                "message" : str(e)
            })


# update status

class ChangeStatus(APIView):
    def post(self,request):

        token=request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({
                "message": "Authentication Failed!",
                "success" : False
            })
        try:
            data=request.data
            try:
                announce = Annoncement.objects.get(id=data['id'])
                if (announce.status == 'entered' and data['status']!='submitted'):
                    return JsonResponse({
                        "message" : "Only submitted status allowed for entered !",
                        "success" : False
                    })
                if (announce.status == 'published' and data['status']!='unpublished'):
                    return JsonResponse({
                        "message" : "Only unpublished status allowed for published !",
                        "success" : False
                    })
                if (announce.status == 'unpublished' and data['status']!='published'):
                    return JsonResponse({
                        "message" : "Only published status allowed for unpublished !",
                        "success" : False
                    })

                if ((announce.status == 'submitted' and data['status']!='accepted') and (announce.status == 'submitted' and data['status'] !='rejected') and (announce.status == 'submitted' and data['status'] !="published")):
                    return JsonResponse({
                        "message" : "Only published , accepted or rejected status allowed for submitted , please choose correct status !",
                        "success" : False
                    })
                announce.status=data['status']
                announce.save()
                return JsonResponse({"message": "status updated!",
                    "announcement" : announce.values()
                    })

            except Exception as e :
                return JsonResponse({
                    'message':str(e),
                    'success':False})
        except Exception as e :
            return JsonResponse({
                    'message': str(e),
                    'success':False
                })

# update announcement

class ChangeAnnonce(APIView):

    def post(self,request):

        token=request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({
                "message": "Authentication Failed!",
                "success" : False
            })
        try:
            data=request.data
            try:
                announce = Annoncement.objects.get(id=data['id'])
                if str(data['announce']).strip() == '' :
                    return JsonResponse({
                        "message": "Please Entered a valid announcement it cannot be blank",
                        "success" : False
                    })
                announce.announce=data['announce']
                announce.save()
                return JsonResponse({"message": "announcement updated!",
                    "announcement" : announce.values()
                    })

            except Exception as e :
                return JsonResponse({
                    'message':str(e),
                    'success':False})

        except Exception as e :
            return JsonResponse({
                    'message': str(e),
                    'success':False
                })

# api to delete an announcement

class Delete(APIView):
    def post(self,request):
        token=request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({
                "message": "Authentication Failed!",
                "success" : False
            })
        try:
            data=request.data
            try:
                announce = Annoncement.objects.get(id=data['id'])
                announce.delete()
                return JsonResponse({
                    'message':'Deletion Successful',
                    'success': True
                })
            except:
                return JsonResponse({
                    'message':'No match found !',
                    'success':False
                })
        except:
            return JsonResponse({
                    'message': "Please send valid response!",
                    'success':False
                })

# api to delete all anouncement

class DeleteAll(APIView):

    def get(self,request):

        token=request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({
                "message": "Authentication Failed!",
                "success" : False
            })
        try:
            announce = Annoncement.objects.all()
            announce.delete()
            return JsonResponse({
                'message':'Deletion Successful',
                'success': True
            })
        except Exception as e:
            return JsonResponse({
                'message':str(e),
                'success':False
            })

