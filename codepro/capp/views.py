from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Question, QuizAttempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('userindex')
    return render(request, 'quiz/home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    return render(request, 'quiz/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('userindex')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'quiz/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def userindex(request):
    categories = Question.objects.values('category').distinct()
    difficulties = Question.DIFFICULTY_LEVELS  # Get difficulty choices
    # Get valid category-difficulty combinations
    valid_combinations = Question.objects.values('category', 'difficulty').distinct()
    return render(request, 'quiz/userindex.html', {
        'categories': categories,
        'difficulties': difficulties,
        'valid_combinations': valid_combinations
    })
@login_required
def quiz_page(request, category=None, difficulty=None):
    questions = Question.objects.all()
    if category:
        questions = questions.filter(category=category)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)
    
    if not questions.exists():
        messages.error(request, 'No questions available for the selected category and difficulty.')
        return redirect('userindex')
        
    if request.method == 'POST':
        start_time_str = request.POST.get('start_time')
        try:
            start_time = float(start_time_str) if start_time_str else timezone.now().timestamp()
        except (ValueError, TypeError):
            start_time = timezone.now().timestamp()

        end_time = timezone.now().timestamp()
        time_taken = end_time - start_time
        score = 0
        correct = 0
        wrong = 0
        total = len(questions)
        
        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected and int(selected) == question.correct_option:
                score += 1
                correct += 1
            else:
                wrong += 1
        
        percentage = (score / total) * 100 if total > 0 else 0
        attempt = QuizAttempt.objects.create(
            user=request.user,
            score=score,
            time_taken=time_taken,
            total_questions=total,
            correct_answers=correct,
            wrong_answers=wrong,
            percentage=percentage,
            category=category,
            difficulty=difficulty
        )
        return redirect('result')
    
    return render(request, 'quiz/quiz_page.html', {'questions': questions, 'category': category, 'difficulty': difficulty})

@login_required
def result(request):
    attempt = QuizAttempt.objects.filter(user=request.user).latest('attempted_at')
    return render(request, 'quiz/result.html', {'attempt': attempt})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')
    attempts = QuizAttempt.objects.all()
    questions = Question.objects.all()
    categories = Question.objects.values('category').distinct()
    return render(request, 'quiz/admin_dashboard.html', {'attempts': attempts, 'questions': questions, 'categories': categories})

@login_required
def add_question(request):
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        text = request.POST['text']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        correct_option = int(request.POST['correct_option'])
        category = request.POST['category']
        difficulty = request.POST['difficulty']
        Question.objects.create(
            text=text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            category=category,
            difficulty=difficulty
        )
        messages.success(request, 'Question added successfully')
        return redirect('admin_dashboard')
    return render(request, 'quiz/add_question.html')

@login_required
def edit_question(request, question_id):
    if not request.user.is_staff:
        return redirect('login')
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.text = request.POST['text']
        question.option1 = request.POST['option1']
        question.option2 = request.POST['option2']
        question.option3 = request.POST['option3']
        question.option4 = request.POST['option4']
        question.correct_option = int(request.POST['correct_option'])
        question.category = request.POST['category']
        question.difficulty = request.POST['difficulty']
        question.save()
        messages.success(request, 'Question updated successfully')
        return redirect('admin_dashboard')
    return render(request, 'quiz/edit_question.html', {'question': question})

@login_required
def delete_question(request, question_id):
    if not request.user.is_staff:
        return redirect('login')
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

@login_required
def delete_category(request, category):
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        Question.objects.filter(category=category).delete()
        messages.success(request, f'Category "{category}" and its questions deleted successfully')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')


@login_required
def select_difficulty(request, category):
    difficulties = Question.DIFFICULTY_LEVELS
    # Get available difficulties for the selected category
    available_difficulties = Question.objects.filter(category=category).values('difficulty').distinct()
    available_difficulty_values = [diff['difficulty'] for diff in available_difficulties]
    return render(request, 'quiz/select_difficulty.html', {
        'category': category,
        'difficulties': [diff for diff in difficulties if diff[0] in available_difficulty_values]
    })