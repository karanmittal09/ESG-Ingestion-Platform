import csv
import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import FileUploadSerializer
from .models import DataSource, RawRecord

from organizations.models import Organization
from emissions.models import EmissionRecord


class SAPUploadView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = FileUploadSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        file = serializer.validated_data["file"]

        organization_id = serializer.validated_data[
            "organization_id"
        ]

        uploaded_by = serializer.validated_data[
            "uploaded_by"
        ]

        organization = Organization.objects.get(
            id=organization_id
        )

        datasource = DataSource.objects.create(
            organization=organization,
            source_type="SAP",
            ingestion_method="CSV",
            uploaded_by=uploaded_by,
            file_name=file.name
        )

        decoded_file = file.read().decode(
            "utf-8"
        ).splitlines()

        reader = csv.DictReader(decoded_file)

        processed_count = 0

        for index, row in enumerate(reader, start=1):

            raw_record = RawRecord.objects.create(
                datasource=datasource,
                raw_payload=row,
                row_number=index,
                status="PROCESSED"
            )

            quantity = float(row["quantity"])

            unit = row["unit"]

            if unit == "KL":

                quantity *= 1000

                normalized_unit = "L"

            else:

                normalized_unit = unit

            emission_factor = 2.68

            co2e = quantity * emission_factor

            suspicious = quantity < 0

            EmissionRecord.objects.create(
                organization=organization,
                raw_record=raw_record,
                scope="SCOPE1",
                activity_type="fuel",
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


class UtilityUploadView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        file = request.FILES.get("file")

        organization_id = request.data.get(
            "organization_id"
        )

        uploaded_by = request.data.get(
            "uploaded_by"
        )

        organization = Organization.objects.get(
            id=organization_id
        )

        datasource = DataSource.objects.create(
            organization=organization,
            source_type="UTILITY",
            ingestion_method="CSV",
            uploaded_by=uploaded_by,
            file_name=file.name
        )

        df = pd.read_csv(file)

        processed_count = 0

        for index, row in df.iterrows():

            raw_record = RawRecord.objects.create(
                datasource=datasource,
                raw_payload=row.to_dict(),
                row_number=index + 1,
                status="PROCESSED"
            )

            kwh = float(row["kwh"])

            co2e = kwh * 0.82

            suspicious = kwh > 14000

            EmissionRecord.objects.create(
                organization=organization,
                raw_record=raw_record,
                scope="SCOPE2",
                activity_type="electricity",
                quantity=kwh,
                normalized_unit="kWh",
                emission_factor=0.82,
                co2e=co2e,
                suspicious_flag=suspicious
            )

            processed_count += 1

        return Response(
            {
                "message": "Utility data uploaded successfully",
                "rows_processed": processed_count
            },
            status=status.HTTP_201_CREATED
        )

class TravelUploadView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        file = request.FILES.get("file")

        organization_id = request.data.get(
            "organization_id"
        )

        uploaded_by = request.data.get(
            "uploaded_by"
        )

        organization = Organization.objects.get(
            id=organization_id
        )

        datasource = DataSource.objects.create(
            organization=organization,
            source_type="TRAVEL",
            ingestion_method="CSV",
            uploaded_by=uploaded_by,
            file_name=file.name
        )

        df = pd.read_csv(file)

        processed_count = 0

        for index, row in df.iterrows():

            raw_record = RawRecord.objects.create(
                datasource=datasource,
                raw_payload=row.to_dict(),
                row_number=index + 1,
                status="PROCESSED"
            )

            distance = float(row["distance_km"])

            mode = row["mode"]

            if mode == "flight":

                emission_factor = 0.115

            elif mode == "cab":

                emission_factor = 0.18

            else:

                emission_factor = 0.05

            co2e = distance * emission_factor

            suspicious = distance > 2500

            EmissionRecord.objects.create(
                organization=organization,
                raw_record=raw_record,
                scope="SCOPE3",
                activity_type=mode,
                quantity=distance,
                normalized_unit="km",
                emission_factor=emission_factor,
                co2e=co2e,
                suspicious_flag=suspicious
            )

            processed_count += 1

        return Response(
            {
                "message": "Travel data uploaded successfully",
                "rows_processed": processed_count
            },
            status=status.HTTP_201_CREATED
        )