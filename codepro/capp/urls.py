from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login_view', views.login_view, name='login'),
    path('adminindex', views.adminindex, name='adminindex'), 
    path('usersignup', views.signup, name='signup'),
    path('forgotpassword', views.getusername, name='forgotpassword'),
    path('verifyotp', views.verifyotp, name='verifyotp'),
    path('passwordreset', views.passwordreset, name='passwordreset'),
    path('', views.index, name="index"), 
    path('logout', views.logoutuser, name="logoutuser"),
    path('adminlogout/', views.logoutadmin, name='adminlogout'),
    path('profile/', views.profile, name='profile'),
    path('quiz/<int:category_id>/', views.quiz_difficulty, name='quiz_difficulty'),
    path('quiz/<int:category_id>/<str:difficulty>/', views.take_quiz, name='take_quiz'),
    path('questions/', views.manage_questions, name='manage_questions'),
    path('questions/add/', views.add_question, name='add_question'),
    path('questions_edit/<int:question_id>/', views.edit_question, name='edit_question'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('questions/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('categories/add/', views. add_category, name='add_category'),  
    path('quiz/<int:category_id>/result/', views.quiz_result, name='quiz_result'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
