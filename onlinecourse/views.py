from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import (
    Course,
    Lesson,
    Question,
    Choice,
    Submission
)


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {
            "course": course
        }
    )


@login_required
def submit(request, course_id):

    course = get_object_or_404(Course, pk=course_id)

    questions = Question.objects.filter(
        lesson__course=course
    )

    score = 0
    total = questions.count()

    submission = Submission.objects.create(
        user=request.user,
        course=course
    )

    for question in questions:

        selected_choice_id = request.POST.get(
            f"question_{question.id}"
        )

        if selected_choice_id:

            choice = Choice.objects.get(
                pk=selected_choice_id
            )

            submission.choices.add(choice)

            if choice.is_correct:
                score += 1

    percentage = 0

    if total > 0:
        percentage = round(
            (score / total) * 100,
            2
        )

    submission.score = percentage
    submission.save()

    return redirect(
        "show_exam_result",
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(
    request,
    course_id,
    submission_id
):

    course = get_object_or_404(
        Course,
        pk=course_id
    )

    submission = get_object_or_404(
        Submission,
        pk=submission_id
    )

    passed = submission.score >= 50

    return render(
        request,
        "onlinecourse/result.html",
        {
            "course": course,
            "submission": submission,
            "passed": passed,
        }
    )