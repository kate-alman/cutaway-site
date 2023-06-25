from django.shortcuts import redirect

from accounts.models import Profile


class PostMixin:
    """Defines pagination of posts. If an author's blog is selected,
    then checks if such a user exists and shows his blog."""
    paginate_by = 4

    def post(self, request, *args, **kwargs):
        try:
            user_id_, nickname = (request.POST.getlist("nickname")[0]).split()
            return redirect("selected_blog", nickname=nickname, pk=user_id_)
        except ValueError:
            return redirect("blog")


class UserMixin:
    def get_user_context(self, self_profile=False, **kwargs):
        """Adds data about the user from his profile to the context."""
        context = kwargs
        user_id = self.kwargs.get("pk", kwargs.get("pk"))
        if user_id and user_id != self.request.user.pk or self_profile:
            user_profile = Profile.objects.select_related("user").get(user__id=user_id)
            user_info = {
                "f_user": user_profile,
                "nickname": user_profile.nickname,
                "bio": user_profile.bio,
                "location": user_profile.location,
                "birth_date": user_profile.birth_date,
                "photo": user_profile.photo,
            }
            context["user_info"] = user_info
        return context
