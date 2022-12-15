from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Entry
from django.urls import reverse
from django.shortcuts import get_object_or_404
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment_analysis(id):
   entry = get_object_or_404(Entry,pk=id)
   sid = SentimentIntensityAnalyzer()
   score = sid.polarity_scores(entry.text)
   return score    

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
    def formatday(self, day, entries):
        entries_per_day = entries.filter(date__day=day)
        d = ''
        for entry in entries_per_day:
            sent = sentiment_analysis(entry.id)
            sent = sent['compound']
            print(sent)
            if sent > 0.2:
                d += f'<li><a style="color: green !important" href="{reverse("detail", args=(entry.id,))}">{entry.title}</a></li>'
            elif sent < -0.2:
                d += f'<li><a style="color: red !important" href="{reverse("detail", args=(entry.id,))}">{entry.title}</a></li>'
            else:
                d += f'<li><a style="color: grey !important" href="{reverse("detail", args=(entry.id,))}">{entry.title}</a></li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

	# formats a week as a tr 
    def formatweek(self, theweek, entries):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, entries)
        return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
    def formatmonth(self, withyear=True):
        entries = Entry.objects.filter(date__year=self.year, date__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, entries)}\n'
        return cal
   