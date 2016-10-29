from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

import sys
sys.path.insert(0, '../runebook')

from runebook import *

conn = RuneBookConnect(serverHost="175.126.112.130", userId="rune", userPw="fjsld89", userDb="rune_dev")

def index(request):
    return render(request, 'login.html', {})
    #return HttpResponse("Hello, world. You're at the polls index.")

def loginProc(request):
    cond = {"email": request.POST["email"], "password": request.POST["password"]}
    result = requests.post("http://175.126.112.130:8888/getAuth", json=cond)

    if result.text == 'None' or result is ():
        return redirect('index')

    userInfo = result[0]
    
    print(userInfo)

    if userInfo is () or userInfo is None:
        return redirect('index')

    request.session["userinfo"] = userInfo
    return redirect('project_list')
    #return HttpResponse("asdfasdf", status=200)

def userSignup(request):
    return render(request, 'user_signup.html', {})

def addUser(request):
    cond = {"email": request.POST["email"], "password": request.POST["password"]}
    result = requests.post("http://175.126.112.130:8888/addUser", json=cond)
    return redirect('index')

def projectList(request):
    userInfo = request.session["userinfo"]
    ret = conn.getProjectList(None, None, {"userid": userInfo[0]})
    
    return render(request, 'project_list.html', {"list": ret, "user": userInfo})

def addProjectProc(request):
    userInfo = request.session["userinfo"]
    if userInfo is () or userInfo is None:
        return redirect('index')

    projectName = request.POST["project_name"]

    if str(projectName).strip() == "":
        return redirect('project_list')

    project = RuneProject(userInfo[0], projectName)

    ret = conn.setProject(project)

    return redirect('project_list')

def removeProjectProc(request):
    userInfo = request.session["userinfo"]
    if userInfo is () or userInfo is None:
        return redirect('index')

def codeList(request):
    projectId = request.GET["project_id"]

    userInfo = request.session["userinfo"]
    if userInfo is () or userInfo is None:
        return redirect('index')

    ret = conn.getFunctionList(None, None, {"projectid": projectId})

    return render(request, 'code_list.html', {"list": ret, "user": request.session["userinfo"], "project_id": projectId})    

def setCode(request):
    userInfo = request.session["userinfo"]
    #project = conn.getProject({"id": request.GET["project_id"]})[0]

    codeData = None

    if "code_id" in  request.GET.keys():
        codeData = conn.getFunction({"id" : request.GET["code_id"]})[0]

    print("code_data", codeData)

    return render(request, 'code_form.html', {"code_data" : codeData, "project_id": request.GET["project_id"]})

def setCodeProc(request):
    userInfo = request.session["userinfo"]
    #project = conn.getProject({"id": request.GET["project_id"]})[0]

    name = request.POST["code_name"]
    code = str(request.POST["code_area"])
    projectId = request.POST["project_id"]

    codeId = None

    if "id" in request.POST.keys():
        codeId = request.POST["id"]

    codeData = None

    codeObject = RuneCode(projectId, name, code, None, codeId)

    if codeId != None:
        ret = conn.updateFunction({"id":codeId}, codeObject)
    else:
        ret = conn.setFunction(codeObject)

    return render(request, 'code_form_proc.html', {"ret": ret})
