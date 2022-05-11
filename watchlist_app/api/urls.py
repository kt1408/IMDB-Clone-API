from django.urls import path,include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchDetailAV, WatchListAV, 
                                     ReviewList,ReviewDetail,ReviewCreate,
                                     StreamPlatformVS,UserReview)
                                     

router = DefaultRouter()
router.register('stream',StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='Watch-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name = 'movie-details'),
#    path('list2/', WatchListGV.as_view(), name = 'movie-details'),
    
    path('',include(router.urls)),
     
    path('<int:pk>/review/', ReviewList.as_view(), name ='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name = 'review-detail'),
    path('<int:pk>/review/create/', ReviewCreate.as_view(), name ='review-create'),
    
    path('user-review/', UserReview.as_view(), name = 'user-review-detail'),
]


 