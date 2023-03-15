from django.shortcuts import render
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task


class TaskAPIView(APIView):
    def get(self, request):
        output = [
            {
                'task_name': task.task_name,
                'start_date': task.start_date,
                'duration': (task.deadline - task.start_date).days,
                'status': task.status
            }
            for task in Task.objects.all()
        ]
        return Response({'tasks': output})

    def post(self, request):
        return Response({"succues": True})
        # try:
        #     if isinstance(request.data, list):
        #         tasks = []
        #         for task in request.data:
        #             new_task = Task.objects.create(
        #                 task_name=task.get('task_name'),
        #                 task_description=task.get('task_description', None),
        #                 start_date=task.get('start_date'),
        #                 deadline=task.get('deadline'),
        #                 status=task.get('status')
        #             )
        #             tasks.append(model_to_dict(task))
        #         return Response({'status': 'Success', 'tasks': tasks})
        #     else:
        #         task = Task.objects.create(
        #             task_name=request.data.get('task_name'),
        #             task_description=request.data.get('task_description', None),
        #             start_date=request.data.get('start_date'),
        #             deadline=request.data.get('deadline'),
        #             status=request.data.get('status')
        #         )
        #         return Response({'status': 'Success', 'task': model_to_dict(task)})
        # except:
        #     return Response({'status': 'Failed'})
