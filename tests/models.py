import uuid

from django.db import models

from easy_tenants.models import TenantAwareAbstract, TenantManager


class ContactQuery(models.QuerySet):
    def by_phone(self):
        return self.filter(name__startswith="phone")


class StoreTenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class TenantModel(TenantAwareAbstract):
    store = models.ForeignKey(
        to=StoreTenant, on_delete=models.CASCADE, editable=False
    )

    objects = TenantManager()

    class Meta:
        abstract = True


class Product(TenantModel):
    name = models.CharField(max_length=10)
    category = models.ForeignKey(
        "tests.Category", null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Category(TenantModel):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Contact(TenantModel):
    name = models.CharField(max_length=10)

    objects = TenantManager.from_queryset(ContactQuery)()
