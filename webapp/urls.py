from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.convert_csv_to_other_new, name='convert-csv-new-index'),
    path('analysis', views.analysis_data, name='analysis'),
    path('search', views.search_data, name='search'),
    path('trending', views.trending_topic, name='trending'),
    path('export', views.export_csv, name='export'),
    path('export-csv', views.export_csv_news, name='export-csv'),
    path('convert-csv', views.convert_csv_to_other, name='convert-csv'),
    path('convert-csv-new', views.convert_csv_to_other_new, name='convert-csv-new'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)