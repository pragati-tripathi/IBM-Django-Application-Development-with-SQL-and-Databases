# <HINT> Create a submit view to create an exam submission record for a course enrollment
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)

    choices = extract_answers(request)
    submission.choices.set(choices)

    submission_id = submission.id

    return HttpResponseRedirect(
        reverse('onlinecourse:exam_result', args=(course_id, submission_id,))
    )


# <HINT> A example method to collect the selected choices from the exam form from the request object
def extract_answers(request):
    submitted_answers = []

    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)

    return submitted_answers


# <HINT> Create an exam result view to check if learner passed exam and show their question results and result for each question
def show_exam_result(request, course_id, submission_id):
    context = {}

    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.get(id=submission_id)

    choices = submission.choices.all()
    total_score = 0

    for choice in choices:
        if choice.is_correct:
            total_score += choice.question.grade

    context['course'] = course
    context['grade'] = total_score
    context['choices'] = choices

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
