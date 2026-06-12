from django.db import connection
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Lightweight health check used by Render and uptime pings."""

    permission_classes = [AllowAny]
    throttle_classes = []
    http_method_names = ["get", "head", "options"]

    def get(self, request):
        database_ok = True
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            database_ok = False

        return Response(
            {"status": "ok" if database_ok else "degraded", "database": database_ok},
            status=status.HTTP_200_OK if database_ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        )
