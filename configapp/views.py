from rest_framework.views import APIView
from .models import Employee, Client
from .employee_serializer import *
from .client_serializer import ClientStatisticsSerializer
from rest_framework.views import Response
from rest_framework import generics

class EmployeeStatisticsView(APIView):
    def get(self, request, pk):
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        month = int(month) if month else None
        year = int(year) if year else None

        try:
            emp = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found"}, status=404)

        serializer = EmployeeStatisticsSerializer(
            emp, context={"month": month, "year": year}
        )
        return Response(serializer.data)
    

class AllEmployeesStatisticsView(APIView):
    def get(self, request):
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        month = int(month) if month else None
        year = int(year) if year else None

        employees = Employee.objects.all()
        serializer = EmployeeStatisticsSerializer(
            employees, many=True, context={"month": month, "year": year}
        )
        return Response(serializer.data)


class ClientStatisticsView(APIView):
    def get(self, request, pk):
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        month = int(month) if month else None
        year = int(year) if year else None

        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({"detail": "Client not found"}, status=404)

        serializer = ClientStatisticsSerializer(
            client, context={"month": month, "year": year}
        )
        return Response(serializer.data)
    

class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer



