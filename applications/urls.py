from django.urls import path

from .views import ApplicationAPIView, DocumentAPIView, ApplicationRetrieveAPIView, DocumentRetrieveAPIView

urlpatterns = [
    path('applications/', ApplicationAPIView.as_view(), name='applications'),
    path('application/<int:pk>/', ApplicationRetrieveAPIView.as_view(), name='application'),
    path('documents/', DocumentAPIView.as_view(), name='documents'),
    path('document/<int:pk>/', DocumentRetrieveAPIView.as_view(), name='document')
]

