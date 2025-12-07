from django.shortcuts import render, redirect
import requests
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

from TicketMaster.forms import FavouriteEventsForm
from TicketMaster.models import FavouriteEvent
from django.contrib import messages
from datetime import datetime, timedelta

import json
from django.http import JsonResponse


API_KEY = "0Lu4pGlOGCmVHCIQkX9JHWFXjgo74VEp"

def ticketmaster(request):
    genre = request.GET.get("genre", "").strip()
    city = request.GET.get("city", "").strip()
    events = []
    error = ""
    message = ""

    if request.GET:
        if not genre:
            error = "Search term cannot be empty. Please enter a genre!"
        elif not city:
            error = "City cannot be empty. Please enter a city!"
        else:
            url = "https://app.ticketmaster.com/discovery/v2/events.json"
            params = {"apikey": API_KEY, "keyword": genre, "city": city, "sort": "date,asc"}
            try:
                response = requests.get(url, params=params).json()
                raw_events = response.get("_embedded", {}).get("events", [])

                if request.user.is_authenticated:
                    user_favourites = FavouriteEvent.objects.filter(user=request.user)
                else:
                    user_favourites = []

                for e in raw_events:
                    date_raw = e.get("dates", {}).get("start", {}).get("dateTime")
                    formatted_date = ""
                    formatted_time = ""
                    if date_raw:
                        dt = datetime.fromisoformat(date_raw.replace("Z", "+00:00"))
                        dt_est = dt - timedelta(hours=5)
                        formatted_date = dt_est.strftime("%B %d, %Y")
                        formatted_time = dt_est.strftime("%I:%M %p EST")

                    venue = e["_embedded"]["venues"][0]
                    images = e.get("images", [])
                    images_url = ""
                    if images:
                        images_url = max(images, key=lambda img: img.get('width', 0) * img.get('height', 0)).get('url',"")

                    check_favourite = False
                    if request.user.is_authenticated:
                        check_favourite = user_favourites.filter(name=e.get("name"), date=formatted_date).exists()

                    events.append({
                        "name": e.get("name"),
                        "images": e.get("images", []),
                        "venue_name": venue.get("name"),
                        "address": venue.get("address", {}).get("line1"),
                        "city": venue.get("city", {}).get("name"),
                        "state": venue.get("state", {}).get("name"),
                        "date": formatted_date,
                        "time": formatted_time,
                        "images_url": images_url,
                        "url": e.get("url"),
                        "dt": dt,
                        "check_favourite": check_favourite
                    })

                if not events:
                    message = "Sorry...No results found for the entered search term and city."

            except Exception as e:
                error = "fail to get events."
                return render(request, "ticketmaster.html")

    context = {
        "events": events,
        "genre": genre,
        "city": city,
        "error": error,
        "message": message,
    }
    return render(request, "ticketmaster.html", context)

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('ticketmaster')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('ticketmaster')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('ticketmaster')



@login_required(login_url='login')
def add_favourite(request):
    if request.method == "POST" :
        event_name = request.POST.get("event_name", "")
        venue_name = request.POST.get("venue_name", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        event_date = request.POST.get("event_date", "")
        event_time = request.POST.get("event_time", "")
        event_url = request.POST.get("event_url", "")
        images_url = request.POST.get("images_url", "")

        if not FavouriteEvent.objects.filter(user=request.user, name=event_name, date=event_date).exists():
            FavouriteEvent.objects.create(
                user=request.user,
                name=event_name,
                venue=venue_name,
                city=city,
                state=state,
                url=event_url,
                date=event_date,
                time=event_time,
                images_url=images_url,
            )
            return JsonResponse({
                "added": "success",
                "message": "Event added."})
        else:
            return JsonResponse({
                "added": "info",
                "message": "Event already added."})

    return JsonResponse({
        "added": "error",
        "message": "Something went wrong."})


@login_required(login_url='login')
def display_favourite(request):
    favourites = FavouriteEvent.objects.filter(user=request.user)
    search_term = request.GET.get('search-term', '')
    if search_term:
        favourites = favourites.filter(name__icontains=search_term)
    return render(request, 'favourites.html', {'favourites': favourites, 'search_term': search_term })

@login_required(login_url='login')
def delete_favourite(request, event_id):
    event = FavouriteEvent.objects.get(id=event_id, user=request.user)
    if request.method == "POST":
        event.delete()
        return redirect('display_favourite')

    return render(request, 'delete.html', {'event': event})

@login_required(login_url='login')
def update_favourite(request, event_id):
    event = FavouriteEvent.objects.get(id=event_id, user=request.user)
    form = FavouriteEventsForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('display_favourite')
    else:
       form = FavouriteEventsForm(instance=event)
    return render(request, 'update.html', {'form': form, 'event': event})


@login_required(login_url='login')
def delete_event_with_ajax(request):
    if request.method == "POST":
        event_id = request.POST["event_id"]
        event = FavouriteEvent.objects.get(id=event_id,user=request.user)
        event.delete()
        return JsonResponse(
            {'deleted': True,
             'message': 'You deleted the item. Yay!'
             })

    return JsonResponse(
        {"message": "Something went wrong."})

