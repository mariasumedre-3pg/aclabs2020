from django.shortcuts import render
from django.http.response import HttpResponseRedirect

from todo.forms import TodoForm
from todo.models import Todo


def thanks(request):
    return render(request, "thanks")

# Create your views here.
def get_todo(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TodoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            Todo.objects.create(text=form.text, due_date=form.due_date, priority=form.priority)
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TodoForm()

    return render(request, 'todo.html', {'form': form})
