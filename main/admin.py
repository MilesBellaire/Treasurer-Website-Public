from django.contrib import admin
from .models import ReimbursementRequest as rr

class ReceiptAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(rr, ReceiptAdmin)