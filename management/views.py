from itertools import chain

from django.contrib.admin.templatetags.admin_list import pagination
from django.db.models import Q, CharField, Value
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
    PatientVisitSerializer, PatientMedicationSerializer, MRNMergeDataSerializer
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




class MRNFilterListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        mrn = request.GET.get("mrn")
        log_id = request.GET.get("log_id")

        instance_models = [
            PatientCoding, PatientHistory, PatientInformation, PatientLabs,
            PatientMedication, PatientLDA, PatientPostOPComplications,
            PatientProcedureEvents, PatientVisit
        ]

        all_data = []
        for model in instance_models:

            filters = Q()
            model_fields = [f.name for f in model._meta.get_fields()]

            if mrn and 'mrn' in model_fields:
                filters &= Q(mrn__iexact=mrn)

            if log_id and 'log_id' in model_fields:
                filters &= Q(log_id__iexact=log_id)

            queryset = model.objects.filter(filters)

            for obj in queryset:
                results = {
                    "model_name": model.__name__,
                    "id": getattr(obj, "id", None),
                    "mrn": getattr(obj, "mrn", None),
                    "source_key": getattr(obj, "source_key", None),
                    "source_name": getattr(obj, "source_name", None),
                    "name": getattr(obj, "name", None),
                    "ref_bill_code_set_name": getattr(obj, "ref_bill_code_set_name", None),
                    "ref_bill_code": getattr(obj, "ref_bill_code", None),
                    "diagnosis_code": getattr(obj, "diagnosis_code", None),
                    "dx_name": getattr(obj, "dx_name", None),
                    "log_id": getattr(obj, "log_id", None),
                    "disch_disp_c": getattr(obj, "disch_disp_c", None),
                    "hosp_admsn_time": getattr(obj, "hosp_admsn_time", None),
                    "hosp_disch_time": getattr(obj, "hosp_disch_time", None),
                    "los": getattr(obj, "los", None),
                    "icu_admin_flag": getattr(obj, "icu_admin_flag", None),
                    "surgery_date": getattr(obj, "surgery_date", None),
                    "birth_date": getattr(obj, "birth_date", None),
                    "height": getattr(obj, "height", None),
                    "weight": getattr(obj, "weight", None),
                    "sex": getattr(obj, "sex", None),
                    "primary_anes_type_nm": getattr(obj, "primary_anes_type_nm", None),
                    "asa_rating_c": getattr(obj, "asa_rating_c", None),
                    "asa_rating": getattr(obj, "asa_rating", None),
                    "patient_class_group": getattr(obj, "patient_class_group", None),
                    "patient_class_nm": getattr(obj, "patient_class_nm", None),
                    "primary_procedure_nm": getattr(obj, "primary_procedure_nm", None),
                    "in_or_dttm": getattr(obj, "in_or_dttm", None),
                    "out_or_dttm": getattr(obj, "out_or_dttm", None),
                    "an_start_datetime": getattr(obj, "an_start_datetime", None),
                    "an_stop_datetime": getattr(obj, "an_stop_datetime", None),
                    "enc_type_nm": getattr(obj, "enc_type_nm", None),
                    "lab_code": getattr(obj, "lab_code", None),
                    "lab_name": getattr(obj, "lab_name", None),
                    "observation_value": getattr(obj, "observation_value", None),
                    "measurement_units": getattr(obj, "measurement_units", None),
                    "reference_range": getattr(obj, "reference_range", None),
                    "abnormal_flag": getattr(obj, "abnormal_flag", None),
                    "collection_datetime": getattr(obj, "collection_datetime", None),
                    "enc_type_c": getattr(obj, "enc_type_c", None),
                    "ordering_date": getattr(obj, "ordering_date", None),
                    "order_class_nm": getattr(obj, "order_class_nm", None),
                    "medication_id": getattr(obj, "medication_id", None),
                    "display_name": getattr(obj, "display_name", None),
                    "medication_nm": getattr(obj, "medication_nm", None),
                    "start_date": getattr(obj, "start_date", None),
                    "end_date": getattr(obj, "end_date", None),
                    "order_status_nm": getattr(obj, "order_status_nm", None),
                    "record_type": getattr(obj, "record_type", None),
                    "mar_action_nm": getattr(obj, "mar_action_nm", None),
                    "med_action_time": getattr(obj, "med_action_time", None),
                    "admin_sig": getattr(obj, "admin_sig", None),
                    "dose_unit_nm": getattr(obj, "dose_unit_nm", None),
                    "med_route_nm": getattr(obj, "med_route_nm", None),
                    "description": getattr(obj, "description", None),
                    "properties_display": getattr(obj, "properties_display", None),
                    "site": getattr(obj, "site", None),
                    "placement_instant": getattr(obj, "placement_instant", None),
                    "removal_instant": getattr(obj, "removal_instant", None),
                    "flo_meas_name": getattr(obj, "flo_meas_name", None),
                    "line_group_name": getattr(obj, "line_group_name", None),
                    "element_name": getattr(obj, "element_name", None),
                    "context_name": getattr(obj, "context_name", None),
                    "element_abbr": getattr(obj, "element_abbr", None),
                    "smrtdta_elem_value": getattr(obj, "smrtdta_elem_value", None),
                    "event_display_name": getattr(obj, "event_display_name", None),
                    "event_time": getattr(obj, "event_time", None),
                    "note_text": getattr(obj, "note_text", None),
                }

                all_data.append(results)

        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(all_data, request)

        return paginator.get_paginated_response(paginated_data)



