from django.db import models


# Create your models here.

class Question(models.Model):
	question_text = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text
		

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	choice_text = models.CharField(max_length = 200)
	# votes = models.IntegerField(default = 0)
	# voter_list = models.TextField(default = "")
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.choice_text

class Vote(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete = models.CASCADE)
	user = models.PositiveIntegerField(default = 0)
	pub_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.question.question_text