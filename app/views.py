from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse,Http404
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from PIL import Image
import cv2
from CloudAndGridREC.recognize import recognize
from CloudAndGridREC.extract_embeddings import extract_embeddings
from CloudAndGridREC.train_model import train_model
import datetime
from .forms import LoginForm
from .models import Educator, Timetable, Student, Attendance
from django.shortcuts import get_object_or_404
import requests
import base64, numpy, json, io
from django.http import JsonResponse
import collections, ast
# Create your views here.


def empty_view(request):
    if request.user:
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'app/main_page/start_page.html', {'username': request.user.username})
    return HttpResponseRedirect('/login/')


def login_view(request):
    form = LoginForm(request.POST or None)
    print("Login form created", request.POST, form.is_valid())
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return render(request, 'app/main_page/start_page.html', {'username': user.username})
    return render(request, 'app/main_page/login.html', {'form': form})


def logout_view(request):
   logout(request)
   return HttpResponseRedirect('/login/')


@login_required(login_url='/login/', redirect_field_name='/make_recognition/')
def make_recognition(request):

    if request.method=="POST":
        dictionary = json.loads(request.body.decode('utf-8'))
        data = dictionary['image']
        #image = cv2.imread("./CloudAndGridREC/images/emcka.jpg")
        #image.save(response, "JPEG")

        format, imgstr = data.split(';base64,')
        file_bytes = base64.b64decode(imgstr)
        image = Image.open(io.BytesIO(file_bytes))
        print(image)
        image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        image, student_names, student_emotions = recognize(image)
        print(len(student_names))
        print(len(student_emotions))
        image = cv2.cvtColor(numpy.array(image), cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="JPEG")
        img_str = base64.b64encode(img_buffer.getvalue())

        response_data={}
        response_data['image']=img_str.decode('utf-8')
        response_data['student_dict'] = dict(zip(student_names, student_emotions))
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status':400, 'descr':'wrong http method'})



@login_required(login_url='/login/', redirect_field_name='/train/')
def extract_and_train(request):
    extract_embeddings()
    train_model()
    html = "<html><body>Extraction embeddings and training model done.</body></html>"
    return HttpResponse(html)



@login_required(login_url='/login/', redirect_field_name='/record/')
def record(request):
    if request.method=='GET':
        try:
            educator = Educator.objects.get(user=request.user)
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            link = 'https://timetable.spbu.ru/api/v1/educators/search/'+ str(request.user.last_name)
            response = requests.get(link).json()
            print(response)
            subjects = []
            intervals = []
            locations = []
            groups = []
            ids = []

            for e in response['Educators']:
                if e['FullName'] == (str(request.user.last_name) + " " + str(request.user.first_name) + " " + str(educator.middle_name)):
                    link = 'https://timetable.spbu.ru/api/v1/educators/'+ str( e['Id']) + '/events/2020-03-02/2020-03-03'
                    response = requests.get(link).json()
                    for EducatorEvents in response['EducatorEventsDays']:
                        day = EducatorEvents['DayString']
                        for dayEvent in EducatorEvents['DayStudyEvents']:
                            subjects.append(dayEvent['Subject'])
                            intervals.append(dayEvent['TimeIntervalString'])
                            locations.append(dayEvent['LocationsDisplayText'])
                            groups.append(dayEvent['ContingentUnitName'])
                            try:
                                timetable = get_object_or_404(Timetable,
                                                    group=dayEvent['ContingentUnitName'],
                                                    start=dayEvent['Start'],
                                                    end=dayEvent['End'],
                                                    subject=dayEvent['Subject'],
                                                    educator=educator)
                                ids.append(timetable.id)

                            except Http404:
                                timetable = Timetable(
                                    group=dayEvent['ContingentUnitName'],
                                    start=dayEvent['Start'],
                                    end=dayEvent['End'],
                                    subject=dayEvent['Subject'],
                                    educator=educator)
                                timetable.save()
                                ids.append(timetable.id)
                                print(timetable.id)

            return render(request, 'app/main_page/subjects_page.html', {'zip':zip(subjects, groups, intervals, locations, ids),
                                                                    'username': request.user.username,
                                                                    'day': day})
        except Educator.DoesNotExist:
            raise Http404("You are student and doesnt have such abilities")
    else:
        return Http404('Wrong Http method')

@login_required(login_url='/login/', redirect_field_name='/')
def rec(request):
    if request.method == 'GET':
        id = request.GET["id"]
        timetable = Timetable.objects.get(id=id)
        return render(request, "app/main_page/record_page.html",{'username': request.user.username,
                                                                 'subject':timetable.subject,
                                                                 'group':timetable.group,
                                                                 'lecturer':request.user.last_name + " " +
                                                                            request.user.first_name + " " +
                                                                            timetable.educator.middle_name,
                                                                 'start': timetable.start.replace('T',' '),
                                                                 'end': timetable.end.replace('T', ' ')})
    else:
        return Http404(request, "Wrong Http method")


