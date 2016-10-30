from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

import sys
import requests
import json
import datetime

sys.path.insert(0, '../runebook')

from runebook import *

SENTINELHOST = "175.126.112.130:8888"

def index(request):
    return render(request, 'login.html', {})
    #return HttpResponse("Hello, world. You're at the polls index.")

def loginProc(request):
    cond = {"email": request.POST["email"], "password": request.POST["password"]}
    result = requests.post("http://"+SENTINELHOST+"/getAuth", json=cond)

    if result.text == 'None' or result is ():
        return redirect('index')

    userInfo = result.json()
    
    print(userInfo)

    if userInfo is () or userInfo is None:
        return redirect('index')

    request.session["userinfo"] = userInfo
    return redirect('project_list')

def userSignup(request):
    return render(request, 'user_signup.html', {})

def addUser(request):
    cond = {"email": request.POST["email"], "password": request.POST["password"]}
    result = requests.post("http://"+SENTINELHOST+"/addUser", json=cond)
    return redirect('index')

def projectList(request):
    userInfo = request.session["userinfo"]
    cond = {"user_id": userInfo[0]}
    ret = requests.post("http://"+SENTINELHOST+"/getProjectList", json=cond)
    print(ret.json())
    return render(request, 'project_list.html', {"list": ret.json(), "user": userInfo})

def addProjectProc(request):
    userInfo = request.session["userinfo"]
    if userInfo is () or userInfo is None:
        return redirect('index')

    projectName = request.POST["project_name"]
    cond = {"user_id": userInfo[0], "project_name": projectName}

    if str(projectName).strip() == "":
        return redirect('project_list')

    ret = requests.post("http://"+SENTINELHOST+"/addProject", json=cond)
    
    return redirect('project_list')

def removeProjectProc(request):
    userInfo = request.session["userinfo"]
    if userInfo is () or userInfo is None:
        return redirect('index')
    userid = request.GET["userid"]
    name = request.GET["name"]
    print(userid)
    print(name)
    cond = {"user_id": userid, "name": name}
    ret = requests.post("http://"+SENTINELHOST+"/removeProject", json=cond)
    return redirect('project_list')

def removeCodeProc(request):
    userInfo = request.session["userinfo"]
    if userInfo is () or userInfo is None:
        return redirect('index')
    id = request.GET["id"]
    project_id = request.GET["project_id"]
    name = request.GET["name"]
    print(id)
    print(project_id)
    print(name)
    cond = {"id": id, "project_id": project_id, "name": name}
    ret = requests.post("http://"+SENTINELHOST+"/removeFunction", json=cond)
    return redirect('project_list')

def codeList(request):
    projectId = request.GET["project_id"]

    userInfo = request.session["userinfo"]
    if userInfo is () or userInfo is None:
        return redirect('index')

    cond = {"project_id": projectId}
    print(cond)
    ret = requests.post("http://"+SENTINELHOST+"/getFunctionList", json=cond)

    retObject = ret.json()

    for item in retObject:
        if item[4] is None:
            item[4] = None
            item[4] = datetime.datetime.now()
        else:
            ts = item[4]
            item[4] = None
            item[4] = datetime.datetime.fromtimestamp(ts)

    return render(request, 'code_list.html', {"list": retObject, "user": request.session["userinfo"], "project_id": projectId})    

def setCode(request):
    userInfo = request.session["userinfo"]

    codeData = None
    print(codeData)
    if "code_id" in  request.GET.keys():
        cond = {"code_id": request.GET["code_id"]}
        codeData = requests.post("http://"+SENTINELHOST+"/getFunction", json=cond)
        codeData = codeData.json()
    print(codeData)
    return render(request, 'code_form.html', {"code_data" : codeData, "project_id": request.GET["project_id"]})

def setCodeProc(request):
    userInfo = request.session["userinfo"]

    codeName = request.POST["code_name"]
    codeArea = str(request.POST["code_area"])
    projectId = request.POST["project_id"]

    codeId = None

    if "id" in request.POST.keys():
        codeId = request.POST["id"]

    print(codeId)
    codeData = None

    codeObject = RuneCode(projectId, codeName, codeArea, None, codeId)
    #codeObject = RuneCode(projectId, codeArea, None, codeId)

    if codeId != None:
        cond = {"code_id": codeId, "project_id": projectId, "code_name": codeName, "code_area": codeArea}
        ret = requests.post("http://"+SENTINELHOST+"/updateFunction", json=cond)
    else:
        cond = {"project_id": projectId, "code_name": codeName, "code_area": codeArea}
        ret = requests.post("http://"+SENTINELHOST+"/addFunction", json=cond)

    return render(request, 'code_form_proc.html', {"ret": ret})
