# flake8: noqa
"""test for recipe apis"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL=reverse('recipe:recipe-list')


def create_recipe(user,**params):
    """create and return s sample recipe"""
    defaults={
        'title':'sample recipe title',
        'time_minutes':22,
        'price':Decimal('5.25'),
        'description':'sample decsription',
        'link':'http://example.com/recipe.pdf'
    }
    defaults.update(params)

    recipe=Recipe.objects.create(user=user,**defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """test unauthenticated API request"""

    def setUp(self):
        self.client=APIClient()

    def test_auth_required(self):
        """"""

        res=self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """test authenciated api request"""

    def setUp(self):
        self.client=APIClient()
        self.user=get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """test retrieveing a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)

        recipes=Recipe.objects.all().order_by('-id')
        serializer=RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_recicpe_list_limited_to_user(self):
        """test list of recipes is limited to authenticated user"""

        other_user=get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)

        recipe=Recipe.objects.filter(user=self.user)
        serializer=RecipeSerializer(recipe,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

