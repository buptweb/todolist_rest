from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie

# Create your views here.
from .models import Todo
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, TodoSerializer
from rest_framework import permissions

@login_required
@ensure_csrf_cookie
def index(request):
    return render(request,"index.html")


@login_required
@ensure_csrf_cookie
def index_angular(request):
    return render(request,"index_angular.html")


class TodoViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def create(self, request):
        request.data['user'] = request.user.id
        serialized = TodoSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
        return Response({"success":"true"})

    def partial_update(self, request, pk=None):
        todo = Todo.objects.get(pk=pk)
        serialized = TodoSerializer(todo, data=request.data, partial=True)
        if serialized.is_valid():
            serialized.save()
        return Response({"success":"true"})

    def destroy(self, request, pk=None):
        Todo.objects.get(pk=pk).delete()
        return Response({"success": "true"})



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

def mylogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect("/")
        else:
            errmsg = "用户名/密码输入错误"
        return render(request, 'login.html',{'errmsg':errmsg})
    else:
        return render(request, 'login.html',{'errmsg':""})


@login_required
def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username = username).exists():
            user = User.objects.create_user(username, '',password)
            user.save()
            return HttpResponseRedirect('/login/')
        else:
            errmsg = "该用户名已被注册"
            return render(request, 'register.html',{'errmsg':errmsg})
    else:
        return render(request, 'register.html', {'errmsg': ""})
