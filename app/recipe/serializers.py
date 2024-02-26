# flake8: noqa
"""for apis"""

from rest_framework import serializers

from core.models  import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """for recipes"""
    class Meta:
        model=Recipe
        fields=['id','title','time_minutes','price','link']
        read_only_fields=['id']
        