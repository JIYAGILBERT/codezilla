from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import datetime, timedelta
from .models import Category, Question, Option, UserProfile
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confpassword')

        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Signup successful! Please log in to continue.")
            return redirect('login')  # Redirect to login page

    return render(request, "signup.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username
            messages.success(request, "User logged in successfully!")
            if user.is_superuser:
                return redirect('adminindex')
            else:
                return redirect('index')  # Redirect to index page
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'login.html')

def index(request): 
    categories = Category.objects.filter(published=True)
    context = {
        'categories': categories,
        'no_categories': not categories.exists()
    }
    return render(request, "index.html", context)

def adminindex(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You need to be logged in as an admin to access this page.")
        return redirect('login')
    categories = Category.objects.all()
    questions = Question.objects.all()  # Add questions to context
    return render(request, 'adminindex.html', {'categories': categories, 'questions': questions})

def logoutuser(request):
    logout(request)
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('index')

def logoutadmin(request):
    logout(request)
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('index')

def getusername(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['email'] = user.email
            messages.success(request, "OTP has been sent to your email.")
            return redirect('verifyotp')
        except User.DoesNotExist:
            messages.error(request, "Username does not exist.")
    
    return render(request, 'getusername.html')  

def verifyotp(request):
    if 'email' not in request.session:
        messages.error(request, "Session expired. Please start the password reset process again.")
        return redirect('forgotpassword')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp1 = request.session.get('otp')
        otp_time_str = request.session.get('otp_time')

        if otp_time_str:
            otp_time = datetime.fromisoformat(otp_time_str)
            otp_expiry_time = otp_time + timedelta(minutes=5)
            if datetime.now() > otp_expiry_time:
                messages.error(request, 'OTP has expired. Please request a new one.')
                del request.session['otp']
                del request.session['otp_time']
                return redirect('forgotpassword')

        if otp == otp1:
            del request.session['otp']
            del request.session['otp_time']
            messages.success(request, "OTP verified successfully.")
            return redirect('passwordreset')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    # Generate and send OTP
    otp = ''.join(random.choices('123456789', k=6))
    request.session['otp'] = otp
    request.session['otp_time'] = datetime.now().isoformat()
    message = f'Your CodeZilla password reset OTP is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.session.get('email')]
    try:
        send_mail('CodeZilla Password Reset OTP', message, email_from, recipient_list)
        messages.success(request, "A new OTP has been sent to your email.")
    except Exception as e:
        messages.error(request, "Failed to send OTP. Please try again.")
        return redirect('forgotpassword')

    return render(request, "otp.html")
def passwordreset(request):
    if 'email' not in request.session:
        messages.error(request, "Session expired. Please start the password reset process again.")
        return redirect('forgotpassword')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confpassword')

        if confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        else:
            email = request.session.get('email')
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                del request.session['email']
                messages.success(request, "Your password has been reset successfully. Please log in.")
                return redirect('login')  # Fixed redirect
            except User.DoesNotExist:
                messages.error(request, "No user found with that email address.")
                return redirect('forgotpassword')

    return render(request, "passwordreset.html")

# capp/views.py
def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access this page.")
        return redirect('login')
    
    # Get or create UserProfile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        name = request.POST.get('name')
        place = request.POST.get('place')
        
        # Update User model
        if username and username != request.user.username:
            if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                messages.error(request, "Username already exists.")
            else:
                request.user.username = username
        if email and email != request.user.email:
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, "Email already exists.")
            else:
                request.user.email = email
        request.user.save()
        
        # Update UserProfile
        profile.mobile = mobile
        profile.name = name
        profile.place = place
        profile.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    
    return render(request, 'profile.html', {'user': request.user, 'profile': profile})

# capp/views.py
def quiz_difficulty(request, category_id):
    category = get_object_or_404(Category, id=category_id, published=True)
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to take the quiz.")
        return redirect('login')
    context = {
        'category': category,
        'difficulty_levels': Question.DIFFICULTY_LEVELS
    }
    return render(request, 'quiz_difficulty.html', context)
def take_quiz(request, category_id, difficulty):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to take the quiz.")
        return redirect('login')
    
    category = get_object_or_404(Category, id=category_id, published=True)
    questions = Question.objects.filter(category=category, difficulty=difficulty, published=True)
    
    if not questions.exists():
        messages.error(request, "No questions available for this category and difficulty.")
        return redirect('index')
    
    if request.method == 'POST':
        score = 0
        total = questions.count()
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=selected_option_id)
                    if selected_option.is_correct:
                        score += 1
                except Option.DoesNotExist:
                    continue
        percentage = (score / total) * 100 if total > 0 else 0
        # Store results in session
        request.session['quiz_result'] = {
            'score': score,
            'total': total,
            'percentage': percentage
        }
        print(f"Stored quiz_result: {request.session['quiz_result']}")  # Debug
        return redirect('quiz_result', category_id=category_id)
    
    print(f"Difficulty in take_quiz: {difficulty}")  # Debug
    return render(request, 'take_quiz.html', {'category': category, 'difficulty': difficulty, 'questions': questions})

