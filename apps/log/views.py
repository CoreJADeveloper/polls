from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from apps.voting.models import Question, Choice, Vote
from django.http import HttpResponse
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from Crypto.Cipher import AES
# from urllib import quote

# Create your views here.

# @login_required(login_url="login/")
def home(request):
	if request.method == 'POST':
		current_user = request.user
		if current_user.is_authenticated:
			current_user_id = current_user.id
			question_id = request.POST.get('question-id')
			choice_id = request.POST.get('poll-choice')
			if not choice_id:
				return HttpResponse(
					"Select option",
					content_type="application/plain-text"
				)
			question_record = Question.objects.get(id = question_id)
			choice_record = Choice.objects.get(id = choice_id, question = question_id)
			# return HttpResponse(choice_id)
			if Vote.objects.filter(question = question_id, user = current_user_id).exists():
				return HttpResponse(
					"Exists",
					content_type="application/plain-text"
				)
			else:
				vote_record = Vote.objects.create(question = question_record, choice = choice_record)
				vote_record.user = current_user_id
				vote_record.save()
				return HttpResponse(
					"Success",
					content_type="application/plain-text"
				)
			# choice_votes = int(choice_record.votes) + 1
			# existing_voters = choice_record.voter_list
			# if existing_voters == '':
			# 	existing_voter_list = []
			# elif ',' in existing_voters:
			# 	existing_voter_list = existing_voters.split(',')
			# else:
			# 	existing_voter_list = [existing_voters]
			# if current_user_id in existing_voter_list:
			# 	return HttpResponse(
			# 		"Exists",
			# 		content_type="application/plain-text"
			# 	)
			# else:
			# 	if not existing_voter_list:
			# 		existing_voter_list.append(current_user_id)
			# 		current_voter_list = ','.join(map(str, existing_voter_list))
			# 	else:
			# 		current_voter_list = current_user_id
			# 	choice_record.votes = choice_votes
			# 	choice_record.voter_list = current_voter_list
			# 	choice_record.save()
				
			# 	return HttpResponse(
			# 		"Success",
			# 		content_type="application/plain-text"
			# 	)
		else:
			return HttpResponse(
				"User not authenticated",
				content_type="application/plain-text"
			)
	else:
		questions = Question.objects.all();
		votes = []
		# encrypted_ids = []
		question_text_url = []
		for question in questions:
			# encryption_obj = AES.new('abcdefghijklmnop')
			# plain_id = question.id
			# mismatch = len(plain) % 16
			# if mismatch != 0:
			# 	padding = (16 - mismatch) * ' '
			# 	plain += padding
			# ciph = encryption_obj.encrypt(plain_id)
			# quoted_ciph = quote(ciph)
			# encrypted_ids.append(quoted_ciph)
			question_text = question.question_text
			question_text_lower = question_text.lower().replace(" ", "-")
			question_text_lower = question_text_lower.replace('?', '')
			question_text_url.append(question_text_lower)
			# vote_summation_objects = Choice.objects.filter(question = question.id).aggregate(Sum('votes'))
			total_question_votes = Vote.objects.filter(question = question.id).count()
			votes.append(total_question_votes)
			# for vote_summation_object in vote_summation_objects.values():
			# 	votes.append(vote_summation_object)
		paginator = Paginator(questions, 10)
		page = request.GET.get('page')
		try:
			questions = paginator.page(page)
		except PageNotAnInteger:
			questions = paginator.page(1)
		except EmptyPage:
			questions = paginator.page(paginator.num_pages)
		compressed = zip(questions, votes, question_text_url)
		context = {'questions': questions, 'compressed': compressed}
		return render(request, "home.html", context)

def signup(request):
	current_user = request.user
	if current_user.is_authenticated:
		return redirect('/')
	return render(request, 'sign-up.html')

def create_user(request):
	user_name = request.POST.get('username', '')
	password = request.POST.get('password', '')
	mail = request.POST.get('email', '')
	if User.objects.filter(username = user_name).exists():
		context = "The user name already has been created"
	elif password and mail and user_name:
		user = User.objects.create_user(user_name, mail, password)
		user.save()
		login(request, user)
		context = "User has been successfully created"
	else:
		context = "There is a problem with creating the user"
	return render(request, 'create-user.html', {'context' : context})