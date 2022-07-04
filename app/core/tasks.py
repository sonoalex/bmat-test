from celery import current_app
from core.service import ProcessCsv

@current_app.task(bind=True)
def processCsv(self, file):

    processor = ProcessCsv.ProcessCsv()

    return processor.process(file, self.request.id)
