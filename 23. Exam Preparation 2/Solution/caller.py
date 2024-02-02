import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create queries within functions
from main_app.models import Profile, Product, Order
from django.db.models import Q, F, Count


def get_profiles(search_string=None):
    result = []
    if search_string is not None:
        profiles = Profile.objects \
            .annotate(num_orders=Count('orders')) \
            .filter(Q(full_name__icontains=search_string)
                    | Q(email__icontains=search_string)
                    | Q(phone_number__icontains=search_string)) \
            .order_by('full_name')

        [result.append(f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, '
                       f'orders: {p.num_orders}') for p in profiles]

    return '\n'.join(result) if result else ''


def get_loyal_profiles():
    # loyal_profiles = Profile.objects.annotate(num_orders=Count('orders'))
    # .filter(num_orders__gt=2).order_by('-num_orders')
    loyal_profiles = Profile.objects.get_regular_customers()
    result = []
    [result.append(f"Profile: {p.full_name}, orders: {p.num_orders}") for p in loyal_profiles]

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


def get_top_products():
    top_products = Product.objects.annotate(num_orders=Count('orders')) \
                       .filter(num_orders__gt=0) \
                       .order_by('-num_orders', 'name')[:5]

    if top_products:
        top_products_str = "\n".join(f'{product.name}, sold {product.num_orders} times' for product in top_products)
        return f"Top products:\n{top_products_str}"
    return ""


def apply_discounts():
    discounted_orders = Order.objects.annotate(num_products=Count('products')) \
        .filter(num_products__gt=2, is_completed=False) \
        .update(total_price=F('total_price') * 0.9)

    return f'Discount applied to {discounted_orders} orders.'


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()
    if order is None:
        return ""

    order.is_completed = True
    order.save()

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False
        product.save()

    return "Order has been completed!"


# print(Profile.objects.get_regular_customers())

# print(get_profiles('9zz'))
# print(get_loyal_profiles())
# print(get_last_sold_products())
# print(get_top_products())
# print(apply_discounts())
# print(complete_order())
