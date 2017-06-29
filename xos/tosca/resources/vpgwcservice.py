from service import XOSService
from services.vpgwc.models import VPGWCService

class XOSVPGWCService(XOSService):
    provides = "tosca.nodes.VPGWCService"
    xos_model = VPGWCService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key", "private_key_fn", "versionNumber"]