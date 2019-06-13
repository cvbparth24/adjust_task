from rest_framework import routers
from django.conf.urls import url, include
from . import views

router = routers.SimpleRouter()

router.register(r'pmall', views.PerformanceMetricsModelView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^pmview/$', views.PerformanceMetricsAPIView.as_view()),
]



