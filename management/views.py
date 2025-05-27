import json
from itertools import chain

from django.contrib.admin.templatetags.admin_list import pagination
from django.core import cache
from django.core.cache import caches
from django.db import connection
from django.db.models import Q, CharField, Value
from django.http import JsonResponse
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

            queryset = model.objects.filter(filters).only(*model_fields)

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

        serializer = MRNMergeDataSerializer(all_data, many=True)
        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(serializer.data, request)

        return paginator.get_paginated_response(paginated_data)

#
# class SQLMRNFilterListAPIView(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         mrn = request.GET.get("mrn")
#         log_id = request.GET.get("log_id")
#
#         # Define the tables and their relevant fields
#         table_configs = [
#             {
#                 "table": "management_patientcoding",
#                 "fields": ["id",
#                     "mrn", "source_key", "source_name", "name",
#                     "ref_bill_code_set_name", "ref_bill_code"
#                 ],
#                 "filterable": ["mrn"]
#             },
#             {
#                 "table": "management_patienthistory",
#                 "fields": ["id", "mrn", "diagnosis_code", "dx_name"],
#                 "filterable": ["mrn"]
#             },
#             {
#                 "table": "management_patientinformation",
#                 "fields": ["id",
#                     "log_id", "mrn", "disch_disp_c", "disch_disp", "hosp_admsn_time",
#                     "hosp_disch_time", "los", "icu_admin_flag", "surgery_date",
#                     "birth_date", "height", "weight", "sex", "primary_anes_type_nm",
#                     "asa_rating_c", "asa_rating", "patient_class_group",
#                     "patient_class_nm", "primary_procedure_nm", "in_or_dttm",
#                     "out_or_dttm", "an_start_datetime", "an_stop_datetime"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientlabs",
#                 "fields": ["id",
#                     "log_id", "mrn", "enc_type_nm", "lab_code", "lab_name",
#                     "observation_value", "measurement_units", "reference_range",
#                     "abnormal_flag", "collection_datetime"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientmedication",
#                 "fields": ["id",
#                     "enc_type_c", "enc_type_nm", "log_id", "mrn", "ordering_date",
#                     "order_class_nm", "medication_id", "display_name", "medication_nm",
#                     "start_date", "end_date", "order_status_nm", "record_type",
#                     "mar_action_nm", "med_action_time", "admin_sig", "dose_unit_nm",
#                     "med_route_nm"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientlda",
#                 "fields": [
#                     "id", "log_id", "mrn", "description", "properties_display",
#                     "site", "placement_instant", "removal_instant", "flo_meas_name",
#                     "line_group_name"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientpostopcomplications",
#                 "fields": ["id",
#                     "log_id", "mrn", "element_name", "context_name",
#                     "element_abbr", "smrtdta_elem_value"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientprocedureevents",
#                 "fields": ["id","log_id", "mrn", "event_display_name", "event_time", "note_text"],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientvisit",
#                 "fields": ["id","log_id", "mrn", "diagnosis_code", "dx_name"],
#                 "filterable": ["mrn", "log_id"]
#             }
#         ]
#
#         # Build the SQL query with UNION ALL
#         queries = []
#         params = []
#         all_fields = [
#             "id", "mrn", "source_key", "source_name", "name", "ref_bill_code_set_name",
#             "ref_bill_code", "diagnosis_code", "dx_name", "log_id", "disch_disp_c",
#             "hosp_admsn_time", "hosp_disch_time", "los", "icu_admin_flag", "surgery_date",
#             "birth_date", "height", "weight", "sex", "primary_anes_type_nm",
#             "asa_rating_c", "asa_rating", "patient_class_group", "patient_class_nm",
#             "primary_procedure_nm", "in_or_dttm", "out_or_dttm", "an_start_datetime",
#             "an_stop_datetime", "enc_type_nm", "lab_code", "lab_name", "observation_value",
#             "measurement_units", "reference_range", "abnormal_flag", "collection_datetime",
#             "enc_type_c", "ordering_date", "order_class_nm", "medication_id",
#             "display_name", "medication_nm", "start_date", "end_date", "order_status_nm",
#             "record_type", "mar_action_nm", "med_action_time", "admin_sig",
#             "dose_unit_nm", "med_route_nm", "description", "properties_display",
#             "site", "placement_instant", "removal_instant", "flo_meas_name",
#             "line_group_name", "element_name", "context_name", "element_abbr",
#             "smrtdta_elem_value", "event_display_name", "event_time", "note_text"
#         ]
#
#         for config in table_configs:
#             table = config["table"]
#             table_fields = config["fields"]
#             filterable = config["filterable"]
#
#             # Build SELECT clause
#             select_fields = [f"{table}.{f} AS {f}" if f in table_fields else f"NULL AS {f}" for f in all_fields]
#             select_clause = ", ".join([f"'{table}' AS model_name"] + select_fields)
#
#             # Build WHERE clause
#             where_clauses = []
#             if mrn and "mrn" in filterable:
#                 where_clauses.append("mrn = %s")
#                 params.append(mrn)
#             if log_id and "log_id" in filterable:
#                 where_clauses.append("log_id = %s")
#                 params.append(log_id)
#
#             where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
#             query = f"SELECT {select_clause} FROM {table} WHERE {where_clause}"
#             queries.append(query)
#
#         # Combine queries with UNION ALL
#         final_query = " UNION ALL ".join(queries)
#
#         # Execute the query
#         with connection.cursor() as cursor:
#             cursor.execute(final_query, params)
#             rows = cursor.fetchall()
#
#         # Map rows to dictionaries
#         all_data = []
#         columns = ["model_name"] + all_fields
#         for row in rows:
#             results = dict(zip(columns, row))
#             all_data.append(results)
#
#         # Apply pagination
#         paginator = CustomPagination()
#         paginated_data = paginator.paginate_queryset(all_data, request)
#
#         return paginator.get_paginated_response(paginated_data)
#

