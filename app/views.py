from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse,Http404
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from PIL import Image
import cv2
from CloudAndGridREC.recognize import recognize
from .forms import LoginForm
# Create your views here.

def empty_view(request):
    return HttpResponseRedirect('/login/')

def login_view(request):

    form = LoginForm(request.POST or None)
    print("Login form created", request.POST, form.is_valid())
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('make_recognition', kwargs={}))
    return render(request, 'app/registration/login.html', {'form': form})



def logout_view(request):
   logout(request)
   return HttpResponseRedirect('/login/')

@login_required(login_url='/login/', redirect_field_name='/make_recognition/')
def make_recognition(request):
    image = cv2.imread("./CloudAndGridREC/images/emcka.jpg")
    image = recognize(image)
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    response = HttpResponse(content_type="image/jpeg")
    image.save(response, "JPEG")
    return response
