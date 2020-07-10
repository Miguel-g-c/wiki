from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from . import util

from random import choice

class SearchForm(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search encyclopedia'}))

class EntryForm(forms.Form):

    def __init__(self, *args,**kwargs):
        self.dis = kwargs.pop('dis', False)
        super(EntryForm, self).__init__(*args,**kwargs)
        self.fields['title']  = forms.CharField(label='Title', widget=forms.TextInput(attrs={
                                    'placeholder' : 'New entry title',
                                    'readonly'    : self.dis}))
        self.fields['content'] = forms.CharField(label='', widget=forms.Textarea(attrs={
                                    'placeholder' : 'Enter the Markdown content for the page',
                                    'style'       : 'height:500px;'}))


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries" : util.list_entries(),
        "form"    : SearchForm()
        })

def entry(request, title):

    entry = util.get_entry(title)

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title"   : title,
            "content" : util.MarkdownToHtml(entry),
            "form"    : SearchForm()
            })

    else:
        return redirect(reverse("encyclopedia:error", kwargs={
                "message" : "Error 404, page not found."
                }))

def error(request, message):

    return render(request, "encyclopedia/error.html", {
        "message" : message,
        "form"    : SearchForm()
        })

def search(request, query):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['q']
            return redirect(reverse("encyclopedia:search", kwargs={
                "query" : query
                }))
        else:
            return redirect(reverse("encyclopedia:error", kwargs={
                "message" : "Invalid search form, please try again"
                }))

    if query.lower() in map(str.lower, util.list_entries()):
        entry = util.get_entry(query)
        return redirect(reverse("encyclopedia:entry", kwargs={
            "title":query
            }))

    elif any(query.lower() in entry.lower() for entry in util.list_entries()):
        matches = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "matches" : matches,
            "form"    : SearchForm()
            })

    else:
        return redirect(reverse("encyclopedia:error", kwargs={
                "message" : 'Query did not match'
                }))

def create(request):

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title   = form.cleaned_data['title']
            if title.lower() in map(str.lower, util.list_entries()):
                return redirect(reverse("encyclopedia:error", kwargs={
                "message" : "Entry already exist, Try to edit it instead."
                }))
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect(reverse("encyclopedia:entry", kwargs={
                "title" : title
                }))
        else:
            return redirect(reverse("encyclopedia:error", kwargs={
                "message" : "Invalid new entry form, please try again"
                }))

    return render(request, "encyclopedia/create.html", {
        "form"  : SearchForm(),
        "form2" : EntryForm()
        })

def edit(request, title):

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title   = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect(reverse("encyclopedia:entry", kwargs={
                "title" : title
                }))
        else:
            return redirect(reverse("encyclopedia:error", kwargs={
                "message" : "Invalid edit entry form, please try again"
                }))

    entry = util.get_entry(title)

    if entry:
        return render(request, "encyclopedia/edit.html", {
            "title"   : title,
            "content" : util.MarkdownToHtml(entry),
            "form"    : SearchForm(),
            "form2"   : EntryForm(dis=True, initial={'title'   : title,
                                                      'content' : entry})
            })

    else:
        return redirect(reverse("encyclopedia:error", kwargs={
                "message" : "Error 404, page not found."
                }))

def random(request):
    return redirect(reverse("encyclopedia:entry", kwargs={
                "title" : choice(util.list_entries())
                }))
    