#
# class SQLMRNFilterListAPIView(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         mrn = request.GET.get("mrn")
#         log_id = request.GET.get("log_id")
#
#         # Generate cache key
#         cache_key = f"mrn_filter:{mrn}:{log_id}"
#
#         # Try to get cached results
#         cached_data = cache.get(cache_key)
#         if cached_data:
#             return self._paginated_response(json.loads(cached_data), request)
#
#         # Define table configurations with indexes recommendation
#         table_configs = [
#             {
#                 "table": "management_patientcoding",
#                 "fields": ["id",
#                            "mrn", "source_key", "source_name", "name",
#                            "ref_bill_code_set_name", "ref_bill_code"
#                            ],
#                 "filterable": ["mrn"]
#             },
#             {
#                 "table": "management_patienthistory",
#                 "fields": ["id", "mrn", "diagnosis_code", "dx_name"],
#                 "filterable": ["mrn"]
#             },
#             {
#                 "table": "management_patientinformation",
#                 "fields": ["id",
#                            "log_id", "mrn", "disch_disp_c", "disch_disp", "hosp_admsn_time",
#                            "hosp_disch_time", "los", "icu_admin_flag", "surgery_date",
#                            "birth_date", "height", "weight", "sex", "primary_anes_type_nm",
#                            "asa_rating_c", "asa_rating", "patient_class_group",
#                            "patient_class_nm", "primary_procedure_nm", "in_or_dttm",
#                            "out_or_dttm", "an_start_datetime", "an_stop_datetime"
#                            ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientlabs",
#                 "fields": ["id",
#                            "log_id", "mrn", "enc_type_nm", "lab_code", "lab_name",
#                            "observation_value", "measurement_units", "reference_range",
#                            "abnormal_flag", "collection_datetime"
#                            ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientmedication",
#                 "fields": ["id",
#                            "enc_type_c", "enc_type_nm", "log_id", "mrn", "ordering_date",
#                            "order_class_nm", "medication_id", "display_name", "medication_nm",
#                            "start_date", "end_date", "order_status_nm", "record_type",
#                            "mar_action_nm", "med_action_time", "admin_sig", "dose_unit_nm",
#                            "med_route_nm"
#                            ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientlda",
#                 "fields": [
#                     "id", "log_id", "mrn", "description", "properties_display",
#                     "site", "placement_instant", "removal_instant", "flo_meas_name",
#                     "line_group_name"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientpostopcomplications",
#                 "fields": ["id",
#                            "log_id", "mrn", "element_name", "context_name",
#                            "element_abbr", "smrtdta_elem_value"
#                            ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientprocedureevents",
#                 "fields": ["id", "log_id", "mrn", "event_display_name", "event_time", "note_text"],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientvisit",
#                 "fields": ["id", "log_id", "mrn", "diagnosis_code", "dx_name"],
#                 "filterable": ["mrn", "log_id"]
#             }
#         ]

#         all_fields = [
#             "id", "mrn", "source_key", "source_name", "name", "ref_bill_code_set_name",
#             "ref_bill_code", "diagnosis_code", "dx_name", "log_id", "disch_disp_c",
#             "hosp_admsn_time", "hosp_disch_time", "los", "icu_admin_flag", "surgery_date",
#             "birth_date", "height", "weight", "sex", "primary_anes_type_nm",
#             "asa_rating_c", "asa_rating", "patient_class_group", "patient_class_nm",
#             "primary_procedure_nm", "in_or_dttm", "out_or_dttm", "an_start_datetime",
#             "an_stop_datetime", "enc_type_nm", "lab_code", "lab_name", "observation_value",
#             "measurement_units", "reference_range", "abnormal_flag", "collection_datetime",
#             "enc_type_c", "ordering_date", "order_class_nm", "medication_id",
#             "display_name", "medication_nm", "start_date", "end_date", "order_status_nm",
#             "record_type", "mar_action_nm", "med_action_time", "admin_sig",
#             "dose_unit_nm", "med_route_nm", "description", "properties_display",
#             "site", "placement_instant", "removal_instant", "flo_meas_name",
#             "line_group_name", "element_name", "context_name", "element_abbr",
#             "smrtdta_elem_value", "event_display_name", "event_time", "note_text"
#         ]

#         queries = []
#         params = []
#
#         # Optimize query construction
#         for config in table_configs:
#             if not mrn and not log_id:
#                 continue  # Skip if no filters provided
#
#             table = config["table"]
#             table_fields = config["fields"]
#             filterable = config["filterable"]
#
#             # Only include tables that can be filtered by provided parameters
#             if (mrn and "mrn" not in filterable) or (log_id and "log_id" not in filterable):
#                 continue
#
#             # Build SELECT clause with minimal fields
#             select_fields = [
#                 f"{table}.{f}" if f in table_fields else f"NULL AS {f}"
#                 for f in all_fields
#             ]
#             select_clause = ", ".join([f"'{table}' AS model_name"] + select_fields)
#
#             # Build WHERE clause with parameter binding
#             where_clauses = []
#             if mrn and "mrn" in filterable:
#                 where_clauses.append("mrn = %s")
#                 params.append(mrn)
#             if log_id and "log_id" in filterable:
#                 where_clauses.append("log_id = %s")
#                 params.append(log_id)
#
#             if not where_clauses:
#                 continue
#
#             where_clause = " AND ".join(where_clauses)
#             query = f"SELECT {select_clause} FROM {table} WHERE {where_clause}"
#             queries.append(f"({query})")
#
#         if not queries:
#             return self._paginated_response([], request)
#
#         # Combine queries with UNION ALL
#         final_query = " UNION ALL ".join(queries)
#
#         # Execute query with connection pooling
#         with connection.cursor() as cursor:
#             cursor.execute(final_query, params)
#             columns = ["model_name"] + all_fields
#             all_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#
#         # Cache results (store for 1 hour)
#         cache.set(cache_key, json.dumps(all_data), timeout=3600)
#
#         return self._paginated_response(all_data, request)
#
#     def _paginated_response(self, data, request):
#         paginator = CustomPagination()
#         paginated_data = paginator.paginate_queryset(data, request)
#         return paginator.get_paginated_response(paginated_data)


class SQLMRNFilterListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        mrn = request.GET.get("mrn")
        log_id = request.GET.get("log_id")

        # Generate cache key
        cache_key = f"mrn_filter:{mrn or 'none'}:{log_id or 'none'}:{'no_filter' if not mrn and not log_id else 'filtered'}"

        # Try quick cache (local memory)
        try:
            quick_cache = caches['quick']
            cached_data = quick_cache.get(cache_key)
            if cached_data:
                logger.debug(f"Cache hit (quick): {cache_key}")
                return self._paginated_response(json.loads(cached_data), request)
        except Exception as e:
            logger.warning(f"Quick cache error: {e}")

        # Fallback to default cache (Memcached)
        try:
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.debug(f"Cache hit (default): {cache_key}")
                quick_cache.set(cache_key, cached_data, timeout=300)
                return self._paginated_response(json.loads(cached_data), request)
        except Exception as e:
            logger.warning(f"Default cache error: {e}")

        # Table configurations
        table_configs = [
            {
                "table": "management_patientcoding",
                "fields": ["id", "mrn", "source_key", "source_name", "name",
                           "ref_bill_code_set_name", "ref_bill_code"],
                "filterable": ["mrn"]
            },
            {
                "table": "management_patienthistory",
                "fields": ["id", "mrn", "diagnosis_code", "dx_name"],
                "filterable": ["mrn"]
            },
            {
                "table": "management_patientinformation",
                "fields": ["id", "log_id", "mrn", "disch_disp_c", "disch_disp", "hosp_admsn_time",
                           "hosp_disch_time", "los", "icu_admin_flag", "surgery_date",
                           "birth_date", "height", "weight", "sex", "primary_anes_type_nm",
                           "asa_rating_c", "asa_rating", "patient_class_group",
                           "patient_class_nm", "primary_procedure_nm", "in_or_dttm",
                           "out_or_dttm", "an_start_datetime", "an_stop_datetime"],
                "filterable": ["mrn", "log_id"]
            },
            {
                "table": "management_patientlabs",
                "fields": ["id", "log_id", "mrn", "enc_type_nm", "lab_code", "lab_name",
                           "observation_value", "measurement_units", "reference_range",
                           "abnormal_flag", "collection_datetime"],
                "filterable": ["mrn", "log_id"]
            },
            {
                "table": "management_patientmedication",
                "fields": ["id", "enc_type_c", "enc_type_nm", "log_id", "mrn", "ordering_date",
                           "order_class_nm", "medication_id", "display_name", "medication_nm",
                           "start_date", "end_date", "order_status_nm", "record_type",
                           "mar_action_nm", "med_action_time", "admin_sig", "dose_unit_nm",
                           "med_route_nm"],
                "filterable": ["mrn", "log_id"]
            },
            {
                "table": "management_patientlda",
                "fields": ["id", "log_id", "mrn", "description", "properties_display",
                           "site", "placement_instant", "removal_instant", "flo_meas_name",
                           "line_group_name"],
                "filterable": ["mrn", "log_id"]
            },
            {
                "table": "management_patientpostopcomplications",
                "fields": ["id", "log_id", "mrn", "element_name", "context_name",
                           "element_abbr", "smrtdta_elem_value"],
                "filterable": ["mrn", "log_id"]
            },
            {
                "table": "management_patientprocedureevents",
                "fields": ["id", "log_id", "mrn", "event_display_name", "event_time", "note_text"],
                "filterable": ["mrn", "log_id"]
            },
            {
                "table": "management_patientvisit",
                "fields": ["id", "log_id", "mrn", "diagnosis_code", "dx_name"],
                "filterable": ["mrn", "log_id"]
            }
        ]

        all_fields = [
            "id", "mrn", "source_key", "source_name", "name", "ref_bill_code_set_name",
            "ref_bill_code", "diagnosis_code", "dx_name", "log_id", "disch_disp_c",
            "hosp_admsn_time", "hosp_disch_time", "los", "icu_admin_flag", "surgery_date",
            "birth_date", "height", "weight", "sex", "primary_anes_type_nm",
            "asa_rating_c", "asa_rating", "patient_class_group", "patient_class_nm",
            "primary_procedure_nm", "in_or_dttm", "out_or_dttm", "an_start_datetime",
            "an_stop_datetime", "enc_type_nm", "lab_code", "lab_name", "observation_value",
            "measurement_units", "reference_range", "abnormal_flag", "collection_datetime",
            "enc_type_c", "ordering_date", "order_class_nm", "medication_id",
            "display_name", "medication_nm", "start_date", "end_date", "order_status_nm",
            "record_type", "mar_action_nm", "med_action_time", "admin_sig",
            "dose_unit_nm", "med_route_nm", "description", "properties_display",
            "site", "placement_instant", "removal_instant", "flo_meas_name",
            "line_group_name", "element_name", "context_name", "element_abbr",
            "smrtdta_elem_value", "event_display_name", "event_time", "note_text"
        ]

        queries = []
        params = []

        # Build queries
        for config in table_configs:
            table = config["table"]
            table_fields = config["fields"]
            filterable = config["filterable"]

            # Skip tables that require specific filters when those filters are provided
            if mrn and "mrn" not in filterable:
                continue
            if log_id and "log_id" not in filterable and not mrn:
                continue

            select_fields = [
                f"{table}.{f}" if f in table_fields else f"NULL AS {f}"
                for f in all_fields
            ]
            select_clause = ", ".join([f"'{table}' AS model_name"] + select_fields)

            where_clauses = []
            if mrn and "mrn" in filterable:
                where_clauses.append("mrn = %s")
                params.append(mrn)
            if log_id and "log_id" in filterable:
                where_clauses.append("log_id = %s")
                params.append(log_id)

            # If no filters, select all records from the table
            where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
            query = f"SELECT {select_clause} FROM {table} WHERE {where_clause}"
            queries.append(query)

        if not queries:
            logger.warning("No valid queries generated")
            return self._paginated_response([], request)

        # Execute query
        try:
            final_query = " UNION ALL ".join(queries)
            logger.debug(f"Executing query: {final_query} with params: {params}")
            with connection.cursor() as cursor:
                cursor.execute(final_query, params)
                columns = ["model_name"] + all_fields
                all_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                logger.debug(f"Retrieved {len(all_data)} records")
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return self._paginated_response([], request)

        # Cache results
        try:
            serialized_data = json.dumps(all_data, default=str)
            cache.set(cache_key, serialized_data, timeout=3600)
            quick_cache.set(cache_key, serialized_data, timeout=300)
            logger.debug(f"Cache set: {cache_key}")
        except Exception as e:
            logger.warning(f"Cache set error: {e}")

        return self._paginated_response(all_data, request)

    def _paginated_response(self, data, request):
        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(data, request)
        return paginator.get_paginated_response(paginated_data)



import logging

logger = logging.getLogger(__name__)


