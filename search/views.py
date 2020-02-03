from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import ListView

from questions.models import Question


def search(request):
    if 'q' not in request.GET:
        return redirect('')

    querystring = request.GET.get('q').strip()

    # if len(querystring) == 0:
    #     return redirect('')

    results = {'questions': Question.objects.filter(
        Q(title__icontains=querystring) |
        Q(description__icontains=querystring))}

    count = {'questions': results['questions'].count()}

    context = {
        'hide_search': True,
        'querystring': querystring,
        'count': count['questions'],
        'results': results['questions']
    }

    return render(request, 'search/results.html', context)





