from django.urls import path
from .views import GenerateFlutterCodeView, UserDesignHistoryView

urlpatterns = [
    path('imgtocode/', GenerateFlutterCodeView.as_view(), name='imgtocode'),
    path('history/', UserDesignHistoryView.as_view(), name='user-design-history'),
]
