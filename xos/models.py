from core.models.plcorebase import *
from models_decl import VPGWCService_decl
from models_decl import VPGWCTenant_decl

from django.db import models
from core.models import Service, PlCoreBase, Slice, Instance, Tenant, TenantWithContainer, Node, Image, User, Flavor, NetworkParameter, NetworkParameterType, Port, AddressPool, SlicePrivilege, SitePrivilege
from core.models.plcorebase import StrippedCharField
import os
from django.db import models, transaction
from django.forms.models import model_to_dict
from django.db.models import *
from operator import itemgetter, attrgetter, methodcaller
from core.models import Tag
from core.models.service import LeastLoadedNodeScheduler
import traceback
from xos.exceptions import *
from sets import Set
from xos.config import Config
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class VPGWCService(VPGWCService_decl):
   class Meta:
        proxy = True 

class VPGWCTenant(VPGWCTenant_decl):
   class Meta:
        proxy = True 

   def __init__(self, *args, **kwargs):
       vpgwcservice = VPGWCService.get_service_objects().all()
       # When the tenant is created the default service in the form is set
       # to be the first created HelloWorldServiceComplete
       if vpgwcservice:
           self._meta.get_field(
                "provider_service").default = vpgwcservice[0].id
       super(VPGWCTenant, self).__init__(*args, **kwargs)

   def save(self, *args, **kwargs):
       # Update the instance that was created for this tenant
       super(VPGWCTenant, self).save(*args, **kwargs)
       model_policy_vpgwctenant(self.pk)   

   def delete(self, *args, **kwargs):
       # Delete the instance that was created for this tenant
       self.cleanup_container()
       super(VPGWCTenant, self).delete(*args, **kwargs)

def model_policy_vpgwctenant(pk):
    # This section of code is atomic to prevent race conditions
    with transaction.atomic():
        # We find all of the tenants that are waiting to update
        tenant = VPGWCTenant.objects.select_for_update().filter(pk=pk)
        if not tenant:
            return
        # Since this code is atomic it is safe to always use the first tenant
        tenant = tenant[0]
        tenant.manage_container()