def save(request):
    if request.method == "POST":
        dict = json.loads(request.body.decode('utf-8'))
        emo_dict = dict['emo_dict']
        print(emo_dict)
        id = dict['id']
        timetable = Timetable.objects.get(id=id)
        group = timetable.group
        groups = group.split(', ')
        print(groups)
        for gr in groups:
            students = Student.objects.filter(group=gr)
            for student in students:
                if str(student.id) in emo_dict.keys():
                    print('presented')
                    print(student.id)
                    try:
                        att = get_object_or_404(Attendance,timetable=timetable,student=student)
                        att.attended = True
                        att.emotion = str(emo_dict[str(student.id)])
                        att.save()
                    except Http404:
                        att = Attendance(timetable=timetable,student=student,attended=True, emotion=str(emo_dict[str(student.id)]))
                        att.save()
                else:
                    print('not presented:')
                    print(student.id)
                    try:
                        att = get_object_or_404(Attendance,timetable=timetable,student=student)
                        att.attended=False
                        att.emotion="{}"
                        att.save()
                    except Http404:
                        att = Attendance(timetable=timetable,student=student,attended=False,emotion="{}")
                        att.save()
        return HttpResponse(status=200)
    else:
        return Http404(request, "Wrong Http method")


def attendance(request):
    try:
        if request.method=='GET':
            student = Student.objects.get(user=request.user)
            timetables = Timetable.objects.filter(group__regex=r"" + str(student.group))
            dictinct_subjects = timetables.distinct('subject')
            subjects = []
            statistic = []
            dicts=[]

            for distinct_sub in dictinct_subjects:
                counter = collections.Counter()
                tmtbl = timetables.filter(subject=distinct_sub.subject)
                attendances = Attendance.objects.filter(timetable__in=list(tmtbl), student=student)
                if attendances.count() > 0:
                    arr = numpy.array(attendances.values_list('attended', flat=True))
                    count = numpy.sum(arr)
                    subjects.append(distinct_sub.subject)
                    statistic.append(str(count) + " / "+ str(len(arr)) )
                    for d in list(attendances.values_list('emotion', flat=True)):
                        counter.update(ast.literal_eval(d))
                    counter.update({'calm':0, 'anger':0, 'happiness':0, 'surprise':0, 'disgust':0, 'fear':0, 'sadness':0})
                    dicts.append(dict(counter))

            return render(request, "app/main_page/student_page.html",{'username':request.user.username,
                                                                      'zip':zip(subjects,statistic,dicts)})


    except Student.DoesNotExist:
        raise Http404("You are educator and doesnt have such abilities")

def statistic(request):
    try:
        if request.method == 'GET':
            educator=Educator.objects.get(user=request.user)
            timetables = Timetable.objects.filter(educator=educator)
            distinct_subjects = timetables.distinct('subject')
            ids = []
            sub_names=[]
            groups=[]
            for distinct_sub in distinct_subjects:
                ids.append(distinct_sub.id)
                sub_names.append(distinct_sub.subject)
                groups.append(distinct_sub.group)

            return render(request, "app/main_page/lecturer_page.html",{'username':request.user.username,
                                                                       'zip':zip(sub_names, groups, ids)})

    except Educator.DoesNotExist:
        raise Http404("You are student and doesnt have such abilities")

def stat2(request, id):
    try:
        if request.method == 'GET':
            educator=Educator.objects.get(user=request.user)
            timetable = Timetable.objects.get(id=id)
            subject = timetable.subject
            groups = timetable.group
            timetables = Timetable.objects.filter(subject=subject,group=groups,educator=educator)
            attendances = Attendance.objects.filter(timetable__in=list(timetables))
            dist_students = attendances.distinct('student')
            students=[]
            statistic = []
            dicts=[]
            for dist_stud in dist_students:
                counter = collections.Counter()
                stud_attends = attendances.filter(student=dist_stud.student)
                arr = numpy.array(stud_attends.values_list('attended', flat=True))
                count = numpy.sum(arr)
                students.append( dist_stud.student.group + " " + dist_stud.student.user.last_name + " " + dist_stud.student.user.first_name)
                statistic.append(str(count) + " / " + str(len(arr)) )
                for d in list(stud_attends.values_list('emotion', flat=True)):
                    counter.update(ast.literal_eval(d))
                counter.update(
                    {'calm': 0, 'anger': 0, 'happiness': 0, 'surprise': 0, 'disgust': 0, 'fear': 0, 'sadness': 0})
                dicts.append(dict(counter))

            if (len(students)<1):
                students=[('No records',' present in database for this subject')]
                statistic=['']
                dicts=['']
            return render(request, "app/main_page/lecturer_page2.html", {'username': request.user.username,
                                                                            'zip': zip(students,statistic,dicts)})
    except Educator.DoesNotExist:
        raise Http404("You are student and doesnt have such abilities")


def profile(request):
    if request.method=='GET':
        try:
            educator=Educator.objects.get(user=request.user)
            fio = request.user.last_name + " " + request.user.first_name + " " + educator.middle_name
            additional="Факультет: " + educator.departament +"Должность: " + educator.position
            return render(request, "app/main_page/profile.html", {'username': request.user.username,
                                                                  'fio': fio,
                                                                  'additional':additional,
                                                                  'email':request.user.email})
        except Educator.DoesNotExist:
            student=Student.objects.get(user=request.user)
            fio = request.user.last_name + " " + request.user.first_name + " " + student.middle_name
            additional = "Группа: "+ student.group  + \
                       " Год поступления : " + str(student.entry_year) + " Год выпуска: " + str(student.graduate_year) +""
            return render(request, "app/main_page/profile.html", {'username': request.user.username,
                                                                  'fio': fio,
                                                                  'additional': additional,
                                                                  'email': request.user.email})
