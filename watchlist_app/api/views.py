from xml.dom import ValidationErr

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
# from rest_framework.throttling import (AnonRateThrottle, ScopedRateThrottle,
#                                        UserRateThrottle)
from rest_framework.views import APIView

# from watchlist_app.api.pagination import (WatchListCPagination,
#                                           WatchListLOPagination,
#                                           WatchListPagination)
from watchlist_app.api.permissions import (IsAdminOrReadOnly,
                                           IsReviewUserOrReadOnly)
from watchlist_app.api.serializers import (ReviewSerializer,
                                           StreamPlatformSerializer,
                                           WatchListSerializer)
from watchlist_app.api.throttling import (ReviewCreateThrottle,
                                          ReviewListThrottle)
from watchlist_app.models import Review, StreamPlatform, WatchList


class UserReview(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You already have reviewed this item!")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
            
        else:
            movie.avg_rating =  (movie.avg_rating + serializer.validated_data['rating'] ) / 2
        
        movie.number_rating = movie.number_rating + 1
        movie.save()
                    
        serializer.save(watchlist=movie, review_user=review_user)
    
    
class ReviewList(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)
    
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    #throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail' 
    

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class =ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#CLASS BASED VIEWS

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True,context={'request': request})
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(user,context={'request': request})
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         else:
#             return Response(serializer.errors)

        
    

class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer  = StreamPlatformSerializer(platform, many=True, context={'request': request} )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request,pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error':'Searched Platform not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform,context={'request': request})
        return Response(serializer.data)
    
    def put(self, request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class WatchListGV(generics.ListAPIView):
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListSerializer
#     pagination_class= WatchListCPagination
#     #permission_classes = [IsAuthenticated]
#     #throttle_classes = [ReviewListThrottle,AnonRateThrottle]
#     # filter_backends = [filters.OrderingFilter]
#     # ordering_fields = ['avg_rating']
    
     
class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        movie = WatchList.objects.all()
        serializer  = WatchListSerializer(movie, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error':'Searched Item not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
                
                




#Function Based Views

# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer  = MovieSerializer(movies,many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
        # serializer = MovieSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        
        # else:
        #     return Response(serializer.errors)


# @api_view(['GET', 'PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method == 'GET':
        # try:
        #     movie = Movie.objects.get(pk=pk)
        # except Movie.DoesNotExist:
        #     return Response({'Error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        # serializer = MovieSerializer(movie)
        # return Response(serializer.data)
    
#     if request.method == 'PUT':
        # movie = Movie.objects.get(pk=pk)
        # serializer = MovieSerializer(movie, data = request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        
        # else:
        #     return Response(serializer.errors,status =status.HTTP_400_BAD_REQUEST)

        
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
        