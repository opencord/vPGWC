import os
import pdb
import sys
import tempfile
sys.path.append("/opt/tosca")
from translator.toscalib.tosca_template import ToscaTemplate
import pdb

from services.vpgwc.models import VPGWCService

from service import XOSService

class XOSVPGWCService(XOSService):
    provides = "tosca.nodes.VPGWCService"
    xos_model = VPGWCService
    copyin_props = ["view_url", "icon_url", "enabled", "published", "public_key",
                    "private_key_fn", "versionNumber",
                    ]

