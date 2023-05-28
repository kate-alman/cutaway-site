import os
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
import requests

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from accounts.models import Profile
from services.info import TITLE_REPLACE, GENRE_REPLACE, POSTER_REPLACE
from services.models import News, Tag
from services.forms import NewPostForm, UpdatePostForm
from services.utils import PostMixin, UserMixin


class ListServicesPageView(View):
    extra_context = {"title": "List of services"}

    def get(self, request):
        return render(request, "services/list.html")


class RandomFilm(View):
    API_KEY_KP = os.environ.get("API_KEY_KP")
    BASE_URL_KP = os.environ.get("BASE_URL_KP")
    extra_context = {"title": "Random film"}

    def get_random_film(self, year, rate, genre):
        try:
            URL = (
                f"{self.BASE_URL_KP}?genres={genre}&order=RATING&type=ALL&ratingFrom={rate}&"
                f"ratingTo=10&yearFrom={year}&yearTo=3000&page={random.randint(1, 5)}"
            )
            response = requests.get(
                URL,
                headers={
                    "X-API-KEY": self.API_KEY_KP,
                    "Content-Type": "application/json",
                },
            ).json()
            film = {
                "title": response["items"][0]["nameRu"],
                "genres": ", ".join(
                    [str(*i.values()) for i in response["items"][0]["genres"]]
                ),
                "ratingKinopoisk": response["items"][0]["ratingKinopoisk"],
                "ratingImdb": response["items"][0]["ratingImdb"],
                "year": response["items"][0]["year"],
                "posterUrl": response["items"][0]["posterUrlPreview"],
                "url": f'https://www.kinopoisk.ru/film/{response["items"][0]["kinopoiskId"]}/',
            }
        except (KeyError, IndexError):
            film = {
                "title": TITLE_REPLACE,
                "genres": GENRE_REPLACE,
                "ratingKinopoisk": 42,
                "ratingImdb": 42,
                "year": 42,
                "posterUrl": POSTER_REPLACE,
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            }
        return film

    def get(self, request, *args, **kwargs):
        film = self.get_random_film(
            random.randint(1920, 2023), random.randint(1, 10), random.randint(1, 10)
        )
        return render(request, "services/random_film.html", {"film": film})

    def post(self, request, *args, **kwargs):
        year = (
            request.POST.getlist("year")[0]
            if request.POST.getlist("year")[0]
            else random.randint(1920, 2023)
        )
        rate = (
            request.POST.getlist("rating")[0] if request.POST.getlist("rating") else 1
        )
        genre = (
            request.POST.getlist("genres")[0]
            if request.POST.getlist("genres")
            else random.randint(1, 10)
        )
        film = self.get_random_film(year, rate, genre)
        return render(request, "services/random_film.html", {"film": film})


class BlogView(PostMixin, ListView):
    model = News
    template_name = "services/blog.html"
    context_object_name = "posts"
    extra_context = {"title": "Blog"}

    def get_queryset(self):
        return News.objects.all().select_related("user__profile").select_related("tag")


class ShowPost(DetailView):
    model = News
    template_name = "services/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_queryset(self):
        return News.objects.all().select_related("user")


class TagsView(ListView):
    model = Tag
    context_object_name = "tags"

    def get_queryset(self):
        return Tag.objects.filter(~Q(name="admin-update"))


class NewPostView(LoginRequiredMixin, CreateView):
    form_class = NewPostForm
    template_name = "services/new_post.html"

    def get_tag(self, tag_info: str) -> str:
        if self.request.user.is_staff and not tag_info:
            tag, create = Tag.objects.get_or_create(name="admin-update")
            return tag
        if tag_info.isdigit():
            tag, create = Tag.objects.get_or_create(id=tag_info)
        else:
            if not tag_info:
                tag_info = "main"
            tag, create = Tag.objects.get_or_create(name=tag_info)
        return tag

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        tag_name = request.POST["tag"]
        post["tag"] = self.get_tag(tag_name)
        request.POST = post
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user_id = self.request.user.pk
            form.save()
            return redirect("blog")


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = "services/edit_post.html"
    form_class = UpdatePostForm
    context_object_name = "post"

    def get(self, request: HttpRequest, **kwargs):
        post = get_object_or_404(News, slug=self.kwargs.get("slug"))
        if self.request.user.pk == post.user_id:
            return super().get(request, **kwargs)
        else:
            raise Http404()

    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            slug = self.kwargs.get("slug")
            return redirect("post", post_slug=slug)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy("blog")


class UserOrTagBlogView(PostMixin, UserMixin, ListView):
    model = News
    template_name = "services/user_blog.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_info = self.get_user_context()
        return dict(list(context.items()) + list(user_info.items()))

    def get_queryset(self):
        tag_name = self.kwargs.get("name")
        user_id = self.kwargs.get("pk")
        if tag_name:
            return (
                News.objects.filter(tag__name=tag_name, is_published=True)
                .select_related("tag")
                .select_related("user")
                .select_related("user__profile")
            )
        return (
            News.objects.filter(user_id=user_id, is_published=True)
            .select_related("tag")
            .select_related("user")
            .select_related("user__profile")
        )


class FavoritePosts(PostMixin, ListView):
    model = News
    template_name = "services/favorite_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        ids = list(
            self.request.user.profile.favorites.all().values_list("user_id", flat=True)
        )
        return (
            News.objects.filter(user_id__in=ids)
            .select_related("tag")
            .select_related("user")
            .select_related("user__profile")
        )


class AddRemoveFavorite(View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user__id=kwargs["pk"])
        if not self.request.user.profile.add_relationship(profile):
            self.request.user.profile.remove_relationship(profile)
        return redirect("selected_blog", **kwargs)
