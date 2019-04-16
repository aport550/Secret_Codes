from django.db import models

#lack of common sense username and password limits make this susceptible to overflows
class User(models.Model):
	username = models.CharField(max_length=1000)
	password = models.CharField(max_length=1000)
	secret = models.TextField()

class Hint(models.Model):
	username = models.CharField(max_length=1000)
	hint = models.TextField()
	
def __str__(self):
	return self.username



