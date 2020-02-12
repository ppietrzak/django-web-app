from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({NAME}))")
    stuff_for_frontend = {'search_result': search_result} # context dictionary
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

# yourapp.com

def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://www.uh.edu/pharmacy/_images/directory-staff/no-image-available.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.insert(data)
            # notify on create
            messages.success(request, 'New movie added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error when trying to create a movie: {}'.format(e))
    return redirect('/')

def edit(request, movie_id):
    if request.method == 'POST':
       data = {
           'Name': request.POST.get('name'),
           'Pictures': [{'url': request.POST.get('url') or 'https://www.uh.edu/pharmacy/_images/directory-staff/no-image-available.jpg'}],
           'Rating': int(request.POST.get('rating')),
           'Notes': request.POST.get('notes')
       }
       try:
            response = AT.update(movie_id, data)
            # notify on update
            messages.success(request, 'Update movie: {}'.format(response['fields'].get('Name')))
       except Exception as e:
            messages.warning(request, 'Got an error when trying to update a movie: {}'.format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        response = AT.delete(movie_id)
        # notify on delete
        messages.warning(request, 'Deleted movie: {}'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'Got an error when trying to delete a movie: {}'.format(e))
    return redirect('/')

