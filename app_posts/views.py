from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_posts.models import PostsModel
from app_posts.serializers import PostSerialize


@api_view(["GET", "POST"])
def posts_view(request):
    if request.method == "GET":
        posts = PostsModel.objects.all()
        serializer = PostSerialize(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = PostSerialize(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE", "PATCH"])
def posts_detail_view(request, slug):
    response = {"success": True}
    try:
        post = PostsModel.objects.get(slug=slug)
    except PostsModel.DoesNotExist:
        response["success"] = False
        response["detail"] = "Post does not exists"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerialize(post)
        response["data"] = serializer.data
        return Response(data=response, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = PostSerialize(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response["data"] = serializer.data
            return Response(data=response, status=status.HTTP_202_ACCEPTED)

    elif request.method == "PATCH":
        serializer = PostSerialize(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response["data"] = serializer.data
            return Response(data=response, status=status.HTTP_202_ACCEPTED)

    elif request.method == "DELETE":
        post.delete()
        response["detail"] = "Post is deleted"
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)

