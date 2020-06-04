from django.contrib.auth import authenticate, login
from django.utils.deprecation import MiddlewareMixin


class WorkerIdAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        worker_id = request.GET.get('workerId')
        if worker_id:
            user = authenticate(request, worker_id=worker_id)
            if user:
                login(request, user)
