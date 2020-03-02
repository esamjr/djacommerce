from django import template
from django.contrib.auth.decorators import login_required
from core.models import Order

# register template tags
register = template.Library()


@register.filter
def cart_item_count(user):
    """
    display cart item counts

    :param user:
    """
    # filter order by user
    queryset = Order.objects.filter(username_order=user, ordered=False)
    if queryset.exists():
        return queryset[0].items.count()

    return 0
