import re
from catalog.models import House, FloorPlan, HouseImage, Content
from api.filters import HouseFilter

from django.conf import settings
from django.urls import reverse
from rest_framework import serializers
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend

class FloorPlanSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField()
    floor_content = serializers.SerializerMethodField()

    class Meta:
        model = FloorPlan
        fields = ['name', 'schema', 'floor_content']

    def get_schema(self, obj):
        request = self.context.get('request')
        rendition = obj.schema.get_rendition("jpegquality-100")
        schema_url = rendition.url
        return request.build_absolute_uri(schema_url)    
    
    def get_floor_content(self, obj):
        cleaned_floor_content = re.sub(r'\sdata-block-key="[^"]*"', '', obj.floor_content)
        return cleaned_floor_content
    

class HouseImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HouseImage
        fields = ['image']   

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = request.build_absolute_uri(obj.image.file.url) # change this line
        return image_url
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_url = representation.pop('image')
        return image_url
    
    
    

class ContentHouseSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['content']

    def get_content(self, obj):
        cleaned_content = re.sub(r'\sdata-block-key="[^"]*"', '', obj.content)
        return cleaned_content   

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        content = representation.pop('content')
        return {str(instance.sort_order + 1): content} 

    
class HouseSerializer(serializers.ModelSerializer):
    floor_plan = FloorPlanSerializer(many=True)
    images = HouseImagesSerializer(many=True)
    content = ContentHouseSerializer(many=True)
    description = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = ['id', 'name', 'area', 'price', 'project', 'floor', 'building_type', 'rooms', 'bathrooms', 'style', 'description', 'floor_plan', 'images', 'content']

    def get_description(self, obj):
        cleaned_description = re.sub(r'\sdata-block-key="[^"]*"', '', obj.description)
        return cleaned_description

class CardObject(viewsets.ModelViewSet):
    serializer_class = HouseSerializer
    queryset = House.objects.all()


class CatalogSerializer(serializers.ModelSerializer):
    card_url = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = ['id', 'name', 'area', 'price', 'project', 'floor', 'card_url', 'building_type']

    def get_card_url(self, obj):
        request = self.context.get('request')
        card_url = reverse('card-detail', kwargs={'pk': obj.id})
        return request.build_absolute_uri(card_url)

class CatalogObject(viewsets.ModelViewSet):
    serializer_class = CatalogSerializer
    queryset = House.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = HouseFilter
