from survey.models import Question, QuestionImage, Category, Survey, Response, AnswerText, AnswerRadio, AnswerSelect, AnswerInteger, AnswerSelectMultiple, AnswerRange
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
import nested_admin

class QuestionImageInline(nested_admin.NestedTabularInline):
	model = QuestionImage
	extra = 0
	list_display = ('image', )
	classes = ['question-images', ]
	template = "admin/survey/edit_inline/tabular.html"
	js = ('js/admin/customjs.js',)

class QuestionInline(nested_admin.NestedTabularInline):
	model = Question
	# ordering = ('category',)
	extra = 0
	inlines = [QuestionImageInline]

class CategoryInline(admin.TabularInline):
	model = Category
	extra = 0

class SurveyAdmin(nested_admin.NestedModelAdmin):
	inlines = [QuestionInline]

class AnswerBaseInline(admin.StackedInline):
	fields = ('question', 'answer')
	readonly_fields = ('question', 'answer')
	extra = 0
#
class AnswerTextInline(AnswerBaseInline):
	model= AnswerText
	template = "admin/survey/edit_inline/stacked.html"

	def has_add_permission(self, request, obj):
		return False

	def has_delete_permission(self, request, obj):
		return False

class AnswerRadioInline(AnswerBaseInline):
	model= AnswerRadio
	template = "admin/survey/edit_inline/stacked.html"

	def has_add_permission(self, request, obj):
		return False

	def has_delete_permission(self, request, obj):
		return False

class AnswerSelectInline(AnswerBaseInline):
	model= AnswerSelect
	template = "admin/survey/edit_inline/stacked.html"

	def has_add_permission(self, request, obj):
		return False

	def has_delete_permission(self, request, obj):
		return False

class AnswerSelectMultipleInline(AnswerBaseInline):
	model= AnswerSelectMultiple
	template = "admin/survey/edit_inline/stacked.html"

	def has_add_permission(self, request, obj):
		return False

	def has_delete_permission(self, request, obj):
		return False

class AnswerIntegerInline(AnswerBaseInline):
	model= AnswerInteger
	template = "admin/survey/edit_inline/stacked.html"

	def has_add_permission(self, request, obj):
		return False

	def has_delete_permission(self, request, obj):
		return False

class AnswerRangeInline(AnswerBaseInline):
	model= AnswerRange
	template = "admin/survey/edit_inline/stacked.html"

	def has_add_permission(self, request, obj):
		return False

	def has_delete_permission(self, request, obj):
		return False

def response_detail(obj):
	print('response_id', obj.id)
	return mark_safe('<a href="{}">View</a>'.format(reverse('admin_response_detail', args=[obj.id])))

class ResponseAdmin(admin.ModelAdmin):
	list_display = ('survey', 'created', response_detail)
	inlines = [AnswerTextInline, AnswerRadioInline, AnswerSelectInline, AnswerSelectMultipleInline, AnswerIntegerInline, AnswerRangeInline]
	# specifies the order as well as which fields to act on
	readonly_fields = ('survey', 'created', 'interview_uuid', 'name')
	save_as = True

	def change_view(self, request, object_id, form_url='', extra_context=None):
		extra_context = extra_context or {}
		extra_context['show_save'] = False
		extra_context['title'] = False
		return super(ResponseAdmin, self).change_view(request, object_id,
			form_url, extra_context=extra_context)

#admin.site.register(Question, QuestionInline)
#admin.site.register(Category, CategoryInline)
# admin.site.register(QuestionImage, QuestionImageAdmin)
admin.site.register(Survey, SurveyAdmin)

admin.site.register(Response, ResponseAdmin)
# admin.site.register(AnswerText, ResponseAdmin)
