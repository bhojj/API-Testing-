from django.shortcuts import render
from .models import Order
from.serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER
import logging


# Create your views here.
class OrderView(APIView):
    def get(self,request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many = True)
            return Response({
                # 'data': serializer.orders,
                'data': serializer.data,
                'message': "Orders Data Fetched Successfully"
            }, status=status.HTTP_200_OK)
        
        except:
            return Response({
                'data':{},
                'message':"Something Went Wrong while fetching the data"
            }, status= status.HTTP_400_BAD_REQUEST)
        
    def post(self,request):
        try:
            data = request.data
            serializer = OrderSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':"Something went wrong"
            }, status= status.HTTP_400_BAD_REQUEST)

            subject ="New Order is Placed"
            message = "Dear Customer" + " " + data['customer_name'] + "Your order is placed now. Thankls for your order"
            email = data['customer_email']
            recipient_list =[email]
            send_mail(subject,message,EMAIL_HOST_USER,recipient_list,fail_silently=True)


            serializer.save()
            return Response({
                'data': serializer.data,
                'message':"New order is created or placed"
            }, status= status.HTTP_201_CREATED)
        except:
            return Response({
                'data': {},
                'message': "Something went wrong in creation of Order"
            }, status= status.HTTP_400_BAD_REQUEST)
       
            
    def patch(self,request):
        try:
            data = request.data 
            Order1 = Order.objects.filter(id=data.get('id'))
            if not Order1.exists():
                return Response({
                    'data': {},
                    'message': "Order is not found with this ID"
            }, status= status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(Order1[0], data = data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong"

                }, status=status.HTTP_500_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': "Order is updated successfully"

            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'data': {},
                'message': "Something went wrong in creation of order"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        try:
            data = request.data 
            Order = Order.objects.filter(id =data.get('id'))
            if not Order.exists():
                return Response({
                    'data': {},
                    'message': "Order is not Found with this ID"
            }, status= status.HTTP_404_NOT_FOUND)
            Order[0].delete()
            return Response({
                'data':{},
                'message': "Order is Deleted"

            }, status= status.HTTP_200_OK)
        except:
            return Response({
                'data':{},
                'message': "Something went wrong  in deleting the order"

        }, status= status.HTTP_400_BAD_REQUEST)

            


            
            
            
            

            
            
            


