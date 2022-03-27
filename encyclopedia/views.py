from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from markdown2 import markdown
from random import randint
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
	content=util.get_entry(title)
	if not content:
		content="this does not exist"

	#from markdown to html
	content=markdown(content)

	return render(request, "encyclopedia/entry.html",{
		"title":title,
		"content":content
		})