def quiz_result(request, category_id):
    category = get_object_or_404(Category, id=category_id, published=True)
    # Retrieve results from session
    quiz_result = request.session.get('quiz_result')
    print(f"Retrieved quiz_result: {quiz_result}")  # Debug
    if not quiz_result:
        messages.error(request, "No quiz results found. Please take the quiz again.")
        return redirect('quiz_difficulty', category_id=category_id)
    
    score = quiz_result['score']
    total = quiz_result['total']
    percentage = quiz_result['percentage']
    win_status = percentage >= 60  # Win if percentage is 60% or higher
    
    context = {
        'category': category,
        'score': score,
        'total': total,
        'percentage': round(percentage, 2),
        'win_status': win_status
    }
    # Clean up session
    try:
        del request.session['quiz_result']
    except KeyError:
        pass
    return render(request, 'quiz_result.html', context)

def quiz_result(request, category_id):
    category = get_object_or_404(Category, id=category_id, published=True)
    quiz_result = request.session.get('quiz_result')
    print(f"Retrieved quiz_result: {quiz_result}")  # Debug
    if not quiz_result:
        messages.error(request, "No quiz results found. Please take the quiz again.")
        return redirect('quiz_difficulty', category_id=category_id)
    
    score = quiz_result.get('score', 0)
    total = quiz_result.get('total', 0)
    percentage = quiz_result.get('percentage', 0)
    win_status = percentage >= 60
    
    context = {
        'category': category,
        'score': score,
        'total': total,
        'percentage': round(percentage, 2),
        'win_status': win_status
    }
    try:
        del request.session['quiz_result']
    except KeyError:
        pass
    return render(request, 'quiz_result.html', context)

def manage_questions(request):
    if not request.user.is_superuser:
        messages.error(request, "You need admin privileges to access this page.")
        return redirect('index')
    
    categories = Category.objects.all()
    questions = Question.objects.all()
    return render(request, 'manage_questions.html', {'categories': categories, 'questions': questions})

def add_question(request):
    if not request.user.is_superuser:
        messages.error(request, "You need admin privileges to access this page.")
        return redirect('index')
    
    if request.method == 'POST':
        try:
            question_text = request.POST.get('question_text')
            category_id = request.POST.get('category')
            difficulty = request.POST.get('difficulty')
            if not question_text or not category_id or not difficulty:
                messages.error(request, 'Question text, category, and difficulty are required.')
                return redirect('add_question')

            category = Category.objects.get(id=category_id)
            question = Question.objects.create(
                question_text=question_text,
                category=category,
                difficulty=difficulty
            )
            has_correct = False
            for i in range(1, 5):
                option_text = request.POST.get(f'option{i}')
                is_correct = request.POST.get('is_correct') == str(i)
                if option_text:
                    Option.objects.create(
                        question=question,
                        text=option_text,
                        is_correct=is_correct
                    )
                    if is_correct:
                        has_correct = True
            if not has_correct:
                question.delete()
                messages.error(request, 'Please select a correct answer.')
                return redirect('add_question')
            messages.success(request, 'Question added successfully!')
            return redirect('adminindex')
        except Category.DoesNotExist:
            messages.error(request, 'Selected category does not exist.')
            return redirect('add_question')
        except Exception as e:
            messages.error(request, f'Error adding question: {str(e)}')
            return redirect('add_question')
    
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'difficulty_levels': Question.DIFFICULTY_LEVELS  # Pass DIFFICULTY_LEVELS to context
    }
    return render(request, 'add_question.html', context)

def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        question.question_text = request.POST.get('question_text')
        category_id = request.POST.get('category')
        question.category = Category.objects.get(id=category_id)
        question.save()
        # Update options
        for option in question.options.all():
            option.delete()  # Clear existing options
        for i in range(1, 5):
            option_text = request.POST.get(f'option{i}')
            is_correct = request.POST.get(f'is_correct') == str(i)
            if option_text:
                Option.objects.create(
                    question=question,
                    text=option_text,
                    is_correct=is_correct
                )
        messages.success(request, 'Question updated successfully!')
        return redirect('manage_questions')
    categories = Category.objects.all()
    return render(request, 'edit_question.html', {'question': question, 'categories': categories})

def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    messages.success(request, 'Question deleted successfully!')
    return redirect('manage_questions')

def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        if request.FILES.get('image'):
            category.image = request.FILES.get('image')
        category.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('adminindex')
    return render(request, 'edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('adminindex')
    
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    messages.success(request, "Question deleted successfully.")
    return redirect('manage_questions')

# capp/views.py
def take_quiz(request, category_id, difficulty):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to take the quiz.")
        return redirect('login')
    
    category = get_object_or_404(Category, id=category_id, published=True)
    questions = Question.objects.filter(category=category, difficulty=difficulty, published=True)
    
    if not questions.exists():
        messages.error(request, "No questions available for this category and difficulty.")
        return redirect('index')
    
    if request.method == 'POST':
        score = 0
        total = questions.count()
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=selected_option_id)
                    if selected_option.is_correct:
                        score += 1
                except Option.DoesNotExist:
                    continue
        percentage = (score / total) * 100 if total > 0 else 0
        request.session['quiz_result'] = {
            'score': score,
            'total': total,
            'percentage': percentage
        }
        return redirect('quiz_result', category_id=category_id)
    
    print(f"Difficulty in take_quiz: {difficulty}")  # Debug
    return render(request, 'take_quiz.html', {'category': category, 'difficulty': difficulty, 'questions': questions})

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category = Category(name=name, description=description, image=image)
        category.save()
        messages.success(request, 'Category added successfully!')
        return redirect('adminindex')
    return render(request, 'add_category.html')