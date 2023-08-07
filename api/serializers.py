from rest_framework import serializers
from wagtail.api.v2.serializers import PageSerializer
from catalog.models import Room, FloorPlan, House

class RoomSerializer(PageSerializer):
    class Meta:
        model = Room
        fields = ['name', 'area']

class FloorPlanSerializer(PageSerializer):
    rooms = RoomSerializer(many=True)

    class Meta:
        model = FloorPlan
        fields = ['name', 'schema', 'rooms']

class HouseSerializer(PageSerializer):
    floor_plan = FloorPlanSerializer(many=True)

    class Meta:
        model = House
        field_names = ['name', 'area', 'price', 'building_type', 'rooms', 'bathrooms', 'style', 'description', 'floor_plan']