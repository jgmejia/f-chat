# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json



def index(request):
    return render(request, 'index.html', {})

@login_required
def room(request, room_name):
    print('Request: =========> %s' %request.user)
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'user': request.user
    })
