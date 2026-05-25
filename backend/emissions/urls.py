from django.urls import path
from .views import DashboardStatsView, ReviewQueueView, ApproveEmissionView, RejectEmissionView, ExportAuditReportView

urlpatterns = [
    path(
        "dashboard/stats/",
        DashboardStatsView.as_view(),
    ),
    path(
        "emissions/review-queue/",
        ReviewQueueView.as_view(),
    ),
    path(
        "emissions/<int:pk>/approve/",
        ApproveEmissionView.as_view(),
    ),
    path(
        "emissions/<int:pk>/reject/",
        RejectEmissionView.as_view(),
    ),
    path(
    "emissions/export/",
    ExportAuditReportView.as_view(),
   ),
]