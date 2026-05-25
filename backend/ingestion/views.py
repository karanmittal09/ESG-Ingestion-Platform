import csv

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import FileUploadSerializer
from .models import DataSource, RawRecord

from organizations.models import Organization
from emissions.models import EmissionRecord

from rest_framework.parsers import MultiPartParser, FormParser

class SAPUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = FileUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        file = serializer.validated_data['file']
        organization_id = serializer.validated_data['organization_id']
        uploaded_by = serializer.validated_data['uploaded_by']

        organization = Organization.objects.get(id=organization_id)

        datasource = DataSource.objects.create(
            organization=organization,
            source_type='SAP',
            ingestion_method='CSV',
            uploaded_by=uploaded_by,
            file_name=file.name
        )

        decoded_file = file.read().decode('utf-8').splitlines()

        reader = csv.DictReader(decoded_file)

        processed_count = 0

        for index, row in enumerate(reader, start=1):

            raw_record = RawRecord.objects.create(
                datasource=datasource,
                raw_payload=row,
                row_number=index,
                status='PROCESSED'
            )

            quantity = float(row['quantity'])
            unit = row['unit']

            if unit == 'KL':
                quantity *= 1000
                normalized_unit = 'L'
            else:
                normalized_unit = unit

            emission_factor = 2.68

            co2e = quantity * emission_factor

            suspicious = quantity < 0

            EmissionRecord.objects.create(
                organization=organization,
                raw_record=raw_record,
                scope='SCOPE1',
                activity_type='fuel',
                quantity=quantity,
                normalized_unit=normalized_unit,
                emission_factor=emission_factor,
                co2e=co2e,
                suspicious_flag=suspicious
            )

            processed_count += 1

        return Response(
            {
                "message": "SAP file processed successfully",
                "rows_processed": processed_count
            },
            status=status.HTTP_201_CREATED
        )