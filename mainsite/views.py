from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import urllib2 as urllib
from .models import Message


def url_data_to_dic(urldata):
    plain_txt = urllib.unquote(urldata)
    plain_list = plain_txt.split("&")
    r = {}
    for i in plain_list:
        t = i.split("=")
        r[t[0].strip()] = t[1].strip()
    return r

def possible_donner(re):
    if not re:
        return "" 
    elif(re == "o-"):
        return "O-"
    elif(re == "o+"):
        return "O-, O+"
    elif(re == "a-"):
        return "O-, A-"
    elif(re == "a+"):
        return "O-, A-, O+, A+"
    elif(re == "b-"):
        return "O-, B-"
    elif(re == "b+"):
        return "O-, B-, O+, B+"
    elif(re == "ab-"):
        return "O-, A-, B-, AB-"
    elif(re == "ab+"):
        return "O+, O-, A+, A-, B+, B-, AB+, AB-"
    else:
        return "" 

def index(request):
    return render(request,"index.html")

def product(request):
    return render(request,"product.html")

def generater(request):
    if request.method == "POST":
        print request.POST
        """URGENT! A Friend needs #blood in #Mumbai, #India. Matching #donors: O-, O+, A-, A+. Call +91 (22) 6615 3330. http://bit.ly/1bezcE0"""
        re = request.POST.get("options", "")+request.POST.get("part", "+")
        donner = possible_donner(re)
        message = """URGENT! A %s needs #blood in %s, %s. Matching #donors: %s. Call %s.""" % (request.POST.get("rel", "").title(), 
                                                                                               request.POST.get("city", "").title(), 
                                                                                               request.POST.get("country", "").title(),
                                                                                               donner,
                                                                                               #request.POST.get("part", "").title(),
                                                                                               request.POST.get("tel", "").title())
        return HttpResponse(message)

@csrf_exempt
def create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        form = data['form']
        form = url_data_to_dic(form)

        gmail = data['gmail']
        
        feed = gmail['feed']
        author = feed['author']
        author = author[0]['name']['$t']
        entry = feed['entry']
        #print entry[0]['gd$email'][0]['address']
        emails = []
        for e in entry:
            if(len(e)):
                if e.has_key('gd$email'):
                    p1 = e['gd$email']
                    if(len(p1)):
                        if(p1[0]['address']):
                            m = p1[0]['address']
                            emails.append(m)
        re = form["options"]+form["part"]
        donner = possible_donner(re)
        message = """URGENT! one of %s's %s needs #blood in #%s, #%s. Matching #donors: %s. Call %s.""" % (author, 
                                                                                                           form["rel"].title().replace("+", " "), 
                                                                                                           form["city"].title(), 
                                                                                                           form["country"].title(),
                                                                                                           donner,
                                                                                                           #request.POST.get("part", "").title(),
                                                                                                           form["tel"].title())

        
        m = Message(message = message)
        m.save()
        page_id = m.id
        #email = EmailMultiAlternatives(subject="Help", headers=_header, body=_message,from_email="lookingforblood@bloodmates.co", to=emails)
        #email.attach_alternative(_message, "text/html")
        #email.send()

        return HttpResponse(content = str(page_id))

def page(request):
    page_id = request.GET.get("page", None)
    message = Message.objects.get(id=page_id)
    return render(request, "message.html",{"message":message.message})

