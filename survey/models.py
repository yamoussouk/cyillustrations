from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

class Survey(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField()

	def __unicode__(self):
		return (self.name)

	def questions(self):
		if self.pk:
			return Question.objects.filter(survey=self.pk)
		else:
			return None

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=400)
	survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

	def __unicode__(self):
		return (self.name)

	def __str__(self):
		return self.name

def validate_list(value):
	'''takes a text value and verifies that there is at least one comma '''
	values = value.split(';')
	if len(values) < 2:
		raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")

class Question(models.Model):
	TEXT = 'text'
	RADIO = 'radio'
	SELECT = 'select'
	SELECT_MULTIPLE = 'select-multiple'
	INTEGER = 'integer'
	RANGE = 'range'
	IMAGE = 'image'
	PLAIN = 'plain'

	QUESTION_TYPES = (
		(TEXT, 'text'),
		(RADIO, 'radio'),
		(SELECT, 'select'),
		(SELECT_MULTIPLE, 'Select Multiple'),
		(INTEGER, 'integer'),
		(RANGE, 'range'),
		(IMAGE, 'image'),
		(PLAIN, 'plain'),
	)

	text = models.TextField()
	required = models.BooleanField()
	# category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
	survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
	question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
	# the choices field is only used if the question type
	choices = models.TextField(blank=True, null=True,
		help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question .')
	# images = models.ManyToManyField(QuestionImage, null=True, blank=True)

	def save(self, *args, **kwargs):
		if (self.question_type == Question.RADIO or self.question_type == Question.SELECT
			or self.question_type == Question.SELECT_MULTIPLE or self.question_type == Question.RANGE):
			validate_list(self.choices)
		super(Question, self).save(*args, **kwargs)

	def get_choices(self):
		''' parse the choices field and return a tuple formatted appropriately
		for the 'choices' argument of a form widget.'''
		choices = self.choices.split(';')
		choices_list = []
		for c in choices:
			c = c.strip()
			choices_list.append((c,c))
		choices_tuple = tuple(choices_list)
		return choices_tuple

	# def get_images(self):
	# 	return [image.image.url for image in self.images.all()]

	def __unicode__(self):
		return (self.text)

	def __str__(self):
		return self.text

class QuestionImage(models.Model):
	question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
	# survey = models.ForeignKey(Survey, related_name='survey', default=0, on_delete=models.CASCADE)
	image = models.ImageField(upload_to=settings.IMAGE_UPLOAD_PATH, blank=True, null=True)
	# questions = models.ManyToManyField('Question', through='Question_Images')

	def get_absolute_image_url(self):
		return os.path.join(settings.IMAGE_UPLOAD_PATH, self.images.url)

	def get_image(self):
		return self.image.url

	def __str__(self):
		return self.image.url.rsplit('/', 1)[1]

class Response(models.Model):
	# a response object is just a collection of questions and answers with a
	name = models.CharField(max_length=400)
	# unique interview uuid
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
	interview_uuid = models.CharField("Unique identifier", max_length=36)

	def __unicode__(self):
		return ("response %s" % self.interview_uuid)

class AnswerBase(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	response = models.ForeignKey(Response, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

# these type-specific answer models use a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.
class AnswerText(AnswerBase):
	answer = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.answer if self.answer else 'No answer'

class AnswerRadio(AnswerBase):
	answer = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.answer if self.answer else 'No answer'

class AnswerSelect(AnswerBase):
	answer = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.answer if self.answer else 'No answer'

class AnswerSelectMultiple(AnswerBase):
	answer = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.answer if self.answer else 'No answer'

class AnswerInteger(AnswerBase):
	answer = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return str(self.answer) if self.answer else 'No answer'

class AnswerRange(AnswerBase):
	answer = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.answer) if self.answer else 'No answer'
