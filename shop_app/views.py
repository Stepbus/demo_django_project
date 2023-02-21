from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Backpack, Products, ShoppingList, Notebook, Dishwasher, VacuumCleaner, TV
from auth_user.tasks import send_email_thread


def home(request):
    all_users = get_user_model().objects.all()
    for auth_user in all_users:
        cache.add(str(auth_user), "Offline", None)
    users_from_cache = cache.get_many(all_users)

    return render(request, "auth_user/main_page.html", {"output": users_from_cache})


class ShowBasket(ListView):
    template_name = "shop_app/list_products_in_backpack.html"
    context_object_name = "products"
    model = Backpack

    def get(self, request, *args, **kwargs):
        if not self.get_queryset().filter(bayer_id=request.user.userprofile.id).exists():
            return HttpResponseRedirect(reverse('shop'))
        self.object_list = self.get_queryset().filter(bayer_id=request.user.userprofile.id)
        count = 777
        context = self.get_context_data(count=count)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        for value in request.POST.items():
            if value[0] == 'csrfmiddlewaretoken':
                continue
            id_product = int(value[0])
            count_product = int(value[1])
            bayer = Backpack.objects.filter(bayer_id=request.user.userprofile.id, product_id=id_product)
            product = Products.objects.filter(id=id_product)
            """применил F"""
            if bayer.count != count_product:
                product.update(count=F('count') + count_product)
                bayer.update(count=F('count') - count_product)
                # product.save(update_fields=["count"])
                # bayer.save(update_fields=["count"])
            else:
                continue

        return HttpResponseRedirect(reverse('basket', args=(request.user.userprofile.id,)))


class ShowShoppingList(ListView):
    template_name = "shop_app/ShoppingUserList.html"
    context_object_name = "products"
    model = ShoppingList

    def get(self, request, *args, **kwargs):
        if not self.get_queryset().filter(bayer_archive=request.user.userprofile.id).exists():
            val = send_email_thread.delay()
            print(f"START ....")
            print(val.get())
            return HttpResponseRedirect(reverse('shop'))

        self.object_list = self.get_queryset().filter(bayer_archive=request.user.userprofile.id)
        context = self.get_context_data()
        return self.render_to_response(context)


class CreateShoppingList(View):

    def get(self, request):
        products = Backpack.objects.filter(bayer_id=request.user.userprofile.id)
        for item in products:
            ShoppingList.objects.create(
                bayer_archive=request.user.userprofile,
                id_product_archive=item.product_id,
                model=item.product.model,
                price=item.product.price,
                warranty=item.product.warranty,
                brand_name=item.product.brand_name,
                category=item.product.category,
                count=item.count,
            )
            item.delete()
        return HttpResponseRedirect(reverse('shop'))


class DeleteFromBackpack(View):

    def get(self, request, product_id):
        product_in_backpack = Backpack.objects.get(bayer_id=request.user.userprofile.id, product_id=product_id)
        product_in_backpack.delete()
        """применил F"""
        products_on_stock = Products.objects.filter(id=product_id)
        products_on_stock.update(count=F('count') + product_in_backpack.count)
        # products_on_stock = Products.objects.get(id=product_id)
        # products_on_stock.count += product_in_backpack.count
        # products_on_stock.save()
        return HttpResponseRedirect(reverse('basket', args=(request.user.userprofile.id,)))


class DetailViewProduct(DetailView):
    template_name = 'shop_app/detail_product.html'
    model = Products

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        message = ''

        if int(request.POST.get("count")) != 0:
            count = int(request.POST.get("count"))
            "должна быть проверка int !"
            if count > self.object.count:
                message = "Please, enter correct value"
                context = self.get_context_data(object=self.object, message=message)
                return self.render_to_response(context)
            """изменил save"""
            self.object.count -= count
            self.object.save(update_fields=["count"])
            self.creating_object_backpack(request, count)

            context = self.get_context_data(object=self.object, message=message)
            return self.render_to_response(context)

        context = self.get_context_data(object=self.object, message=message)
        return self.render_to_response(context)

    def creating_object_backpack(self, request, count):
        obj, created = Backpack.objects.get_or_create(
            bayer=request.user.userprofile,
            product=self.object
        )
        """изменил save"""
        if created:
            obj.count = count
            obj.save(update_fields=["count"])
        else:
            obj.count += count
            obj.save(update_fields=["count"])


class NotebookList(ListView):
    template_name = "shop_app/list_all_products.html"
    context_object_name = "products"
    model = Notebook


class DishwasherList(ListView):
    template_name = "shop_app/list_all_products.html"
    context_object_name = "products"
    model = Dishwasher


class VacuumCleanerList(ListView):
    template_name = "shop_app/list_all_products.html"
    context_object_name = "products"
    model = VacuumCleaner


class TVList(ListView):
    template_name = "shop_app/list_all_products.html"
    context_object_name = "products"
    model = TV
