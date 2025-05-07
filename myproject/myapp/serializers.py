from .models import product_model
from rest_framework import serializers

class productserializers(serializers.ModelSerializer):
    class Meta:
        model=product_model
        fields='__all__'