class MRNMergeDataView(APIView):
    permission_classes = (AllowAny,)
    """
    Optimized view to filter and merge patient data by MRN and log_id with pagination
    """

    def get(self, request):
        mrn = request.query_params.get('mrn')
        log_id = request.query_params.get('log_id')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        try:
            # Use raw SQL for better performance
            merged_data = self.get_merged_patient_data_optimized(mrn, log_id, page, page_size)
            total_count = self.get_total_count(mrn, log_id)

            if not merged_data and total_count == 0:
                return Response(
                    {"message": "No data found for the given parameters"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Calculate pagination info
            total_pages = (total_count + page_size - 1) // page_size
            has_next = page < total_pages
            has_previous = page > 1

            return Response({
                "count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_previous": has_previous,
                "filters_applied": {
                    "mrn": mrn,
                    "log_id": log_id
                },
                "results": merged_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in MRNMergeDataView: {str(e)}")
            return Response(
                {"error": "An error occurred while processing your request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_total_count(self, mrn=None, log_id=None):
        """Get total count using optimized queries"""
        total = 0

        # Build WHERE clauses
        mrn_condition = f"mrn = '{mrn}'" if mrn else "1=1"
        log_condition = f"log_id = '{log_id}'" if log_id else "1=1"

        with connection.cursor() as cursor:
            # Count from tables without log_id (only filter by MRN if provided)
            if not log_id or mrn:  # If no log_id filter or MRN is provided
                cursor.execute(f"SELECT COUNT(*) FROM management_patientcoding WHERE {mrn_condition}")
                total += cursor.fetchone()[0]

                cursor.execute(f"SELECT COUNT(*) FROM management_patienthistory WHERE {mrn_condition}")
                total += cursor.fetchone()[0]

            # Count from tables with log_id
            if mrn and log_id:
                condition = f"{mrn_condition} AND {log_condition}"
            elif mrn:
                condition = mrn_condition
            elif log_id:
                condition = log_condition
            else:
                condition = "1=1"

            tables_with_log_id = [
                'management_patientlabs',
                'management_patientlda',
                'management_patientpostcomplications',
                'management_patientprocedureevents',
                'management_patientvisit',
                'management_patientmedication',
                'management_patientinformation'
            ]

            for table in tables_with_log_id:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {condition}")
                total += cursor.fetchone()[0]

        return total

    def get_merged_patient_data_optimized(self, mrn=None, log_id=None, page=1, page_size=20):
        """
        Optimized method using raw SQL with UNION ALL for better performance
        """
        offset = (page - 1) * page_size

        # Build WHERE clauses with SQL injection protection
        mrn_condition = "mrn = %s" if mrn else "1=1"
        log_condition = "log_id = %s" if log_id else "1=1"

        queries = []
        params = []

        # Build condition for tables with log_id
        if mrn and log_id:
            log_condition_full = f"{mrn_condition} AND {log_condition}"
            log_params = [mrn, log_id]
        elif mrn:
            log_condition_full = mrn_condition
            log_params = [mrn]
        elif log_id:
            log_condition_full = log_condition
            log_params = [log_id]
        else:
            log_condition_full = "1=1"
            log_params = []

        # Tables without log_id - only filter by MRN if provided
        if not log_id or mrn:
            # PatientCoding table mapping
            coding_query, coding_params = self.build_optimized_query_for_table(
                'management_patientcoding',
                {
                    'id': 'id', 'mrn': 'mrn', 'source_key': 'source_key',
                    'source_name': 'source_name', 'name': 'name',
                    'ref_bill_code_set_name': 'ref_bill_code_set_name',
                    'ref_bill_code': 'ref_bill_code'
                },
                mrn_condition if mrn else "1=1",
                'coding'
            )
            queries.append(coding_query)
            params.extend(coding_params)

            # PatientHistory table mapping
            history_query, history_params = self.build_optimized_query_for_table(
                'management_patienthistory',
                {
                    'id': 'id', 'mrn': 'mrn', 'diagnosis_code': 'diagnosis_code',
                    'dx_name': 'dx_name'
                },
                mrn_condition if mrn else "1=1",
                'history'
            )
            queries.append(history_query)
            params.extend(history_params)

        # PatientLabs table mapping
        labs_query, labs_params = self.build_optimized_query_for_table(
            'management_patientlabs',
            {
                'id': 'id', 'log_id': 'log_id', 'mrn': 'mrn', 'enc_type_nm': 'enc_type_nm',
                'lab_code': 'lab_code', 'lab_name': 'lab_name', 'observation_value': 'observation_value',
                'measurement_units': 'measurement_units', 'reference_range': 'reference_range',
                'abnormal_flag': 'abnormal_flag', 'collection_datetime': 'collection_datetime'
            },
            log_condition_full,
            'labs'
        )
        queries.append(labs_query)
        params.extend(labs_params)

        # PatientLDA table mapping
        lda_query, lda_params = self.build_optimized_query_for_table(
            'management_patientlda',
            {
                'id': 'id', 'log_id': 'log_id', 'mrn': 'mrn', 'description': 'description',
                'properties_display': 'properties_display', 'site': 'site',
                'placement_instant': 'placement_instant', 'removal_instant': 'removal_instant',
                'flo_meas_name': 'flo_meas_name', 'line_group_name': 'line_group_name'
            },
            log_condition_full,
            'lda'
        )
        queries.append(lda_query)
        params.extend(lda_params)

        # PatientPostOPComplications table mapping
        complications_query, complications_params = self.build_optimized_query_for_table(
            'management_patientpostcomplications',
            {
                'id': 'id', 'log_id': 'log_id', 'mrn': 'mrn', 'element_name': 'element_name',
                'context_name': 'context_name', 'element_abbr': 'element_abbr',
                'smrtdta_elem_value': 'smrtdta_elem_value'
            },
            log_condition_full,
            'complications'
        )
        queries.append(complications_query)
        params.extend(complications_params)

        # PatientProcedureEvents table mapping
        procedure_query, procedure_params = self.build_optimized_query_for_table(
            'management_patientprocedureevents',
            {
                'id': 'id', 'log_id': 'log_id', 'mrn': 'mrn', 'event_display_name': 'event_display_name',
                'event_time': 'event_time', 'note_text': 'note_text'
            },
            log_condition_full,
            'procedure_events'
        )
        queries.append(procedure_query)
        params.extend(procedure_params)

        # PatientVisit table mapping
        visit_query, visit_params = self.build_optimized_query_for_table(
            'management_patientvisit',
            {
                'id': 'id', 'log_id': 'log_id', 'mrn': 'mrn', 'diagnosis_code': 'diagnosis_code',
                'dx_name': 'dx_name'
            },
            log_condition_full,
            'visit'
        )
        queries.append(visit_query)
        params.extend(visit_params)

        # PatientMedication table mapping
        medication_query, medication_params = self.build_optimized_query_for_table(
            'management_patientmedication',
            {
                'id': 'id', 'enc_type_c': 'enc_type_c', 'enc_type_nm': 'enc_type_nm',
                'log_id': 'log_id', 'mrn': 'mrn', 'ordering_date': 'ordering_date',
                'order_class_nm': 'order_class_nm', 'medication_id': 'medication_id',
                'display_name': 'display_name', 'medication_nm': 'medication_nm',
                'start_date': 'start_date', 'end_date': 'end_date', 'order_status_nm': 'order_status_nm',
                'record_type': 'record_type', 'mar_action_nm': 'mar_action_nm',
                'med_action_time': 'med_action_time', 'admin_sig': 'admin_sig',
                'dose_unit_nm': 'dose_unit_nm', 'med_route_nm': 'med_route_nm'
            },
            log_condition_full,
            'medication'
        )
        queries.append(medication_query)
        params.extend(medication_params)

        # PatientInformation table mapping
        info_query, info_params = self.build_optimized_query_for_table(
            'management_patientinformation',
            {
                'id': 'id', 'log_id': 'log_id', 'mrn': 'mrn', 'disch_disp_c': 'disch_disp_c',
                'hosp_admsn_time': 'hosp_admsn_time', 'hosp_disch_time': 'hosp_disch_time',
                'los': 'los', 'icu_admin_flag': 'icu_admin_flag', 'surgery_date': 'surgery_date',
                'birth_date': 'birth_date', 'height': 'height', 'weight': 'weight', 'sex': 'sex',
                'primary_anes_type_nm': 'primary_anes_type_nm', 'asa_rating_c': 'asa_rating_c',
                'asa_rating': 'asa_rating', 'patient_class_group': 'patient_class_group',
                'patient_class_nm': 'patient_class_nm', 'primary_procedure_nm': 'primary_procedure_nm',
                'in_or_dttm': 'in_or_dttm', 'out_or_dttm': 'out_or_dttm',
                'an_start_datetime': 'an_start_datetime', 'an_stop_datetime': 'an_stop_datetime'
            },
            log_condition_full,
            'information'
        )
        queries.append(info_query)
        params.extend(info_params)

        # Combine all queries with UNION ALL
        final_query = " UNION ALL ".join(queries)
        final_query += f" ORDER BY id LIMIT %s OFFSET %s"
        params.extend([page_size, offset])

        results = []
        with connection.cursor() as cursor:
            cursor.execute(final_query, params)
            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

        return results

    def build_optimized_query_for_table(self, table_name, fields_mapping, condition, record_type):
        """
        Helper method to build optimized query for each table
        Maps actual table fields to the standardized output format
        """
        # Define all possible output fields in the standardized format
        all_fields = [
            'id', 'mrn', 'source_key', 'source_name', 'name', 'ref_bill_code_set_name',
            'ref_bill_code', 'diagnosis_code', 'dx_name', 'log_id', 'disch_disp_c',
            'hosp_admsn_time', 'hosp_disch_time', 'los', 'icu_admin_flag', 'surgery_date',
            'birth_date', 'height', 'weight', 'sex', 'primary_anes_type_nm', 'asa_rating_c',
            'asa_rating', 'patient_class_group', 'patient_class_nm', 'primary_procedure_nm',
            'in_or_dttm', 'out_or_dttm', 'an_start_datetime', 'an_stop_datetime',
            'enc_type_nm', 'lab_code', 'lab_name', 'observation_value', 'measurement_units',
            'reference_range', 'abnormal_flag', 'collection_datetime', 'enc_type_c',
            'ordering_date', 'order_class_nm', 'medication_id', 'display_name',
            'medication_nm', 'start_date', 'end_date', 'order_status_nm', 'record_type',
            'mar_action_nm', 'med_action_time', 'admin_sig', 'dose_unit_nm', 'med_route_nm',
            'description', 'properties_display', 'site', 'placement_instant', 'removal_instant',
            'flo_meas_name', 'line_group_name', 'element_name', 'context_name', 'element_abbr',
            'smrtdta_elem_value', 'event_display_name', 'event_time', 'note_text'
        ]

        # Build SELECT clause mapping actual fields to standardized names
        select_parts = []
        for field in all_fields:
            if field in fields_mapping:
                # Use the actual field from the table
                select_parts.append(f"{fields_mapping[field]} as {field}")
            else:
                # Use NULL for fields that don't exist in this table
                select_parts.append(f"NULL as {field}")

        # Add record type source field
        select_parts.append(f"'{record_type}' as record_type_source")

        # Build the complete SELECT statement
        select_clause = ", ".join(select_parts)

        # Build the complete query
        query = f"""
            SELECT {select_clause}
            FROM {table_name}
            WHERE {condition}
        """

        # Determine parameters based on condition
        params = []
        if condition != "1=1":
            # Count the number of %s placeholders in the condition
            param_count = condition.count('%s')
            if param_count == 1:
                # Single parameter (either mrn or log_id)
                if 'mrn' in condition:
                    params = [self.current_mrn] if hasattr(self, 'current_mrn') else []
                elif 'log_id' in condition:
                    params = [self.current_log_id] if hasattr(self, 'current_log_id') else []
            elif param_count == 2:
                # Two parameters (both mrn and log_id)
                params = [self.current_mrn, self.current_log_id] if hasattr(self, 'current_mrn') and hasattr(self,
                                                                                                             'current_log_id') else []

        return query, params


#
#
# class SQLMRNFilterListAPIView(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         # Extract query parameters
#         mrn = request.GET.get("mrn")
#         log_id = request.GET.get("log_id")
#         diagnosis_code = request.GET.get("diagnosis_code")
#
#         # Define the tables and their relevant fields
#         table_configs = [
#             {
#                 "table": "management_patientcoding",
#                 "fields": [
#                     "id", "mrn", "source_key", "source_name", "name",
#                     "ref_bill_code_set_name", "ref_bill_code"
#                 ],
#                 "filterable": ["mrn", "diagnosis_code"]
#             },
#             {
#                 "table": "management_patienthistory",
#                 "fields": ["id", "mrn", "diagnosis_code", "dx_name"],
#                 "filterable": ["mrn", "diagnosis_code"]
#             },
#             {
#                 "table": "management_patientinformation",
#                 "fields": [
#                     "id", "log_id", "mrn", "disch_disp_c", "disch_disp", "hosp_admsn_time",
#                     "hosp_disch_time", "los", "icu_admin_flag", "surgery_date",
#                     "birth_date", "height", "weight", "sex", "primary_anes_type_nm",
#                     "asa_rating_c", "asa_rating", "patient_class_group",
#                     "patient_class_nm", "primary_procedure_nm", "in_or_dttm",
#                     "out_or_dttm", "an_start_datetime", "an_stop_datetime"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientlabs",
#                 "fields": [
#                     "id", "log_id", "mrn", "enc_type_nm", "lab_code", "lab_name",
#                     "observation_value", "measurement_units", "reference_range",
#                     "abnormal_flag", "collection_datetime"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientmedication",
#                 "fields": [
#                     "id", "enc_type_c", "enc_type_nm", "log_id", "mrn", "ordering_date",
#                     "order_class_nm", "medication_id", "display_name", "medication_nm",
#                     "start_date", "end_date", "order_status_nm", "record_type",
#                     "mar_action_nm", "med_action_time", "admin_sig", "dose_unit_nm",
#                     "med_route_nm"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientlda",
#                 "fields": [
#                     "id", "log_id", "mrn", "description", "properties_display",
#                     "site", "placement_instant", "removal_instant", "flo_meas_name",
#                     "line_group_name"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientpostopcomplications",
#                 "fields": [
#                     "id", "log_id", "mrn", "element_name", "context_name",
#                     "element_abbr", "smrtdta_elem_value"
#                 ],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientprocedureevents",
#                 "fields": ["id", "log_id", "mrn", "event_display_name", "event_time", "note_text"],
#                 "filterable": ["mrn", "log_id"]
#             },
#             {
#                 "table": "management_patientvisit",
#                 "fields": ["id", "log_id", "mrn", "diagnosis_code", "dx_name"],
#                 "filterable": ["mrn", "log_id", "diagnosis_code"]
#             }
#         ]
#
#         # Define all possible fields for the result
#         all_fields = [
#             "id", "mrn", "source_key", "source_name", "name", "ref_bill_code_set_name",
#             "ref_bill_code", "diagnosis_code", "dx_name", "log_id", "disch_disp_c",
#             "hosp_admsn_time", "hosp_disch_time", "los", "icu_admin_flag", "surgery_date",
#             "birth_date", "height", "weight", "sex", "primary_anes_type_nm",
#             "asa_rating_c", "asa_rating", "patient_class_group", "patient_class_nm",
#             "primary_procedure_nm", "in_or_dttm", "out_or_dttm", "an_start_datetime",
#             "an_stop_datetime", "enc_type_nm", "lab_code", "lab_name", "observation_value",
#             "measurement_units", "reference_range", "abnormal_flag", "collection_datetime",
#             "enc_type_c", "ordering_date", "order_class_nm", "medication_id",
#             "display_name", "medication_nm", "start_date", "end_date", "order_status_nm",
#             "record_type", "mar_action_nm", "med_action_time", "admin_sig",
#             "dose_unit_nm", "med_route_nm", "description", "properties_display",
#             "site", "placement_instant", "removal_instant", "flo_meas_name",
#             "line_group_name", "element_name", "context_name", "element_abbr",
#             "smrtdta_elem_value", "event_display_name", "event_time", "note_text"
#         ]
#
#         # Build queries based on filters
#         queries = []
#         params = []
#
#         # Check which filters are provided
#         filters = {}
#         if mrn:
#             filters["mrn"] = mrn
#         if log_id:
#             filters["log_id"] = log_id
#         if diagnosis_code:
#             filters["diagnosis_code"] = diagnosis_code
#
#         for config in table_configs:
#             table = config["table"]
#             table_fields = config["fields"]
#             filterable = config["filterable"]
#
#             # Include all tables if no filters are provided, or only tables that support the provided filters
#             if not filters or any(f in filterable for f in filters):
#                 # Build SELECT clause with only the fields available in the table
#                 select_fields = [
#                     f"{table}.{f}" if f in table_fields else f"NULL AS {f}"
#                     for f in all_fields
#                 ]
#                 select_clause = ", ".join([f"'{table}' AS model_name"] + select_fields)
#
#                 # Build WHERE clause
#                 where_clauses = []
#                 for filter_name, filter_value in filters.items():
#                     if filter_name in filterable:
#                         # Use case-insensitive filtering for string fields
#                         if filter_name in ["mrn", "diagnosis_code"]:
#                             where_clauses.append(f"LOWER({filter_name}) = LOWER(%s)")
#                         else:
#                             where_clauses.append(f"{filter_name} = %s")
#                         params.append(filter_value)
#
#                 where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
#                 query = f"SELECT {select_clause} FROM {table} WHERE {where_clause}"
#                 queries.append(query)
#
#         # Handle case where no queries are generated
#         if not queries:
#             return Response({"detail": "No tables support the provided filters"}, status=400)
#
#         # Combine queries with UNION ALL
#         final_query = " UNION ALL ".join(queries)
#
#         # Execute the query
#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute(final_query, params)
#                 rows = cursor.fetchall()
#                 print(f"Rows fetched: {len(rows)}")  # Debug row count
#         except Exception as e:
#             print(f"Query error: {str(e)}")  # Debug query error
#             return Response({"detail": f"Query execution failed: {str(e)}"}, status=500)
#
#         # Map rows to dictionaries
#         all_data = []
#         columns = ["model_name"] + all_fields
#         for row in rows:
#             results = dict(zip(columns, row))
#             all_data.append(results)
#
#         # Apply pagination
#         paginator = CustomPagination()
#         paginated_data = paginator.paginate_queryset(all_data, request)
#
#         return paginator.get_paginated_response(paginated_data)
#

def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class DBMRNFilterListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        mrn = request.GET.get("mrn")
        log_id = request.GET.get("log_id")

        if not mrn and not log_id:
            return JsonResponse({"error": "Either mrn or log_id parameter is required"}, status=400)

        # Build the unified SQL query using UNION ALL
        sql_parts = []
        params = []

        # PatientCoding query
        if mrn:
            sql_parts.append("""
                SELECT 'PatientCoding' as model_name, id, mrn, source_key, source_name, name, 
                       ref_bill_code_set_name, ref_bill_code,
                       NULL as diagnosis_code, NULL as dx_name, NULL as log_id,
                       NULL as disch_disp_c, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                       NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date,
                       NULL as height, NULL as weight, NULL as sex, NULL as primary_anes_type_nm,
                       NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                       NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm,
                       NULL as out_or_dttm, NULL as an_start_datetime, NULL as an_stop_datetime,
                       NULL as enc_type_nm, NULL as lab_code, NULL as lab_name, NULL as observation_value,
                       NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                       NULL as collection_datetime, NULL as enc_type_c, NULL as ordering_date,
                       NULL as order_class_nm, NULL as medication_id, NULL as display_name,
                       NULL as medication_nm, NULL as start_date, NULL as end_date, NULL as order_status_nm,
                       NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                       NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm,
                       NULL as description, NULL as properties_display, NULL as site,
                       NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name,
                       NULL as line_group_name, NULL as element_name, NULL as context_name,
                       NULL as element_abbr, NULL as smrtdta_elem_value, NULL as event_display_name,
                       NULL as event_time, NULL as note_text
                FROM management_patientcoding WHERE UPPER(mrn) = UPPER(%s)
            """)
            params.append(mrn)

        # PatientHistory query
        if mrn:
            sql_parts.append("""
                SELECT 'PatientHistory' as model_name, id, mrn, NULL as source_key, NULL as source_name, 
                       NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                       diagnosis_code, dx_name, NULL as log_id,
                       NULL as disch_disp_c, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                       NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date,
                       NULL as height, NULL as weight, NULL as sex, NULL as primary_anes_type_nm,
                       NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                       NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm,
                       NULL as out_or_dttm, NULL as an_start_datetime, NULL as an_stop_datetime,
                       NULL as enc_type_nm, NULL as lab_code, NULL as lab_name, NULL as observation_value,
                       NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                       NULL as collection_datetime, NULL as enc_type_c, NULL as ordering_date,
                       NULL as order_class_nm, NULL as medication_id, NULL as display_name,
                       NULL as medication_nm, NULL as start_date, NULL as end_date, NULL as order_status_nm,
                       NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                       NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm,
                       NULL as description, NULL as properties_display, NULL as site,
                       NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name,
                       NULL as line_group_name, NULL as element_name, NULL as context_name,
                       NULL as element_abbr, NULL as smrtdta_elem_value, NULL as event_display_name,
                       NULL as event_time, NULL as note_text
                FROM management_patienthistory WHERE UPPER(mrn) = UPPER(%s)
            """)
            params.append(mrn)

        # PatientInformation query
        where_conditions = []
        if mrn:
            where_conditions.append("UPPER(mrn) = UPPER(%s)")
            params.append(mrn)
        if log_id:
            where_conditions.append("UPPER(log_id) = UPPER(%s)")
            params.append(log_id)

        if where_conditions:
            sql_parts.append(f"""
                SELECT 'PatientInformation' as model_name, id, mrn, NULL as source_key, NULL as source_name,
                       NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                       NULL as diagnosis_code, NULL as dx_name, log_id, disch_disp_c, hosp_admsn_time,
                       hosp_disch_time, los, icu_admin_flag, surgery_date, birth_date, height, weight,
                       sex, primary_anes_type_nm, asa_rating_c, asa_rating, patient_class_group,
                       patient_class_nm, primary_procedure_nm, in_or_dttm, out_or_dttm,
                       an_start_datetime, an_stop_datetime, NULL as enc_type_nm, NULL as lab_code,
                       NULL as lab_name, NULL as observation_value, NULL as measurement_units,
                       NULL as reference_range, NULL as abnormal_flag, NULL as collection_datetime,
                       NULL as enc_type_c, NULL as ordering_date, NULL as order_class_nm,
                       NULL as medication_id, NULL as display_name, NULL as medication_nm,
                       NULL as start_date, NULL as end_date, NULL as order_status_nm,
                       NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                       NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm,
                       NULL as description, NULL as properties_display, NULL as site,
                       NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name,
                       NULL as line_group_name, NULL as element_name, NULL as context_name,
                       NULL as element_abbr, NULL as smrtdta_elem_value, NULL as event_display_name,
                       NULL as event_time, NULL as note_text
                FROM management_patientinformation WHERE {' AND '.join(where_conditions)}
            """)

        # Continue with other models following the same pattern...
        # PatientLabs
        where_conditions = []
        temp_params = []
        if mrn:
            where_conditions.append("UPPER(mrn) = UPPER(%s)")
            temp_params.append(mrn)
        if log_id:
            where_conditions.append("UPPER(log_id) = UPPER(%s)")
            temp_params.append(log_id)

        if where_conditions:
            sql_parts.append(f"""
                SELECT 'PatientLabs' as model_name, id, mrn, NULL as source_key, NULL as source_name,
                       NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                       NULL as diagnosis_code, NULL as dx_name, log_id, NULL as disch_disp_c,
                       NULL as hosp_admsn_time, NULL as hosp_disch_time, NULL as los,
                       NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date,
                       NULL as height, NULL as weight, NULL as sex, NULL as primary_anes_type_nm,
                       NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                       NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm,
                       NULL as out_or_dttm, NULL as an_start_datetime, NULL as an_stop_datetime,
                       enc_type_nm, lab_code, lab_name, observation_value, measurement_units,
                       reference_range, abnormal_flag, collection_datetime, NULL as enc_type_c,
                       NULL as ordering_date, NULL as order_class_nm, NULL as medication_id,
                       NULL as display_name, NULL as medication_nm, NULL as start_date,
                       NULL as end_date, NULL as order_status_nm, NULL as record_type,
                       NULL as mar_action_nm, NULL as med_action_time, NULL as admin_sig,
                       NULL as dose_unit_nm, NULL as med_route_nm, NULL as description,
                       NULL as properties_display, NULL as site, NULL as placement_instant,
                       NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                       NULL as element_name, NULL as context_name, NULL as element_abbr,
                       NULL as smrtdta_elem_value, NULL as event_display_name,
                       NULL as event_time, NULL as note_text
                FROM management_patientlabs WHERE {' AND '.join(where_conditions)}
            """)
            params.extend(temp_params)

        # Add similar queries for remaining models...
        # For brevity, I'll show one more example and indicate the pattern

        # PatientMedication
        where_conditions = []
        temp_params = []
        if mrn:
            where_conditions.append("UPPER(mrn) = UPPER(%s)")
            temp_params.append(mrn)
        if log_id:
            where_conditions.append("UPPER(log_id) = UPPER(%s)")
            temp_params.append(log_id)

        if where_conditions:
            sql_parts.append(f"""
                SELECT 'PatientMedication' as model_name, id, mrn, NULL as source_key, NULL as source_name,
                       NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                       NULL as diagnosis_code, NULL as dx_name, log_id, NULL as disch_disp_c,
                       NULL as hosp_admsn_time, NULL as hosp_disch_time, NULL as los,
                       NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date,
                       NULL as height, NULL as weight, NULL as sex, NULL as primary_anes_type_nm,
                       NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                       NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm,
                       NULL as out_or_dttm, NULL as an_start_datetime, NULL as an_stop_datetime,
                       enc_type_nm, NULL as lab_code, NULL as lab_name, NULL as observation_value,
                       NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                       NULL as collection_datetime, enc_type_c, ordering_date, order_class_nm,
                       medication_id, display_name, medication_nm, start_date, end_date,
                       order_status_nm, record_type, mar_action_nm, med_action_time,
                       admin_sig, dose_unit_nm, med_route_nm, NULL as description,
                       NULL as properties_display, NULL as site, NULL as placement_instant,
                       NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                       NULL as element_name, NULL as context_name, NULL as element_abbr,
                       NULL as smrtdta_elem_value, NULL as event_display_name,
                       NULL as event_time, NULL as note_text
                FROM management_patientmedication WHERE {' AND '.join(where_conditions)}
            """)
            params.extend(temp_params)

        if not sql_parts:
            return JsonResponse({"results": [], "count": 0}, status=200)

        # Combine all queries with UNION ALL
        final_query = " UNION ALL ".join(sql_parts)

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(final_query, params)
            results = dictfetchall(cursor)

        # Apply pagination
        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(results, request)

        return paginator.get_paginated_response(paginated_data)


# Alternative approach: Separate optimized queries (if UNION ALL becomes too complex)
class MRNFilterListAPIViewSeparate(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        mrn = request.GET.get("mrn")
        log_id = request.GET.get("log_id")

        if not mrn and not log_id:
            return JsonResponse({"error": "Either mrn or log_id parameter is required"}, status=400)

        all_data = []

        # Define model queries with their specific fields
        model_queries = [
            {
                'model_name': 'PatientCoding',
                'table': 'management_patientcoding',
                'has_mrn': True,
                'has_log_id': False,
                'fields': ['id', 'mrn', 'source_key', 'source_name', 'name', 'ref_bill_code_set_name', 'ref_bill_code']
            },
            {
                'model_name': 'PatientHistory',
                'table': 'management_patienthistory',
                'has_mrn': True,
                'has_log_id': False,
                'fields': ['id', 'mrn', 'diagnosis_code', 'dx_name']
            },
            {
                'model_name': 'PatientInformation',
                'table': 'management_patientinformation',
                'has_mrn': True,
                'has_log_id': True,
                'fields': ['id', 'log_id', 'mrn', 'disch_disp_c', 'disch_disp', 'hosp_admsn_time',
                           'hosp_disch_time', 'los', 'icu_admin_flag', 'surgery_date', 'birth_date',
                           'height', 'weight', 'sex', 'primary_anes_type_nm', 'asa_rating_c',
                           'asa_rating', 'patient_class_group', 'patient_class_nm', 'primary_procedure_nm',
                           'in_or_dttm', 'out_or_dttm', 'an_start_datetime', 'an_stop_datetime']
            },
            # Add other models following the same pattern...
        ]

        with connection.cursor() as cursor:
            for model_info in model_queries:
                where_conditions = []
                query_params = []

                if mrn and model_info['has_mrn']:
                    where_conditions.append("UPPER(mrn) = UPPER(%s)")
                    query_params.append(mrn)

                if log_id and model_info['has_log_id']:
                    where_conditions.append("UPPER(log_id) = UPPER(%s)")
                    query_params.append(log_id)

                if not where_conditions:
                    continue

                fields_str = ', '.join(model_info['fields'])
                where_str = ' AND '.join(where_conditions)

                query = f"SELECT {fields_str} FROM {model_info['table']} WHERE {where_str}"

                cursor.execute(query, query_params)
                rows = dictfetchall(cursor)

                for row in rows:
                    # Add model_name and fill missing fields with None
                    result = {'model_name': model_info['model_name']}

                    # Define all possible fields
                    all_fields = [
                        'id', 'mrn', 'source_key', 'source_name', 'name', 'ref_bill_code_set_name',
                        'ref_bill_code', 'diagnosis_code', 'dx_name', 'log_id', 'disch_disp_c',
                        'hosp_admsn_time', 'hosp_disch_time', 'los', 'icu_admin_flag', 'surgery_date',
                        'birth_date', 'height', 'weight', 'sex', 'primary_anes_type_nm', 'asa_rating_c',
                        'asa_rating', 'patient_class_group', 'patient_class_nm', 'primary_procedure_nm',
                        'in_or_dttm', 'out_or_dttm', 'an_start_datetime', 'an_stop_datetime',
                        'enc_type_nm', 'lab_code', 'lab_name', 'observation_value', 'measurement_units',
                        'reference_range', 'abnormal_flag', 'collection_datetime', 'enc_type_c',
                        'ordering_date', 'order_class_nm', 'medication_id', 'display_name',
                        'medication_nm', 'start_date', 'end_date', 'order_status_nm', 'record_type',
                        'mar_action_nm', 'med_action_time', 'admin_sig', 'dose_unit_nm', 'med_route_nm',
                        'description', 'properties_display', 'site', 'placement_instant', 'removal_instant',
                        'flo_meas_name', 'line_group_name', 'element_name', 'context_name', 'element_abbr',
                        'smrtdta_elem_value', 'event_display_name', 'event_time', 'note_text'
                    ]

                    for field in all_fields:
                        result[field] = row.get(field, None)

                    all_data.append(result)

        # Apply pagination
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