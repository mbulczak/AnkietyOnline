from django.http import JsonResponse
from django.db.models import Max
from .models import Question


def update_question_position(request):
    new_order = request.POST.getlist('order[]')

    questions = Question.objects.filter(id__in=new_order)
    higest_ordial_number = questions.aggregate(Max('ordinal_number'))["ordinal_number__max"]
    
    for item_id in new_order:
        question = Question.objects.get(pk=item_id)
        question.ordinal_number = higest_ordial_number + 1
        question.save()
        higest_ordial_number += 1

    for index, item_id in enumerate(new_order, start=1):
        question= Question.objects.get(pk=item_id)
        question.ordinal_number = index
        question.save()
    
    return JsonResponse({'success': True})
