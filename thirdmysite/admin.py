from django.contrib import admin

from thirdmysite.models import *


class ProductAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True



admin.site.register(Product, ProductAdmin)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(Reviews)
admin.site.register(Category)
admin.site.register(ContactWithUs, ProductAdmin)