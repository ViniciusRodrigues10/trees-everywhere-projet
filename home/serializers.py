from rest_framework import serializers
from .models import PlantedTree


class PlantedTreeSerializer(serializers.ModelSerializer):
    """
    Serializer for the PlantedTree model.
    """

    class Meta:
        model = PlantedTree
        fields = ["id", "tree", "age", "latitude", "longitude", "planted_at", "account"]
