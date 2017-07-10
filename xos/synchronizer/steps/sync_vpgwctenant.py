import os
import sys
#from django.db.models import Q, F
#from services.vpgwc.models import VPGWCService, VPGWCTenant
#from synchronizers.base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible
from synchronizers.new_base.modelaccessor import *

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

class SyncVPGWCTenant(SyncInstanceUsingAnsible):

    provides = [VPGWCTenant]

    observes = VPGWCTenant

    requested_interval = 0

    template_name = "vpgwctenant_playbook.yaml"

    service_key_name = "/opt/xos/configurations/mcord/mcord_private_key"

    def __init__(self, *args, **kwargs):
        super(SyncVPGWCTenant, self).__init__(*args, **kwargs)

#    def fetch_pending(self, deleted):
#
#        if (not deleted):
#            objs = VPGWCTenant.get_tenant_objects().filter(
#                Q(enacted__lt=F('updated')) | Q(enacted=None), Q(lazy_blocked=False))
#        else:
#
#            objs = VPGWCTenant.get_deleted_tenant_objects()
#
#        return objs

    def get_vpgwc(self, o):
        if not o.provider_service:
            return None

        vpgwc = VPGWCService.objects.filter(id=o.provider_service.id)

        if not vpgwc:
            return None

        return vpgwc[0]


    # Gets the attributes that are used by the Ansible template but are not
    # part of the set of default attributes.
    def get_extra_attributes(self, o):
        fields = {}
        fields['tenant_message'] = o.tenant_message
        vpgwc = self.get_vpgwc(o)
        fields['service_message'] = vpgwc.service_message
        return fields
        # return {"display_message": o.display_message,
        #        "s5s8_pgw_tag": o.s5s8_pgw_tag,
        #        "image_name": o.image_name,
        #       }