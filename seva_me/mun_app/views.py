from django.shortcuts import render
from django.http import HttpResponseRedirect
import smtplib
import json

def send_email(email,code,x_credit,curr_credit):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('alcom.mmt@gmail.com', 'nozmtpwwroptqkxn')
    subject = 'Code for complaint'
    body = 'The complaint with this code '+str(code)+" has been dealt with.\nYou got " + str(x_credit) + " credits and your current credit Bal. is "+str(curr_credit)+"."
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'alcom.mmt@gmail.com',
        email,
        msg
    )
    print("email has been sent")

def mun_main(request):
    with open("database/case_database.json") as f:
        case_db = json.load(f)
    new_case_db = {}
    lst = []
    for case in case_db:
        if case != "prev_code" and case_db[case]['status']!="Done":
            lst.append((case,case_db[case]['case_lvl']))
    lst.sort(key=lambda x: x[1],reverse=True)
    print(lst)
    for case in lst:
        new_case_db[case[0]] = case_db[case[0]]
    print(new_case_db)
    return render(request,"mun_main.html",{"cases":new_case_db})   

def chng_wrk(request,code):
    with open("database/case_database.json") as f:
        case_db = json.load(f)  
    case_db[str(code)]['status'] = "working"

    with open("database/case_database.json","w") as f:
        json.dump(case_db,f,indent=2)   

    return HttpResponseRedirect("/mun/")

def done(request,code):
    with open("database/case_database.json") as f:
        case_db = json.load(f) 
    with open("database/credit_database.json") as f:
        credit_db = json.load(f)  
 

    case_db[str(code)]['status'] = "Done"

    for user in case_db[str(code)]['user_rprt']:
        x_crdt = 50*float(case_db[str(code)]['case_lvl'])
        credit_db[user] = x_crdt + credit_db[user]
        send_email(user,code,x_crdt,credit_db[user])

    with open("database/case_database.json","w") as f:
        json.dump(case_db,f,indent=2)
    with open("database/credit_database.json","w") as f:
        json.dump(credit_db,f,indent=2)     

    return HttpResponseRedirect("/mun/")