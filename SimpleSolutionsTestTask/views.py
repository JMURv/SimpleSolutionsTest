from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.conf import settings
from .models import Item, Order
import stripe


class BuyHandler(TemplateView):
    def get(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        order_id = request.COOKIES.get('order_id')
        if not order_id:
            return JsonResponse({'error': 'No items in order'})

        order = get_object_or_404(Order, pk=order_id)
        tax = order.tax
        discount = order.discount

        tax_rate = stripe.TaxRate.create(
            display_name='Tax',
            percentage=tax.amount if tax else 0,
            inclusive=False
        )
        discount_amount = discount.amount if discount else 0

        line_items = [{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int((item.price - discount_amount) * 100),
            },
            'quantity': 1,
            'tax_rates': [tax_rate['id']] if tax_rate else []
        } for item in order.items.all()]
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=settings.SITE_BASE_URL + reverse_lazy("success"),
            cancel_url=settings.SITE_BASE_URL + reverse_lazy("cancel"),
        )

        return JsonResponse({'id': session.id})


class ItemHandler(TemplateView):
    template_name = "item.html"

    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'item': get_object_or_404(Item, pk=kwargs.get("id")),
                "public_key": settings.STRIPE_PUBLISHABLE_KEY
            }
        )

    def post(self, request, *args, **kwargs):
        item_id = kwargs.get("id")
        item = get_object_or_404(Item, pk=item_id)
        order_id = request.COOKIES.get('order_id')
        if order_id:
            order = get_object_or_404(Order, pk=order_id)
        else:
            order = Order.objects.create()
        order.items.add(item)
        response = redirect('item-handler', id=item_id)
        response.set_cookie('order_id', order.id)
        return response


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
