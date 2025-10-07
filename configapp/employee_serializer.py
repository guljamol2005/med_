from rest_framework import serializers
from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Employee, Client, Product, Order, OrderItem


class EmployeeStatisticsSerializer(serializers.ModelSerializer):
    clients_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    sales_amount = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "full_name", "clients_count", "products_count", "sales_amount"]

    def get_clients_count(self, obj):
        month = self.context.get("month")
        year = self.context.get("year")
        orders = Order.objects.filter(employee=obj)

        if month and year:
            orders = orders.filter(order_date__year=year, order_date__month=month)
        elif year:
            orders = orders.filter(order_date__year=year)
        elif month:
            orders = orders.filter(order_date__month=month)
        return orders.values("client").distinct().count()

    def get_products_count(self, obj):
        month = self.context.get("month")
        year = self.context.get("year")
        orders = Order.objects.filter(employee=obj)

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
        orders = Order.objects.filter(employee=obj)
        
        if month and year:
            orders = orders.filter(order_date__year=year, order_date__month=month)
        elif year:
            orders = orders.filter(order_date__year=year)
        elif month:
            orders = orders.filter(order_date__month=month)
        return (
            orders.aggregate(total=Coalesce(Sum("total_price"), 0)).get("total", 0)
        )
    




class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "full_name"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "employee", "client", "order_date", "total_price"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity"]


