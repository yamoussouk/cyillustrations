from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
import datetime
from . import settings

from .models import Question, Survey, Category, Response, AnswerBase, AnswerText, AnswerRadio, AnswerSelect, AnswerSelectMultiple, AnswerInteger, AnswerRange, QuestionImage
from .forms import ResponseForm


def Index(request):
	return render(request, 'index.html')

def SurveyDetail(request, id):
	survey = Survey.objects.get(id=id)
	category_items = Category.objects.filter(survey=survey)
	categories = [c.name for c in category_items]
	if request.method == 'POST':
		form = ResponseForm(request.POST, survey=survey)
		if form.is_valid():
			response = form.save()
			return HttpResponseRedirect("/confirm/%s" % response.interview_uuid)
	else:
		form = ResponseForm(survey=survey)
		# TODO sort by category
	return render(request, 'survey.html', {'response_form': form, 'survey': survey})

def Confirm(request, uuid):
	email = settings.support_email
	return render(request, 'confirm.html', {'uuid':uuid, "email": email})

def privacy(request):
	return render(request, 'privacy.html')

@staff_member_required
def admin_response_detail(request, response_id):
	model = []
	response = get_object_or_404(Response, id=response_id)
	# for a in answer_text:
	# 	print(a.question.id)
	answer_text = AnswerText.objects.filter(response=response)
	answer_radio = AnswerRadio.objects.filter(response=response)
	answer_select = AnswerSelect.objects.filter(response=response)
	answer_select_multiple = AnswerSelectMultiple.objects.filter(response=response)
	answer_integer = AnswerInteger.objects.filter(response=response)
	answer_range = AnswerRange.objects.filter(response=response)
	for a in answer_text:
		question = Question.objects.filter(pk=a.question.id)
		choices = [c[0] for c in question[0].get_choices() if c[0] != '']
		model.append({'question': a.question, 'answer': a.answer, 'choices': choices})
	for a in answer_radio:
		question = Question.objects.filter(pk=a.question.id)
		question_image = QuestionImage.objects.filter(question=a.question.id)
		choices = [c[0] for c in question[0].get_choices() if c[0] != '']
		choice_index = [idx for idx, e in enumerate(choices) if e == a.answer][0]
		if len(question_image) > 0:
			model.append({'question': a.question, 'answer': a.answer, 'choices': choices, 'image': question_image[choice_index]})
		else:
			model.append({'question': a.question, 'answer': a.answer, 'choices': choices})
	for a in answer_select:
		question = Question.objects.filter(pk=a.question.id)
		choices = [c[0] for c in question[0].get_choices() if c[0] != '']
		model.append({'question': a.question, 'answer': a.answer, 'choices': choices})
	for a in answer_select_multiple:
		question = Question.objects.filter(pk=a.question.id)
		choices = [c[0] for c in question[0].get_choices() if c[0] != '']
		model.append({'question': a.question, 'answer': a.answer, 'choices': choices})
	for a in answer_integer:
		question = Question.objects.filter(pk=a.question.id)
		choices = [c[0] for c in question[0].get_choices() if c[0] != '']
		model.append({'question': a.question, 'answer': a.answer, 'choices': choices})
	for a in answer_range:
		question = Question.objects.filter(pk=a.question.id)
		choices = [c[0] for c in question[0].get_choices() if c[0] != '']
		model.append({'question': a.question, 'answer': a.answer, 'choices': choices})
		# print(a.question.id)
	# answer_base = AnswerBase.objects.filter(response=response)
	# for a in answer_base:
	# 	print(a.question.id)
	# print(model)
	return render(request, 'admin/survey/response/detail.html', {'model': model})
