from services.vpgwc.models import VPGWCService
from service import XOSService

class XOSVPGWCService(XOSService):
    provides = "tosca.nodes.VPGWCService"
    xos_model = VPGWCService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key",
                    "private_key_fn", "versionNumber",
                    ]

