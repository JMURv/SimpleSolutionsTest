from django.contrib import admin
from django.urls import path
from .views import (
    BuyHandler,
    ItemHandler,
    SuccessView,
    CancelView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/<int:id>/', BuyHandler.as_view(), name='buy-handler'),
    path('item/<int:id>/', ItemHandler.as_view(), name='item-handler'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
]