# class MRNFilterListAPIView(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         mrn = request.GET.get("mrn")
#         if not mrn:
#             return Response({"error": "MRN parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # List of models and fields to fetch
#         instance_models = [
#             PatientCoding, PatientHistory, PatientInformation, PatientLabs,
#             PatientMedication, PatientLDA, PatientPostOPComplications,
#             PatientProcedureEvents, PatientVisit
#         ]
#
#         # Define fields you want to fetch from all models (subset)
#         fields = [
#             "id", "mrn", "source_key", "source_name", "name",
#             "ref_bill_code_set_name", "ref_bill_code", "diagnosis_code",
#             "dx_name", "log_id", "disch_disp_c", "hosp_admsn_time",
#             "hosp_disch_time", "los", "icu_admin_flag", "surgery_date",
#             "birth_date", "height", "weight", "sex", "primary_anes_type_nm",
#             "asa_rating_c", "asa_rating", "patient_class_group",
#             "patient_class_nm", "primary_procedure_nm", "in_or_dttm",
#             "out_or_dttm", "an_start_datetime", "an_stop_datetime",
#             "enc_type_nm", "lab_code", "lab_name", "observation_value",
#             "measurement_units", "reference_range", "abnormal_flag",
#             "collection_datetime", "enc_type_c", "ordering_date",
#             "order_class_nm", "medication_id", "display_name",
#             "medication_nm", "start_date", "end_date", "order_status_nm",
#             "record_type", "mar_action_nm", "med_action_time", "admin_sig",
#             "dose_unit_nm", "med_route_nm", "description", "properties_display",
#             "site", "placement_instant", "removal_instant", "flo_meas_name",
#             "line_group_name", "element_name", "context_name", "element_abbr",
#             "smrtdta_elem_value", "event_display_name", "event_time", "note_text",
#         ]
#
#         all_data_querysets = []
#
#         for model in instance_models:
#             qs = model.objects.filter(mrn__iexact=mrn).values(*fields)
#             # Add model name so frontend knows where the data came from
#             qs = qs.annotate(model_name=Value(model.__name__, output_field=CharField()))
#             all_data_querysets.append(qs)
#
#         # Chain all querysets into a single iterable
#         all_data = list(chain(*all_data_querysets))
#
#         paginator = CustomPagination()
#         paginated_data = paginator.paginate_queryset(all_data, request)
#
#         return paginator.get_paginated_response(paginated_data)