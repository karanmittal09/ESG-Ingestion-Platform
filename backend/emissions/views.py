import csv

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import EmissionRecord


class DashboardStatsView(APIView):

    def get(self, request):

        total_records = EmissionRecord.objects.count()

        suspicious_records = EmissionRecord.objects.filter(
            suspicious_flag=True
        ).count()

        approved_records = EmissionRecord.objects.filter(
            review_status="APPROVED"
        ).count()

        return Response({
            "total_records": total_records,
            "suspicious_records": suspicious_records,
            "approved_records": approved_records,
        })


class ReviewQueueView(APIView):

    def get(self, request):

        records = EmissionRecord.objects.all()

        data = []

        for record in records:

            data.append({
                "id": record.id,
                "source": record.activity_type,
                "quantity": f"{record.quantity} {record.normalized_unit}",
                "co2e": f"{record.co2e} kgCO2e",
                "suspicious": record.suspicious_flag,
                "status": record.review_status,
            })

        return Response(data)


class ApproveEmissionView(APIView):

    def patch(self, request, pk):

        record = EmissionRecord.objects.get(id=pk)

        record.review_status = "APPROVED"

        record.save()

        return Response({
            "message": "Record approved"
        })


class RejectEmissionView(APIView):

    def patch(self, request, pk):

        record = EmissionRecord.objects.get(id=pk)

        record.review_status = "REJECTED"

        record.save()

        return Response({
            "message": "Record rejected"
        })


class ExportAuditReportView(APIView):

    def get(self, request):

        response = HttpResponse(
            content_type="text/csv"
        )

        response[
            "Content-Disposition"
        ] = 'attachment; filename="audit_report.csv"'

        writer = csv.writer(response)

        writer.writerow([
            "ID",
            "Source",
            "Quantity",
            "Unit",
            "CO2e",
            "Status",
            "Suspicious",
        ])

        records = EmissionRecord.objects.all()

        for record in records:

            writer.writerow([
                record.id,
                record.activity_type,
                record.quantity,
                record.normalized_unit,
                record.co2e,
                record.review_status,
                record.suspicious_flag,
            ])

        return response