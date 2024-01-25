import os
import django
from django.db.models import Count, Q, F

from main_app.models import Profile, Product, Order

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


def get_profiles(search_string=None):

    if search_string is None:
        return ''
    profile_objects = Profile.objects.annotate(num_orders=Count('profile_order')).filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)).order_by('full_name')
    result = []
    for profile_object in profile_objects:
        if profile_object is None:
            return ''
        result.append(f"Profile: {profile_object.full_name}, email: {profile_object.email}, "
                      f"phone number: {profile_object.phone_number}, orders: {profile_object.num_orders}")
    return '\n'.join(result) if result else ''


def get_loyal_profiles():

    loyal_profile = Profile.objects.annotate(
        num_orders=Count('profile_order')).filter(num_orders__gt=2).order_by('-num_orders')
    result = []
    [result.append(f"Profile: {profile.full_name}, orders: {profile.num_orders}") for profile in loyal_profile]
    return '\n'.join(result) if result else ''


def get_last_sold_products():
    try:
        last_order = Order.objects.prefetch_related('products').latest('creation_date')
        last_sold_products = last_order.products.all().order_by('name')
        if last_sold_products:
            last_sold_products_str = ", ".join(product.name for product in last_sold_products)
            return f"Last sold products: {last_sold_products_str}"
        return ""
    except Order.DoesNotExist:
        return ""

    # products = Order.objects.annotate(latest_order='product').order_by('product__name')
    # result = []
    # for product in products:
    #     if not product:
    #         return ''
    #     result.append(product)
    #
    # if not products:
    #     return ''
    # else:
    #     return f"Last sold products: {', '.join(result)}"


def get_top_products():
    top_products = Product.objects.annotate(
        num_orders=Count('orders')).filter(num_orders__gt=0).order_by('-num_orders', 'name')[:5]
    if not top_products:
        return ''
    top_products_str = [f"{product.name}, sold {product.num_orders} times" for product in top_products]

    return f"Top products:\n" + "\n".join(top_products_str)


def apply_discounts():
    discounted_orders = Order.objects.annotate(
        num_products=Count('products')
    ).filter(num_products__gt=2, is_completed=False).update(total_price=F('total_price') * 0.90)

    return f"Discount applied to {discounted_orders} orders."


def complete_order():
    order = Order.objects.prefetch_related('products').filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ''

    for product in order.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False

        product.save()

    order.is_completed = True
    order.save()

    return f"Order has been completed!"