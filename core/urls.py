from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf.urls.static import static

from workflow.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workflow/', include(('workflow.urls', 'workflow'),
                              namespace='workflow')),
    path('', HomeView.as_view(), name='home'),
    path('robots.txt',
         lambda x: HttpResponse("User-Agent: *\nDisallow: /",
                                content_type="text/plain")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
