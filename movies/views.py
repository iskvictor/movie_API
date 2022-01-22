from django.db import models
from rest_framework import generics, permissions
from .models import Movie, Actor
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    MovieListSerializer, 
    MovieDetailSerializer, 
    ReviewCreateSerializer, 
    CreateRatingSerialiser, 
    ActorListSerializer, 
    ActorDetailSerializer)
from .service import get_client_ip, MovieFilter

class MovieListView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = MovieFilter
    permission_classes =[permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
            ).annotate(
                middle_star = models.Sum(models.F('ratings__star'))/models.Count(models.F('ratings'))
            )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.filter(draft=False)
        

class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильма """
    serializer_class =CreateRatingSerialiser
    
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
        
        


class ActorListView(generics.ListAPIView):
        """ Вывод список актеров"""
        queryset = Actor.objects.all()
        serializer_class = ActorListSerializer
        

class ActorDetailView(generics.RetrieveAPIView):
        """ Вывод полного описания актеров и режиссеров"""
        queryset = Actor.objects.all()
        serializer_class = ActorDetailSerializer






