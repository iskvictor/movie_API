from rest_framework import serializers
from .models import Movie, Review, Rating


class MovieListSerializer(serializers.ModelSerializer):
    """  Список фильмов """
    class Meta:
        model = Movie
        fields = ("title", "tagline", "category")

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"

class FilterReviewListSerializer(serializers.ListSerializer):
    """ Вывод рекурсивно children """
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """ Фильтр коментариев, только parent """
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")

class MovieDetailSerializer(serializers.ModelSerializer):
    """  Список фильмов """
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True,  many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True,  many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True,  many=True)
    reviews = ReviewSerializer(many=True)
    
    class Meta:
        model = Movie
        exclude = ("draft",)


class CreateRatingSerialiser(serializers.ModelSerializer):
    """ Добавление рейтинга пользователя """
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get("ip", None),
            movie=validated_data.get("movie", None),
            defaults={"star": validated_data.get("star")}
        )
        return rating

