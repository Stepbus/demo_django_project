from django.contrib import admin

from .models import TV, Notebook, Dishwasher, Brand, VacuumCleaner, Backpack, ShoppingList, Products

for model in [TV, Notebook, Dishwasher, Brand, VacuumCleaner]:
    admin.site.register(model)


class CustomShoppingList(admin.ModelAdmin):
    list_display = (
        'bayer_archive', 'purchase_date', 'category', 'count'
    )
    list_filter = ('bayer_archive', 'category')

#     def show_products(self, obj):
#         return [i for i in obj.product.all()]


class CustomBackpack(admin.ModelAdmin):
    list_display = (
        'bayer', 'product', 'count'
    )

#     def product_list(self, obj):
#         return [i for i in obj.product.all()]


admin.site.register(Products)
admin.site.register(Backpack,
                    CustomBackpack
                    )
admin.site.register(ShoppingList,
                    CustomShoppingList
                    )

