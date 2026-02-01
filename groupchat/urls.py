from django.urls import path, include
from rest_framework.routers import DefaultRouter  
from.views import GroupViewSet,GroupMessagesViewSet

router = DefaultRouter()
router.register(r'groups',GroupViewSet,basename='group')
router.register(r'groupmessages',GroupMessagesViewSet,basename='groupmessages')

urlpatterns = [
    path('', include(router.urls)),
]

