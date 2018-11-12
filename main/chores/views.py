from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ChorePoints
from .serializers import UserSerializer

'''
choresData needs to inherit Api view since the data has to be loaded from the rest api

urls should be as follow 

path('chores/', views.get_chores, name='chores'),
path('api/chores/data', ChoresData.as_view(), name='chores-endpoint'),

api/chores/data - is where we get the data from in the url-endpoint on our html
'''


## to delete ChorePoints.objects.all().delete()

# User = get_user_model()

# ************************************************************

def about(request):
    return render(request, 'chores/about.html')

class ChoresCreateView(LoginRequiredMixin, CreateView):
    model = ChorePoints
    template_name = 'chores/chore_points.html'
    context_object_name = 'form'
    fields = ['points','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        calculations = Calculations()
        user_points = calculations.calculate_points(self.request.user.username)

        context = super(ChoresCreateView, self).get_context_data(**kwargs)
        context['points'] = user_points
        return context


class ChorePostListView(LoginRequiredMixin,ListView):
    model = ChorePoints
    template_name = 'chores/chore_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

class ChorePostDetailedView(LoginRequiredMixin,ListView):
    model = ChorePoints
    template_name = 'chores/chore_post_detail.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username= self.kwargs.get('username'))
        queryset = ChorePoints.objects.filter(author=user).order_by('-date_posted')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ChorePostDetailedView, self).get_context_data(**kwargs)
        calculations = Calculations()
        user_points = calculations.calculate_points(self.kwargs.get('username'))

        context['points'] = user_points
        context['current_user'] = self.kwargs.get('username')
        return context

# ************************************************************ 

class ChoresView(View):
    def get(self,request):
        users = DataCollection()
        labels = users.get_users_names()
        default_items, next_person, dic = users.next_to_chore()

        return render(request, 'chores/chores.html', {'next': next_person, 'labels': labels ,'points': dic})

class ChoresData(APIView):	
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, format=None):
        users = DataCollection()
        labels = users.get_users_names()
        default_items, next_person, dic = users.next_to_chore()

        data = {
    		'labels': labels,'default': default_items, 'Next_to_wash': next_person, 'Hash map': dic,
    	}
        return Response(data)

# ************************************************************ 

class DataCollection:
    def get_users_names(self):
        # Returns list format of current users
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        labels = []
        for i in range(len(serializer.data)):
            labels.append(serializer.data[i]['username'])
        return labels

    def next_to_chore(self):
        calculations_object = Calculations()
        users = DataCollection()
        labels = users.get_users_names()

        default_items = []
        for names in labels:
            points = calculations_object.calculate_points(names)
            default_items.append(points)

        dic = dict()
        for points, names in zip(default_items,labels):
            dic[names] = points

        min_value = calculations_object.calculate_min_points(default_items)
        next_person = calculations_object.find_next(min_value,labels,default_items)

        return default_items, next_person, dic


class Calculations:
    def calculate_points(self,username):
    	chore_points = ChorePoints.objects.filter(author__username=username)
    	points = 0
    	for chore in chore_points:
    		points += chore.points

    	return points

    def calculate_min_points(self,array):
        minimum = 999
        for x in array:
            if x < minimum:
                minimum = x
        return minimum

    def find_next(self,min_value,labels,default_items):
        dic = dict()
        for lab, points in zip(labels,default_items):
            dic[lab] = points 

        next_person = 'none'

        for key,value in dic.items():
            if value == min_value:
                next_person = key

        return next_person




