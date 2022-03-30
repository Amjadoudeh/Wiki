from audioop import reverse
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
	content= markdown(content)

	return render(request, "encyclopedia/entry.html",{
		"title":title,
		"content":content
		})

def create(request):
	if request.method =='POST':
		title=request.POST.get('title')
		content=request.POST.get('content')

		if not title or not content:
			return render(request,"encyclopedia/create.html", {
				"message": "Title or Content is missing. Please provide both."
				})

		if title in util.list_entries():
				return render(request,"encyclopedia/create.html", {
				"message": "Title is already feeded."
				})

		util.save_entry(title, content)
		return redirect("entry", title=title)
	return render(request, "encyclopedia/create.html")


def search(request):
	if request.method == 'GET':
		input = request.GET.get('q')
		entries = util.list_entries()
		search_pages = []
		for entry in entries:
			if input.upper() in entry.upper():
				search_pages.append(entry)
		for entry in entries:
			if input.upper() == entry.upper():
				return render(request, "encyclopedia/entry.html",{
					"entry": input, 
					"entryTitle": input
				})
			elif search_pages != []:
				return render(request, "encyclopedia/search.html",{
					"entries": search_pages
					})
			else:
				return render(request, "encyclopedia/nonExistingEntry.html",{
					"entryTitle": input
					})

def edit(request, title):
	content=util.get_entry(title)
	if request.method=='POST':
		content = request.POST.get("content")
		title=request.POST.get("title")
		util.save_entry(title, content)
		return redirect("entry", title=title)
	return render(request, "encyclopedia/edit.html",{
		"title": title,
		"content": content
		})

def random(request):
	entries=util.list_entries()
	rand_entry = entries[randint(0, len(entries)-1)]
	return redirect('entry', title=rand_entry)