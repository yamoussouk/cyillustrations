from django import forms
from django.forms import models
from survey.models import Question, QuestionImage, Category, Survey, Response, AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple
from django.utils.safestring import mark_safe
import uuid

class CustomRadioSelectBoundField(forms.BoundField):
	@property
	def select(self):
		value = self.value()
		if value:
			return value
		else:
			return None


class CustomRadioSelect(forms.RadioSelect):
	def __init__(self, attrs=None, show_hidden_initial=False, initial=None,
			   localize=False, disabled=False, label_suffix=None, choices=(),
				label='', widget=forms.RadioSelect(), *args, **kwargs):
		super().__init__(attrs)
		self.choices = list(choices)
		self.label = label
		self.widget = widget
		self.show_hidden_initial = show_hidden_initial
		self.localize = localize
		self.disabled = disabled
		self.label_suffix = label_suffix
		self.initial = initial
		self.images = kwargs['images']

	def get_bound_field(self, form, field_name):
		return CustomRadioSelectBoundField(form, self, field_name)

	def prepare_value(self, value):
		return value

	def create_option(self, name, value, label, selected, index, subindex=None,
					attrs=None):
		index = str(index) if subindex is None else "%s_%s" % (index, subindex)
		if attrs is None:
			attrs = {}
		option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
		if selected:
			option_attrs.update(self.checked_attribute)
		if 'id' in option_attrs:
			option_attrs['id'] = self.id_for_label(option_attrs['id'], index)
		return {
			'name': name,
			'value': value,
			'label': label,
			'selected': selected,
			'index': index,
			'attrs': option_attrs,
			'type': self.input_type,
			'template_name': self.option_template_name,
			'wrap_label': True,
			'image': self.images[int(index)]
		}

	images = 'EZ MI?'
	option_template_name = 'survey/radio_option.html'
	help_text="Your helptext here."

# blatantly stolen from
# http://stackoverflow.com/questions/5935546/align-radio-buttons-horizontally-in-django-forms?rq=1
class HorizontalRadioRenderer(forms.RadioSelect):
  def render(self):
	  return mark_safe(u'\n'.join([u'%s\n' % str(w) for w in self]))


