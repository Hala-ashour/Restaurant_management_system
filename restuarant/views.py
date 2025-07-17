# views.py
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import  Product
from .serializers import  ProductSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'price']
    
    @action(detail=True, methods=['GET'], url_path='check-availability')
    def check_availability(self, request, pk=None):
        
        product = self.get_object()
        return Response({
            'product_id': product.id,
            'product_name': product.name,
            'is_available': product.is_available,
            'message': 'Available for order' if product.is_available else 'Currently unavailable'
        }, status=status.HTTP_200_OK)

