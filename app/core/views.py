import os
from posixpath import basename
from .tasks import processCsv

from celery import current_app
from core.models import Task
import uuid

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse


class TaskUploadView(APIView):
    def put(self, request, filename):

        f = request.FILES['file']
        path_to_file = os.path.join(settings.UPLOADS_TMP_DIR, filename)
        with open(path_to_file, 'ab+') as destination: 
            for chunk in f.chunks():
                destination.write(chunk)

        # Process uploaded csv asynch
        celery_task = processCsv.delay(filename)
        task = Task.objects.create(type='PLAY', raw_filename=filename, raw_internal_filename=filename, celery_task_uuid = uuid.UUID(celery_task.id))
        task.save()

        response_data = {'task_status': celery_task.status, 'task_id': celery_task.id}

        return Response(response_data)

class TaskView(APIView):
    SUCCESS = 'SUCCESS'

    def stream_it(self, output_file):
        with open(output_file, 'r') as read_file:
            while True:
                data = read_file.readline()
                if not data:
                    break
                yield data

        
    def get(self, request, task_id):
        celery_task = current_app.AsyncResult(task_id)
        response_data = {'task_status': celery_task.status, 'task_id': celery_task.id}

        if celery_task.status == self.SUCCESS:
            output_file = celery_task.get()
            base_name = basename(output_file)
            task = Task.objects.get(celery_task_uuid=celery_task.id)
            task.out_filename = base_name
            task.save()

            return StreamingHttpResponse(
                self.stream_it(output_file),
                content_type="text/csv",
                headers={'Content-Disposition': 'attachment; filename="%s"'%(base_name)},
            )

        return Response(response_data)

