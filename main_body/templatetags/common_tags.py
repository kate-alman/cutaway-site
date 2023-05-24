from django import template
from django.contrib.auth.models import User
from django.db.models import Q
from django.template import RequestContext

from accounts.models import Profile
from main_body.models import Menu, PageVisits

from services.models import News

register = template.Library()


@register.inclusion_tag("main_body/menu.html", takes_context=True)
def show_top_menu(context: RequestContext, selected: str) -> RequestContext:
    menu_items = list(Menu.objects.select_related("parent").all())
    have_child: dict = {}
    for item in menu_items.copy():
        parent = item.parent
        if parent:
            menu_items.remove(item)
            have_child[parent.name] = have_child.get(parent.name, []) + [item]
    selected = selected.strip("/") if len(selected) > 1 else "home"
    context["menu_items"] = menu_items
    context["have_child"] = have_child
    context["selected"] = selected
    return context


@register.simple_tag(name="get_child")
def get_child(child_list: dict, parent: str) -> list[Menu]:
    return child_list[parent]


@register.inclusion_tag("services/users_list.html", takes_context=True)
def get_users(context: RequestContext, user: User) -> RequestContext:
    context["users"] = Profile.objects.filter(~Q(user_id=user.pk)).select_related(
        "user"
    )
    return context


@register.inclusion_tag("services/posts.html", takes_context=True)
def show_posts(context: RequestContext, **kwargs) -> RequestContext:
    staff = kwargs.get("staff")
    if staff:
        context["posts"] = News.objects.filter(user__is_staff=staff)
    return context


@register.simple_tag
def show_counter(url: str) -> int:
    page = PageVisits.objects.get(url=url)
    return page.count
