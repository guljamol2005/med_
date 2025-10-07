from rest_framework import serializers
from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Client, Order, OrderItem



class ClientStatisticsSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    sales_amount = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["id", "full_name", "products_count", "sales_amount"]

    def get_products_count(self, obj):
        month = self.context.get("month")
        year = self.context.get("year")
        orders = Order.objects.filter(client=obj)
        if month and year:
            orders = orders.filter(order_date__year=year, order_date__month=month)
        elif year:
            orders = orders.filter(order_date__year=year)
        elif month:
            orders = orders.filter(order_date__month=month)
        return (
            OrderItem.objects.filter(order__in=orders)
            .aggregate(total=Coalesce(Sum("quantity"), 0))
            .get("total", 0)
        )

    def get_sales_amount(self, obj):
        month = self.context.get("month")
        year = self.context.get("year")
        orders = Order.objects.filter(client=obj)
        if month and year:
            orders = orders.filter(order_date__year=year, order_date__month=month)
        elif year:
            orders = orders.filter(order_date__year=year)
        elif month:
            orders = orders.filter(order_date__month=month)
        return (
            orders.aggregate(total=Coalesce(Sum("total_price"), 0)).get("total", 0)
        )
