from django.conf.urls import include
from django.urls import path, re_path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from . import views
from django.conf.urls.static import static

admin.autodiscover()
media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')

urlpatterns = [
	# Examples:
	path('admin/', admin.site.urls),
	# path('', views.Index, name='home'),
	path('survey/<int:id>/', views.SurveyDetail, name='survey_detail'),
	re_path(r'^confirm/(?P<uuid>[^/]+)/$', views.Confirm, name='confirmation'),
	path('privacy/', views.privacy, name='privacy_statement'),
	path('admin/response/<int:response_id>', views.admin_response_detail, name='admin_response_detail'),


	# Uncomment the admin/doc line below to enable admin documentation:
	path('admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# path('admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # media url hackery. le sigh.
# urlpatterns += [
#     re_path(r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
#      { 'document_root': settings.MEDIA_ROOT, 'show_indexes':True }),
# ]
