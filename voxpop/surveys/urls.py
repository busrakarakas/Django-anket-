from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('anketler/', views.SurveyListView.as_view(), name='survey_list'),
    path('anket/<int:pk>/', views.SurveyDetailView.as_view(), name='survey_detail'),
    path('anket/<int:pk>/sonuclar/', views.ResultsView.as_view(), name='results'),
    path('anket/<int:survey_pk>/soru/<int:question_pk>/oy/', views.vote, name='vote'),
    # Kullanıcı anket oluşturma
    path('anket-olustur/', views.create_survey, name='create_survey'),
    path('anket/<int:pk>/sorular/', views.add_question, name='add_question'),
    path('anketlerim/', views.my_surveys, name='my_surveys'),
    path('anket/<int:pk>/sil/', views.delete_survey, name='delete_survey'),
]

# Hata sayfalarını test etmek için (sadece geliştirme)
from django.urls import path
from surveys import error_views as ev

urlpatterns += [
    path('hata/404/', lambda r: ev.error_404(r), name='test_404'),
    path('hata/500/', lambda r: ev.error_500(r), name='test_500'),
    path('hata/403/', lambda r: ev.error_403(r), name='test_403'),
]
