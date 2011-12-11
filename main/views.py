# Create your views here.
from main.models import Entrant
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import random

def submit(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    street = request.POST.get('street')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip = request.POST.get('zip')
    hint = request.POST.get('hint')
     
    if not (email and name):
        request.session['error'] = "We at least need your email address and name."
        return HttpResponseRedirect('/')

    try:
       entrant = Entrant.objects.get(email=email)
       request.session['error'] = "That email has already signed up."
       return HttpResponseRedirect('/')
    except Entrant.DoesNotExist:
       Entrant.objects.create(email=email, name=name, city=city, zip=zip, street=street, state=state, hint=hint)

    request.session['message']  = "That wasn't so hard eh? You can come back here later to see who else as signed up"
    return HttpResponseRedirect('/')

def processor(request):
    ret = {}
    error = request.session.get('error')
    message = request.session.get('message')
    if error:
       ret['error'] = error 
       del request.session['error']

    if message:
       ret['message'] = message
       del request.session['message']
    return ret


def make_matches():
   
    entrants = Entrant.objects.all()
    entrant_list = list(entrants)

    for entrant in entrants:
        cantget = entrant.cantget.all()
        left = [e for e in entrant_list if e.id !=entrant.id and e not in cantget]
        if not left:
            return make_matches()
        choice = random.choice(left)
        entrant_list.remove(choice)
        entrant.match = choice

    for entrant in entrants:
        entrant.save() 

def notify_entrants():

    entrants = Entrant.objects.all().select_related('match')
    for entrant in entrants: 
        match = entrant.match
        msg = """Alright, the results are in, here is your victim:

Name:    %(name)s
Address: %(street)s %(city)s, %(state)s %(zip)s

Here's what they said about what they want for christmas:

%(hint)s

        """ % {'name': match.name, 'street': match.street, 'city': match.city, 'state': match.state, 'zip': match.zip, 'hint': match.hint}
        send_mail('Secret Santa Results', msg, 'secretsanta@joelsemar.com', [entrant.email], fail_silently=True) 

