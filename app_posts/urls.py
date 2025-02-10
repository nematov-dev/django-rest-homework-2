from django.urls import path


from app_posts import views

app_name = 'posts'

urlpatterns = [
    path('',views.posts_view,name='list'),
    path('<slug:slug>/',views.posts_detail_view,name='detail'),

]