from django.db.models import QuerySet

from db.models import Ticket, Order, User, MovieSession
import datetime
from django.db import transaction


@transaction.atomic
def create_order(tickets: dict,
                 username: str,
                 date: datetime = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        ms_id = MovieSession.objects.get(pk=ticket["movie_session"],)
        Ticket.objects.create(movie_session=ms_id,
                              order=order,
                              row=ticket["row"],
                              seat=ticket["seat"],)
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