class ResponseForm(models.ModelForm):
	class Meta:
		model = Response
		fields = ()

	def __init__(self, *args, **kwargs):
		# expects a survey object to be passed in initially
		survey = kwargs.pop('survey')
		self.survey = survey
		super(ResponseForm, self).__init__(*args, **kwargs)
		self.uuid = random_uuid = uuid.uuid4().hex

		# add a field for each survey question, corresponding to the question
		# type as appropriate.
		data = kwargs.get('data')
		for q in survey.questions():
			q_type = None
			if q.question_type == Question.TEXT:
				q_type = 'text'
				self.fields[f"question_{q.pk}_{q_type}"] = forms.CharField(label=q.text,
					widget=forms.TextInput)
				self.fields[f"question_{q.pk}_{q_type}"].widget.attrs.update({'class': 'form-control', 'rows': '1', 'id': f"question_{q.pk}_{q_type}", 'data_id': f'{q.pk}'})
			elif q.question_type == Question.RADIO:
				q_type = 'radio'
				question_choices = q.get_choices()
				self.fields[f"question_{q.pk}_{q_type}"] = forms.ChoiceField(label=q.text,
					widget=forms.RadioSelect(),
					choices = question_choices)
				self.fields[f"question_{q.pk}_{q_type}"].widget.attrs.update({'id': f"question_{q.pk}_{q_type}", 'data_id': f'{q.pk}'})
			elif q.question_type == Question.SELECT:
				q_type = 'select'
				question_choices = q.get_choices()
				# add an empty option at the top so that the user has to
				# explicitly select one of the options
				question_choices = tuple([('', '-------------')]) + question_choices
				self.fields[f"question_{q.pk}_{q_type}"] = forms.ChoiceField(label=q.text,
					widget=forms.Select, choices = question_choices)
				self.fields[f"question_{q.pk}_{q_type}"].widget.attrs.update({'class': 'form-control', 'id': f"question_{q.pk}_{q_type}", 'data_id': f'{q.pk}'})
			elif q.question_type == Question.SELECT_MULTIPLE:
				q_type = 'multiple'
				question_choices = q.get_choices()
				self.fields[f"question_{q.pk}_{q_type}"] = forms.MultipleChoiceField(label=q.text,
					widget=forms.CheckboxSelectMultiple, choices = question_choices)
				self.fields[f"question_{q.pk}_{q_type}"].widget.attrs.update({'id': f"question_{q.pk}_{q_type}", 'data_id': f'{q.pk}'})
			elif q.question_type == Question.INTEGER:
				q_type = 'integer'
				self.fields[f"question_{q.pk}_{q_type}"] = forms.IntegerField(label=q.text)
				self.fields[f"question_{q.pk}_{q_type}"].widget.attrs.update({'type': 'text', 'class': 'form-control', 'id': f"question_{q.pk}_{q_type}", 'data_id': f'{q.pk}'})
			elif q.question_type == Question.RANGE:
				q_type = 'range'
				question_choices = q.get_choices()
				self.fields[f"question_{q.pk}_{q_type}"] = forms.IntegerField(label=q.text, widget=forms.NumberInput(attrs={'type':'range', 'class': f'c-range_{q.pk}', 'data-slider-min':"0", 'data-slider-max':"100", 'data-slider-step':"1", 'data-slider-value':"0", 'data-slider-handler': 'custom', 'oninput':'display(id);', 'data_from':f'{question_choices[0][0]}', 'data_to':f'{question_choices[1][0]}', 'id': f"question_{q.pk}_{q_type}", 'data_id': f'{q.pk}'}))
				self.fields[f"question_{q.pk}_{q_type}"].name = 'range'
			elif q.question_type == Question.IMAGE:
				q_type = 'image'
				question_choices = q.get_choices()
				images = [image.get_image() for image in QuestionImage.objects.filter(question__text=q.text)]
				boundaries = f'{question_choices[0][0]}-{question_choices[1][0]}'
				self.fields[f"question_{q.pk}_{q_type}"] = forms.ChoiceField(label=q.text,
					widget=CustomRadioSelect(images=images),
					choices = question_choices, required=True)
				self.fields[f"question_{q.pk}_{q_type}"].widget.attrs.update({'data_id': f'{q.pk}'})
				self.fields[f"question_{q.pk}_{q_type}"].name = 'image'
			elif q.question_type == Question.PLAIN:
				q_type = 'plain'
				self.fields[f"question_{q.pk}_{q_type}"] = forms.CharField(label=q.text,
					widget=forms.TextInput)
				self.fields[f"question_{q.pk}_{q_type}"].widget.attrs.update({'class': 'anything'})
			# if the field is required, give it a corresponding css class.
			if q.required:
				self.fields[f"question_{q.pk}_{q_type}"].required = True
				if 'class' in self.fields[f"question_{q.pk}_{q_type}"].widget.attrs:
					required_class = self.fields[f"question_{q.pk}_{q_type}"].widget.attrs["class"] + " required"
				else:
					required_class = 'required'
				self.fields[f"question_{q.pk}_{q_type}"].widget.attrs.update({'class': required_class})
			else:
				self.fields[f"question_{q.pk}_{q_type}"].required = False

			classes = self.fields[f"question_{q.pk}_{q_type}"].widget.attrs.get("class")
			if classes:
				self.fields[f"question_{q.pk}_{q_type}"].widget.attrs["class"] = classes
			self.fields[f"question_{q.pk}_{q_type}"].widget.attrs["category"] = ''


			# initialize the form field with values from a POST request, if any.
			if data:
				self.fields[f"question_{q.pk}_{q_type}"].initial = data.get('question_%d' % q.pk)

	def save(self, commit=True):
		# save the response object
		response = super(ResponseForm, self).save(commit=False)
		response.survey = self.survey
		response.interview_uuid = self.uuid
		response.save()

		# create an answer object for each question and associate it with this
		# response.
		for field_name, field_value in self.cleaned_data.items():
			if field_name.startswith("question_"):
				# warning: this way of extracting the id is very fragile and
				# entirely dependent on the way the question_id is encoded in the
				# field name in the __init__ method of this form class.
				q_id = int(field_name.split("_")[1])
				q = Question.objects.get(pk=q_id)
				if q.question_type == Question.TEXT:
					a = AnswerText(question = q)
					a.answer = field_value
				elif q.question_type == Question.RADIO:
					a = AnswerRadio(question = q)
					a.answer = field_value
				elif q.question_type == Question.SELECT:
					a = AnswerSelect(question = q)
					a.answer = field_value
				elif q.question_type == Question.SELECT_MULTIPLE:
					a = AnswerSelectMultiple(question = q)
					a.answer = ', '.join([str(i) for i in field_value])
				elif q.question_type == Question.INTEGER:
					a = AnswerInteger(question = q)
					a.answer = field_value
				elif q.question_type == Question.RANGE:
					a = AnswerText(question = q)
					a.answer = field_value
				elif q.question_type == Question.IMAGE:
					a = AnswerRadio(question = q)
					a.answer = field_value
				a.response = response
				a.save()
		return response
