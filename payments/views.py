import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Payments
from .serializers import PaymentSerializer
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BaseAuthentication

class NoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return None



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save(student=request.user)

        # Llamada a la API de WOMPI (sandbox)
        url = "https://sandbox.wompi.co/v1/transactions"
        headers = {"Authorization": f"Bearer {settings.WOMPI_PRIVATE_KEY}"}
        payload = {
            "amount_in_cents": int(payment.amount * 100),
            "currency": "COP",
            "customer_email": request.user.email,
            "reference": f"course_{payment.course.id}_student_{request.user.id}",
            "payment_method": {
                "type": "CARD",
                "token": request.data.get("token"),  # token generado desde frontend
                "installments": 1,
            },
        }

        wompi_response = requests.post(url, json=payload, headers=headers).json()
        print(wompi_response.get("data", {}))
        transaction_id = wompi_response.get("data", {}).get("id")
        print(transaction_id)

        payment.wompi_transaction_id = transaction_id
        payment.status = "PENDING"
        payment.save()
        print(PaymentSerializer(payment).data)
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@authentication_classes([])  # 👈 vacío = sin autenticación
@permission_classes([])      # 👈 acceso público
def wompi_webhook(request):
    event = request.data.get("event")
    data = request.data.get("data", {})

    if event == "transaction.updated":
        transaction_id = data.get("transaction", {}).get("id")
        status_wompi = data.get("transaction", {}).get("status")

        try:
            payment = Payments.objects.get(wompi_transaction_id=transaction_id)
            if status_wompi == "APPROVED":
                payment.status = "APPROVED"
                # Suscribir al estudiante al curso
                # payment.course.students.add(payment.student)
            elif status_wompi == "DECLINED":
                payment.status = "DECLINED"
            payment.save()
        except Payments.DoesNotExist:
            pass

    return Response({"status": "ok"})