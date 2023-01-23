from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
# Create your views here.
from .models import Entry
import datetime
from .forms import EntryForm
from .utils import Calendar, sentiment_analysis
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView

from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


client_id='865dd348f96a475ebf08eb27eb5cbef2'
client_secret='7fa3127674e04edb815b769d3ce7a211'
redirect_url='http://127.0.0.1:8080/callback/'


current_datetime = datetime.datetime.now()

def detail(request, id):
    entry = get_object_or_404(Entry,pk=id)
    ss = sentiment_analysis(entry.id)
    scope = "user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret= client_secret, redirect_uri=redirect_url, scope=scope))
    results = sp.current_user_top_tracks(limit=10, time_range='short_term')
    tracks = results['items']
    track_ids = [track['id'] for track in tracks]
    features = sp.audio_features(tracks=track_ids)
    valences = [feature['valence'] for feature in features]
    tracks_valences = zip(tracks, valences)
        
    return render(request, "entries/detail.html", {"entry": entry, "ss": ss, "tracks_valences": tracks_valences})

def music_stuff(request):
    scope = "user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret= client_secret, redirect_uri=redirect_url, scope=scope))
    short_term_top_tracks = (sp.current_user_top_tracks(limit=10, time_range='short_term'))['items']
    short_term_track_ids = [track['id'] for track in short_term_top_tracks]
    short_term_features = sp.audio_features(tracks=short_term_track_ids)
    short_term_tracks_features = zip(short_term_top_tracks, short_term_features)

    medium_term_top_tracks = sp.current_user_top_tracks(limit=10, time_range='medium_term')
    long_term_top_tracks = sp.current_user_top_tracks(limit=10, time_range='long_term')
    short_term_top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')
    medium_term_top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')
    long_term_top_artists = sp.current_user_top_artists(limit=10, time_range='long_term')
    musical_key_dictionary = {0:"C", 1:"C#",2:"D",3:"D#",4:"E",5:"F",6:"F#",7:"G",8:"G#",9:"A", 10:"A#", 11:"B"}
    context = {
        "short_term_tracks_features": short_term_tracks_features,
        "short_term_tracks": short_term_top_tracks,
        "medium_term_tracks": medium_term_top_tracks['items'],
        "long_term_tracks": long_term_top_tracks['items'],
        "short_term_artists": short_term_top_artists['items'],
        "medium_term_artists": medium_term_top_artists['items'],
        "long_term_artists": long_term_top_artists['items'],
        "short_term_track_keys": musical_key_dictionary,


    }
    return render(request, "entries/music.html", context)

def entries_list(request, page):
    entries = Entry.objects.all().order_by("date")
    page = request.GET.get('page', 1)
    paginator = Paginator(entries, per_page=3)
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)
   
   
    return render(request, "entries/entries_list.html", {"entries": entries})

def new(request):
    if request.method == "POST":
        # form has been submitted, process data
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("welcome")
    else:
        form = EntryForm(initial={"date": current_datetime})
    return render(request, "entries/new.html", {"form": form})

# class EditEntryView(UpdateView):
#     model = Entry
#     template_name = "edit.html"
#     fields = ['title','text','tags']

def edit(request, id):
    entry = Entry.objects.get(pk=id)
    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("welcome")
    else:
        form = EntryForm(instance=entry)
    return render(request, "entries/edit.html", {"entry": entry, "form": form})

def delete(request, id):
    entry = Entry.objects.get(pk=id)
    if request.method == "POST":
        entry.delete()
        return redirect("welcome")
    return render(request, "entries/entry_delete.html", {"entry": entry})



def calendar_view(request):
    query = request.GET.get('query')
    initial_year = current_datetime.year
    initial_month = current_datetime.month
    default_year = request.session.get('year_counter',initial_year)
    default_month = request.session.get('month_counter', initial_month)
    if request.session.get('year_counter') is None:
        request.session['month_counter'] = default_month
        request.session['year_counter'] = default_year


    def calendar_update(year, month):
        request.session['month_counter'] = month
        request.session['year_counter'] = year
        #Old simple calendar
        #cal = HTMLCalendar().formatmonth(year, month)
        #d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        first_cal = Calendar(request.session['year_counter'], request.session['month_counter'])

        # Call the formatmonth method, which returns our calendar as a table
        cal = first_cal.formatmonth(withyear=True)
        return cal
    #Query for previous page link will -1 from month counter unless it is the first month
    if query=='minus':
        if request.session["month_counter"] == 1:
            request.session["month_counter"] = 12
            request.session["year_counter"] -= 1
        else:
            request.session["month_counter"] -= 1
        calendar_update(request.session['year_counter'], request.session['month_counter'])
        return redirect('calendar')
#Query for next page will +1 to month counter unless it is last month
    if query=='plus':
        print(request.session["month_counter"])
        if request.session["month_counter"] == 12:
            request.session["month_counter"] = 1
            request.session["year_counter"] += 1
        else:
            request.session["month_counter"] += 1
        calendar_update(request.session['year_counter'], request.session['month_counter'])
        return redirect('calendar')

#Resets using current datetime if user wants to return to current month
    if query=='current' or query=='':
        request.session["month_counter"] = initial_month
        request.session["year_counter"] = initial_year
        calendar_update(request.session['year_counter'], request.session['month_counter'])
        return redirect('calendar')
    #Standar calendar rendering
    #calendar_update(initial_year, initial_month)
    return render(request, "entries/calendar.html", {"cal": calendar_update(request.session['year_counter'], request.session['month_counter'])})