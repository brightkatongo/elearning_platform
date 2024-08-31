# courses/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Module, Quiz, Question, Choice, StudentProgress
from django.utils import timezone
from django.db.models import Q


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(course=course).order_by('order')
    return render(request, 'courses/course_detail.html', {'course': course, 'modules': modules})

@login_required
def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    progress, created = StudentProgress.objects.get_or_create(
        user=request.user,
        course=module.course,
        module=module
    )
    return render(request, 'courses/module_detail.html', {'module': module, 'progress': progress})
# courses/views.py
from django.utils import timezone

@login_required
def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        score = 0
        total_questions = quiz.question_set.count()
        for question in quiz.question_set.all():
            if question.question_type == 'multiple_choice':
                selected_choice = request.POST.get(f'question_{question.id}')
                if selected_choice:
                    choice = Choice.objects.get(id=selected_choice)
                    if choice.is_correct:
                        score += 1
            elif question.question_type == 'true_false':
                answer = request.POST.get(f'question_{question.id}')
                correct_answer = question.choice_set.get(is_correct=True).text.lower()
                if answer.lower() == correct_answer:
                    score += 1
            elif question.question_type == 'short_answer':
                answer = request.POST.get(f'question_{question.id}')
                correct_answer = question.choice_set.get(is_correct=True).text.lower()
                if answer.lower() == correct_answer:
                    score += 1
        
        percentage = (score / total_questions) * 100
        return render(request, 'courses/quiz_result.html', {'quiz': quiz, 'score': score, 'percentage': percentage})
    else:
        questions = quiz.question_set.all()
        start_time = timezone.now()
        request.session['quiz_start_time'] = start_time.timestamp()
        return render(request, 'courses/quiz.html', {'quiz': quiz, 'questions': questions, 'start_time': start_time})

@login_required
def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        score = 0
        total_questions = quiz.question_set.count()
        for question in quiz.question_set.all():
            selected_choice = request.POST.get(f'question_{question.id}')
            if selected_choice:
                choice = Choice.objects.get(id=selected_choice)
                if choice.is_correct:
                    score += 1
        percentage = (score / total_questions) * 100
        return render(request, 'courses/quiz_result.html', {'quiz': quiz, 'score': score, 'percentage': percentage})
    else:
        questions = quiz.question_set.all()
        return render(request, 'courses/quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def mark_module_complete(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    progress, created = StudentProgress.objects.get_or_create(
        user=request.user,
        course=module.course,
        module=module
    )
    progress.completed = True
    progress.save()
    return redirect('module_detail', module_id=module_id)
    # courses/views.py
@login_required
def user_dashboard(request):
    enrolled_courses = Course.objects.filter(studentprogress__user=request.user).distinct()
    progress_data = []
    
    for course in enrolled_courses:
        total_modules = course.module_set.count()
        completed_modules = StudentProgress.objects.filter(user=request.user, course=course, completed=True).count()
        progress_percentage = (completed_modules / total_modules) * 100 if total_modules > 0 else 0
        
        progress_data.append({
            'course': course,
            'progress_percentage': progress_percentage,
            'completed_modules': completed_modules,
            'total_modules': total_modules,
        })
    
    return render(request, 'courses/user_dashboard.html', {'progress_data': progress_data})
# courses/views.py


def search_courses(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        courses = Course.objects.all()
    return render(request, 'courses/search_results.html', {'courses': courses, 'query': query})
    # courses/views.py
from django.contrib import messages
from .forms import CourseReviewForm

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(course=course).order_by('order')
    reviews = CourseReview.objects.filter(course=course).order_by('-created_at')
    
    if request.method == 'POST':
        form = CourseReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.course = course
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseReviewForm()
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'reviews': reviews,
        'form': form,
    })
# courses/views.py
from django.contrib import messages
from .forms import CourseReviewForm

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(course=course).order_by('order')
    reviews = CourseReview.objects.filter(course=course).order_by('-created_at')
    
    if request.method == 'POST':
        form = CourseReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.course = course
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseReviewForm()
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'reviews': reviews,
        'form': form,
    })