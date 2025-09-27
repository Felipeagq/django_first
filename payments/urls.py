from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PaymentViewSet, wompi_webhook

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename="payment")

urlpatterns = [
    path("wompi/webhook/", wompi_webhook, name="wompi-webhook"),
]

urlpatterns += router.urls
