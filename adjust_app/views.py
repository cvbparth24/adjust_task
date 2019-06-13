from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PerformanceMetrics
from .serializer import PerformanceMetricsSerializer
from django.db.models import Sum, Count
from datetime import date
from dateutil.parser import parse
from django.db.models import FloatField, F, ExpressionWrapper

# Create your views here.
class PerformanceMetricsAPIView(APIView):

    permission_classes = (permissions.AllowAny,)
    queryset = PerformanceMetrics.objects.all()
    serializer_class = PerformanceMetricsSerializer
    http_method_names = ['get']

    def get(self, request):

        cpi_ca = self.question_4_answer_cpi_ca()

        data: dict = request.data
        if not bool(data):
            return Response(data={"message": "No Data", "cpi_ca": cpi_ca}, status=status.HTTP_200_OK)

        # Filter by date range date_from / date_to, channels, countries and os

        date_from = None
        if "date_from" in data.keys():
            date_from = data['date_from']

        date_to = None
        if "date_to" in data.keys():
            date_to = data['date_to']

        recorded_date = None
        if "recorded_date" in data.keys():
            recorded_date = data['recorded_date']

        channel = None
        if "channel" in data.keys():
            channel = data['channel']

        country = None
        if "country" in data.keys():
            country = data['country']

        os = None
        if "os" in data.keys():
            os = data.get('os', None)

        queryset = None
        if date_from and date_to:
            queryset = self.question_1_answer(date_from=date_from, date_to=date_to)
        if recorded_date and os:
            queryset = self.question_2_answer(recorded_date=recorded_date, os=os)
        if recorded_date and country:
            queryset = self.question_3_answer(recorded_date=recorded_date, country=country)



        return Response({"data": queryset, "cpi_ca": cpi_ca}, status.HTTP_200_OK)


    def question_1_answer(self, date_from: str, date_to: str):

        if not date_from and date_to:
            return None

        if date_from and date_to:
            queryset = PerformanceMetrics.objects.filter(recorded_date__gte=date_from, recorded_date__lte=date_to).values('channel', 'country').order_by('-clicks').annotate(impressions=Sum('impressions'), clicks=Sum('clicks'))
            return queryset
        if date_from:
            queryset = PerformanceMetrics.objects.filter(recorded_date__gte=date_from).values('channel', 'country').order_by('-clicks').annotate(impressions=Sum('impressions'), clicks=Sum('clicks'))
            return queryset
        if date_to:
            queryset = PerformanceMetrics.objects.filter(recorded_date__lte=date_to).values('channel','country').order_by('-clicks').annotate(impressions=Sum('impressions'), clicks=Sum('clicks'))
            return queryset

    def question_2_answer(self, recorded_date: str, os: str):

        if not recorded_date and os:
            return None

        recorded_month = date.today().month
        recorded_year = date.today().year
        if isinstance(recorded_date, date):
            recorded_month = recorded_date.month
            recorded_year = recorded_date.year
        if isinstance(recorded_date, str):
            recorded_month = parse(recorded_date).month
            recorded_year = parse(recorded_date).year

        queryset = PerformanceMetrics.objects.filter(recorded_date__month=recorded_month, recorded_date__year=recorded_year, os=os).values('installs', 'recorded_date').order_by('recorded_date')

        return queryset

    def question_3_answer(self, recorded_date: str, country: str):

        if not recorded_date and country:
            return None

        queryset = PerformanceMetrics.objects.filter(recorded_date__exact=recorded_date, country__exact=country).values('revenue', 'os').order_by('-revenue')

        return queryset

    def question_4_answer_cpi_ca(self):

        queryset = PerformanceMetrics.objects.filter(country__exact='CA').values('channel').annotate(cpi=ExpressionWrapper(Sum(F('spend'))/Count(F('installs')), output_field=FloatField())).order_by('-cpi')

        return queryset


class PerformanceMetricsModelView(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = PerformanceMetrics.objects.all()
    serializer_class = PerformanceMetricsSerializer