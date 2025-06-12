from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('userindex/', views.userindex, name='userindex'),
    path('quiz/', views.quiz_page, name='quiz_page'),
    path('quiz/<str:category>/', views.select_difficulty, name='select_difficulty'),  # New URL
    path('quiz/difficulty/<str:difficulty>/', views.quiz_page, name='quiz_page_difficulty'),
    path('quiz/<str:category>/<str:difficulty>/', views.quiz_page, name='quiz_page_category_difficulty'),
    path('result/', views.result, name='result'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_question/', views.add_question, name='add_question'),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('delete_category/<str:category>/', views.delete_category, name='delete_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)