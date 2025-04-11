from django.contrib.admin.templatetags.admin_list import pagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .filter import PatientCodingFilterSet, PatientProcedureEventsFilterSet, PatientVisitFilterSet, \
    PatientPostOPComplicationsFilterSet, PatientLDAFilterSet, PatientLabsFilterSet, PatientInformationFilterSet, \
    PatientHistoryFilterSet, PatientMedicationFilterSet
from .models import (PatientCoding, PatientHistory, PatientInformation, PatientLabs, PatientLDA,
                     PatientPostOPComplications, PatientProcedureEvents, PatientVisit, PatientMedication)
from .serializer import PatientCodingSerializer, PatientHistorySerializer, PatientInformationSerializer, \
    PatientLabsSerializer, PatientLDASerializer, PatientPostOPComplicationsSerializer, PatientProcedureEventsSerializer, \
    PatientVisitSerializer, PatientMedicationSerializer
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000


class FilterAPIDataAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        log_id = self.request.GET.get("log_id")
        mrn = self.request.GET.get("mrn")

        coding_query = PatientCoding.objects.filter(Q(mrn=mrn) | Q(log_id=log_id) if log_id else Q())
        history_query = PatientHistory.objects.filter(Q(mrn=mrn) | Q(log_id=log_id) if log_id else Q())
        information_query = PatientInformation.objects.filter(Q(mrn=mrn) | Q(log_id=log_id))
        labs_query = PatientLabs.objects.filter(Q(mrn=mrn) | Q(log_id=log_id))
        lda_query = PatientLDA.objects.filter(Q(mrn=mrn) | Q(log_id=log_id))
        post_op_complication_query = PatientPostOPComplications.objects.filter(Q(mrn=mrn) | Q(log_id=log_id))
        procedure_events_query = PatientProcedureEvents.objects.filter(Q(mrn=mrn) | Q(log_id=log_id))
        visit_query = PatientVisit.objects.filter(Q(mrn=mrn) | Q(log_id=log_id))

        coding_serializer =PatientCodingSerializer(coding_query, many=True)
        history_serializer =PatientHistorySerializer(history_query, many=True)
        information_serializer =PatientInformationSerializer(information_query, many=True)
        labs_serializer =PatientLabsSerializer(labs_query, many=True)
        lda_serializer =PatientLDASerializer(lda_query, many=True)
        post_op_complication_serializer =PatientPostOPComplicationsSerializer(post_op_complication_query, many=True)
        procedure_events_serializer =PatientProcedureEventsSerializer(procedure_events_query, many=True)
        visit_serializer =PatientVisitSerializer(visit_query, many=True)

        res_data = {
            "coding_data":coding_serializer.data,
            "history_data":history_serializer.data,
            "information_data":information_serializer.data,
            "labs_data":labs_serializer.data,
            "lda_data":lda_serializer.data,
            "post_op_complication_data":post_op_complication_serializer.data,
            "procedure_events_data":procedure_events_serializer.data,
            "visit_data":visit_serializer.data,
        }

        return Response(res_data, status=status.HTTP_200_OK)

class PatientCodingListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = PatientCoding.objects.all().order_by('id')
    serializer_class = PatientCodingSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = PatientCodingFilterSet

class PatientHistoryListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = PatientHistory.objects.all().order_by('id')
    serializer_class = PatientHistorySerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = PatientHistoryFilterSet

class PatientInformationListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = PatientInformation.objects.all().order_by('id')
    serializer_class = PatientInformationSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = PatientInformationFilterSet

class PatientLabsListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = PatientLabs.objects.all().order_by('id')
    serializer_class = PatientLabsSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = PatientLabsFilterSet

class PatientLDAListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = PatientLDA.objects.all().order_by('id')
    serializer_class = PatientLDASerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = PatientLDAFilterSet

class PatientPostOPComplicationsListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = PatientPostOPComplications.objects.all().order_by('id')
    serializer_class = PatientPostOPComplicationsSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = PatientPostOPComplicationsFilterSet

class PatientProcedureEventsListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = PatientProcedureEvents.objects.all().order_by('id')
    serializer_class = PatientProcedureEventsSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = PatientProcedureEventsFilterSet

class PatientVisitListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = PatientVisit.objects.all().order_by('id')
    serializer_class = PatientVisitSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = PatientVisitFilterSet

class PatientMedicationListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = PatientMedication.objects.all().order_by('id')
    serializer_class = PatientMedicationSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = PatientMedicationFilterSet