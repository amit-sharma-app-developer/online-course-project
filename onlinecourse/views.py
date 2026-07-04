from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Question, Choice, Submission
from django.contrib.auth.decorators import login_required


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(course=course)

    score = 0
    total = questions.count()

    if request.method == "POST":
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected:
                choice = Choice.objects.get(id=selected)
                if choice.is_correct:
                    score += 1

        percentage = (score / total) * 100 if total > 0 else 0

        Submission.objects.create(
            user=request.user,
            course=course,
            score=percentage
        )

        return redirect("show_exam_result", course_id=course.id, score=percentage)

    return render(request, "onlinecourse/submit.html", {"course": course, "questions": questions})


@login_required
def show_exam_result(request, course_id, score):
    return render(request, "onlinecourse/result.html", {"score": score})