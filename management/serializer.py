from .models import (PatientCoding, PatientHistory, PatientInformation, PatientLabs, PatientLDA,
                     PatientPostOPComplications, PatientProcedureEvents, PatientVisit, PatientMedication)
from rest_framework import serializers

class PatientCodingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientCoding
        fields = "__all__"


class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistory
        fields = "__all__"


class PatientInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInformation
        fields = "__all__"


class PatientLabsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientLabs
        fields = "__all__"


class PatientLDASerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientLDA
        fields = "__all__"


class PatientPostOPComplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientPostOPComplications
        fields = "__all__"


class PatientProcedureEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProcedureEvents
        fields = "__all__"


class PatientVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientVisit
        fields = "__all__"


class PatientMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedication
        fields = "__all__"