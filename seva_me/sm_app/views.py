from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import json
import smtplib
import os


def send_email(email,code):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('alcom.mmt@gmail.com', 'nozmtpwwroptqkxn')
    subject = 'Code for complaint'
    body = 'The code for your complaint you recently placed is '+str(code)+". \nYou can check the status using this code."
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'alcom.mmt@gmail.com',
        email,
        msg
    )
    print("email has been sent")



def main(request):
    return render(request,"main.html")


def ping(request):
    return render(request,"ping.html")

def check(request):
    return render(request,"check.html")

def create(request):
    loc = request.GET.get('check_this',None)
    print(loc)
    image_file = request.FILES['image']
    fs = FileSystemStorage()
    fs.save(image_file.name,image_file)

    tag_priority = {"electricity":1,"pot-hole":0.8,"sewage":0.7,"waste-m":0.7,"traff-flw":0.6,"saf-sec":0.6,"public-pd":0.5,"other":0.3}
    email = request.POST['email']
    tag = request.POST['issue']

    print(tag)

    with open("database/case_database.json") as f:
        case_db = json.load(f)
    with open("database/credit_database.json") as f:
        credit_db = json.load(f)

    case_ext = False
    case_code = ""

    for case in case_db:
        if case != "prev_code" and case_db[case]["tag"] == tag:
            case_code = case
            case_ext = True

    if case_ext:
        if email not in case_db[case_code]["user_rprt"]:
            case_db[case_code]["user_rprt"].append(email)
            case_db[case_code]["case_lvl"] += tag_priority[tag]
            reported = False
        else:
            reported = True
    else:
        case_code = case_db["prev_code"] + 1
        case_db["prev_code"] += 1
        file_name = os.listdir("media")[0]
        new_file_name = "database/case_image/"+str(case_code)+".png"
        os.rename("media/"+file_name,new_file_name)
        case_file = {
            "image":new_file_name,
            "location": "",
            "tag": tag,
            "case_lvl": tag_priority[tag],
            "status": "Received",
            "user_rprt": [email]
        }
        case_db[case_code] = case_file

    send_email(email,case_code)
    credit_db[email] = credit_db.get(email,0)

    with open("database/case_database.json","w") as f:
        json.dump(case_db,f,indent=2)
    with open("database/credit_database.json","w") as f:
        json.dump(credit_db,f,indent=2)


    return render(request,"tick.html")

def status(request):
    code = request.POST['case']
    with open("database/case_database.json") as f:
        case_db = json.load(f)
    status = case_db[str(code)]['status']
    curr_lvl = case_db[str(code)]['case_lvl']

    return render(request,"status.html",{"code":code,"status":status,"curr_lvl":curr_lvl})
