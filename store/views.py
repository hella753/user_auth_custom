from django.db.models import Count
from django.views.generic import DetailView, ListView, TemplateView
from mixins.search_mixin import SearchMixin
from store.models import Product, ProductReviews
from store.models import Category, ShopReviews, ProductTags


class IndexView(SearchMixin, ListView):
    model = ShopReviews
    template_name = "homepage/index.html"
    queryset = ShopReviews.objects.select_related("user")
    context_object_name = "reviews"


class CategoryListingsView(ListView):
    """
    filters:
    'q' -> search
    't' -> tags
    'p' -> price
    'fruitlist' -> sorting
    """
    model = Product
    template_name = "shop/shop.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('q'):
            queryset = queryset.filter(
                product_name__icontains=self.request.GET.get('q')
            ).prefetch_related("tags")

        if self.request.GET.get('t') or self.request.GET.get('p'):
            tags = None
            if self.request.GET.get('t'):
                tags = str(self.request.GET.get('t'))

            queryset = queryset.filter(
                product_price__lte=float(self.request.GET.get('p'))
            ).prefetch_related("tags")

            if tags:
                queryset = queryset.filter(tags=tags).prefetch_related("tags")

        if self.request.GET.get('fruitlist'):
            if self.request.GET.get('fruitlist') == "2":
                queryset = queryset.order_by("product_price")

        category_slug = self.kwargs.get("slug")
        if category_slug:
            category = Category.objects.filter(slug=category_slug)
            categories = category.get_descendants(include_self=True)
            queryset = (
                queryset
                .filter(product_category__in=categories)
                .prefetch_related("tags")
            )
        return queryset.prefetch_related("product_category", "tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent__isnull=True)
        product_tags = ProductTags.objects.all()

        category_slug = self.kwargs.get("slug")
        if category_slug:
            category = Category.objects.filter(slug=category_slug)
            categories = (
                category
                .get_descendants(include_self=False)
                .annotate(count=Count("product") + Count('children__product'))
            )
        else:
            categories = (
                categories
                .get_descendants(include_self=True)
                .annotate(count=Count('product') + Count('children__product'))
                .filter(parent__isnull=True)
            )
        context["categories"] = categories
        context["product_tags"] = product_tags
        return context


class ContactView(SearchMixin, TemplateView):
    template_name = "contact/contact.html"


class ProductView(SearchMixin, DetailView):
    model = Product
    template_name = "product_detail/shop-detail.html"
    pk_url_kwarg = "id"
    queryset = Product.objects.prefetch_related("product_category", "tags")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_reviews = ProductReviews.objects.filter(
            product=self.object
        ).select_related("user")
        quantity = 1

        context["reviews"] = product_reviews
        context["quantity"] = quantity
        return context
