from django.contrib.auth.models import User

from workflow.models import Rater


class WorkerIdBackend:
    def authenticate(self, request, worker_id=None):
        try:
            rater = Rater.objects.filter(worker_id=worker_id).get()
        except Rater.DoesNotExist:
            return None
        else:
            return rater.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
