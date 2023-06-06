from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from drf_yasg.utils import swagger_auto_schema

from accounts.models import Profile
from project_api.permissions import IsOwnerOrReadOnly
from services.models import News, Tag
from project_api.serializers import NewsSerializer, UserSerializer, TagSerializer


class APIListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10000


@method_decorator(
    name="get", decorator=swagger_auto_schema(operation_description="Get list of tags")
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Add new tag, required params: name"
    ),
)
class TagAPIList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_description="Get list of posts. params: ?page=number"
    ),
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Add new post, required params: title, tag"
    ),
)
class NewsAPIList(generics.ListCreateAPIView):
    queryset = News.objects.select_related("user__profile").select_related("tag").all()
    serializer_class = NewsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = APIListPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def filter_queryset(self, queryset):
        amount = self.request.GET.get("amount")
        if amount:
            return News.objects.select_related("user__profile", "tag").all()[:int(amount)]
        return News.objects.select_related("user__profile", "tag").all()


@method_decorator(
    name="get", decorator=swagger_auto_schema(operation_description="Get post by id")
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Change the information of an existing post by id"
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Change the information of an existing post by id"
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(operation_description="Delete post by id"),
)
class PostAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.select_related("user__profile", "tag").all()
    serializer_class = NewsSerializer
    permission_classes = (IsOwnerOrReadOnly,)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(operation_description="Get user posts by id"),
)
class UserPostsAPIList(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = APIListPagination

    def get_queryset(self):
        return (
            News.objects.select_related("user__profile", "tag")
            .filter(user_id=self.kwargs.get("pk", 1))
        )


@method_decorator(
    name="get", decorator=swagger_auto_schema(operation_description="Get list of users")
)
class UsersAPIList(generics.ListAPIView):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


@method_decorator(
    name="get", decorator=swagger_auto_schema(operation_description="Get user by id")
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Change user information by id (only you)"
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Change user information by id (only you)"
    ),
)
class ProfileAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
