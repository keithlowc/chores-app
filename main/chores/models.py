from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class ChorePoints(models.Model):
	points = models.DecimalField(decimal_places=2,max_digits=3)
	content = models.CharField(max_length=100)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.content

	def get_absolute_url(self):
		return reverse('chores-all')
		# return reverse('chores-post', kwargs={'pk':self.pk})

