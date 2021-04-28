from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from pytz import timezone
import random, pytz


# Create your views here.
def index(request):
    if "gold" not in request.session or "activities" not in request.session:
        request.session['gold'] = 0
        request.session['activities'] = []
    context = {
        'activities' : request.session['activities']
    }
    if 'count' not in request.session:
        request.session['count'] = 0
    else:
        request.session['count'] += 1
        
    return render(request, "index.html", context)

def refresh(request):
    request.session.flush()
    return redirect('/')

def process_money(request):
    if request.method == "POST":
        myGold = request.session['gold']
        activities = request.session['activities']
        location = request.POST['location']
        if location == 'farm':
            goldThisTurn = round(random.random() * 10 + 10)
        elif location == 'cave':
            goldThisTurn = round(random.random() * 5 + 5)
        elif location == 'house':
            goldThisTurn = round(random.random() * 3 + 2)
        else:
            winLose = round(random.random())
            if winLose == 1:
                goldThisTurn = round(random.random() * 50)
            else:
                goldThisTurn = (round(random.random() * 50) * -1)

        myGold += goldThisTurn
        request.session['gold'] = myGold

        date_format='%m/%d/%Y %H:%M:%S %Z'
        date = datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Pacific'))
        myTime = date.strftime(date_format)

        if goldThisTurn >= 0:
            str = f"Earned {goldThisTurn} from the {location}  ({myTime})"
        else:
            goldThisTurn *= -1
            str = f"Lost {goldThisTurn} from the {location}  ({myTime})"
        activities.insert(0, str)
        request.session['activities'] = activities
    return redirect('/')