
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('accounts/logout/',
         LogoutView.as_view(next_page=reverse_lazy('main_view')),
         name='logout'),
    path('dump/conf/', views.DumpConfView.as_view(),
         name='dump_conf'),
    path('workflow/item/<int:pk>/', views.WorkflowFormView.as_view(),
         name='item'),
    path('redirect/', views.RedirectLinkView.as_view(),
         name='redirect'),
    path('feedback/', views.FeedbackView.as_view(),
         name='feedback'),
    path('auto-send/', views.MTurkAutoSendView.as_view(),
         name='auto-send'),

    path('qualify/', views.QualifyView.as_view(),
         name='qualify'),
    path('labelone/', views.LabelOneView.as_view(),
         name='labelone'),
    path('quiz/', views.QuizView.as_view(),
         name='quiz'),
    path('consent/', views.ConsentView.as_view(),
         name='consent'),
    path('knowledge/', views.KnowledgeView.as_view(),
         name='knowledge'),
    path('demographics/', views.DemographicsView.as_view(),
         name='demographics'),
    path('congratulations/', views.CongratulationsView.as_view(),
         name='congratulations'),
    path('thankyou/', views.ThankYouView.as_view(),
         name='thankyou'),
    path('error/', views.ErrorView.as_view(),
         name='error'),
    path('test/', views.TestView.as_view(),   # add
         name='test'),
]
