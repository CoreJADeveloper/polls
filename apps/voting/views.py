from django.shortcuts import render
from django.http import HttpResponse
from apps.voting.models import Question, Choice, Vote
from django.shortcuts import get_object_or_404
import datetime
from django.db.models import Q
import json

# Create your views here.

def process_vote(request):
	if request.method == 'POST':
		question_id = request.POST.get('question-id')
		choice_id = request.POST.get('poll-choice')

		question_record = Question.objects.get(id = question_id)
		choice_record = Choice.objects.get(question = question_id)
		choice_votes = int(choice_record.votes) + 1;
		print(choice_votes)
		choice_record.votes = choice_votes
		choice_record.save()
		
		return HttpResponse(
			"Success"
		)
	else:
		return HttpResponse(
			"Failed"
		)

def question_details(request, question_id, question_text):
	today = datetime.datetime.now()
	current_year = today.year
	question_object = Question.objects.get(id = question_id)
	question_text_record = question_object.question_text
	
	question_text_record = question_text_record.lower().replace(" ", "-")
	question_text_record = question_text_record.replace('?', '')
	question_record = Question.objects.get(id = question_id)
	choice_records = Choice.objects.filter(question = question_record)
	# vote_records = Vote.objects.filter(question = question_record, pub_date__year = current_year).values_list('pub_date', flat = True)
	vote_records = Vote.objects.filter(question = question_record, pub_date__year = current_year)
	choice_ids = []
	choice_texts = {}
	all_months_votes = {}
	for record in choice_records:
		choice_ids.append(record.id)
		choice_texts[record.id] = record.choice_text
		all_months_votes[record.id] = {}
	for record in vote_records:
		choice_record = record.choice
		choice_record_id = choice_record.id
		date_object = record.pub_date
		if date_object.month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] and choice_record_id in all_months_votes and date_object.month in all_months_votes[choice_record_id]:
			all_months_votes[choice_record_id][date_object.month] = all_months_votes[choice_record_id][date_object.month] + 1
		else:
			all_months_votes[choice_record_id][date_object.month] = 1
	for key, value in all_months_votes.items():
		choices_month_list = value
		for index in range(1, 13):
			if not index in choices_month_list:
				all_months_votes[key][index] = 0	
		
	if question_text_record == question_text:
		# question = Question.objects.get(id = question_id)
		choices = Choice.objects.filter(question = question_id)
		context = {"question": question_record, "choices": choices, "vote_records": json.dumps(all_months_votes), "choice_texts": json.dumps(choice_texts)}
		return render(request, "details.html", context)
	else:
		return render(request, "404.html", context)

def month_in(year, months, field='pub_date'):
    q = Q(**{field + '__year': year})
    for m in months:
       q |= Q(**{field + '__month': m})
    return q