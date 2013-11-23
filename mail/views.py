from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import urllib2 as urllib

_from = "contact@nuvenote.com"
def url_data_to_dic(urldata):
    plain_txt = urllib.unquote(urldata)
    plain_list = plain_txt.split("&")
    r = {}
    for i in plain_list:
        t = i.split("=")
        r[t[0].strip()] = t[1].strip()
    return r

def render_email(context, template_name):
    template = loader.get_template(template_name)
    c = Context(context)
    return template.render(c)

def transactional_email(to, subject, context, email_type):
    template_name = 'emails/base.html'
    if(email_type =="new_enq"):
        template_name = "emails/new_check.html"
    elif (email_type == "new_registration"):
        template_name = "emails/new_registration.html"
    elif (email_type == "welcome"):
        template_name = "emails/welcome.html"
    elif (email_type == "resetpass"):
        template_name = "emails/reset.html"

    content = render_email(context, template_name)
    #TODO: make fail_silently=True after testing
    email = EmailMultiAlternatives(subject=subject, body="Nuve",from_email="Nuvenote <noreply@nuvenote.com>", to=to)
    email.attach_alternative(content, "text/html")
    email.send()
    #send_mail(subject=subject, message="test", from_email=_from, recipient_list=to, fail_silently=False, html_message=content) 

@csrf_exempt
def email(request):
    if request.method == "POST":
        #data = url_data_to_dic(request.body)
        #return HttpResponse(data)
        data = json.loads(request.body)
        _to = data['to']
        return HttpResponse(_to)
        _from = request.POST.get('from')
        _from = _from+"@facebook.com"
        _message = request.POST.get('message')
        send_mail("Help your friend", _message, _from, _to)
        return HttpResponse()
    return HttpResponse("Hi! Please go to <a href='http://bloodmates.co'>http://bloodmates.co</a>")
