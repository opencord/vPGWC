tosca_definitions_version: tosca_simple_yaml_1_0

# compile this with "m4 vpgwc.m4 > vpgwc.yaml"

# include macros
include(macros.m4)

node_types:
    tosca.nodes.VPGWCService:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The vPGWC Service
        capabilities:
            xos_base_service_caps
        properties:
            xos_base_props
            xos_base_service_props
            view_url:
                type: string
                required: false
            icon_url:
                type: string
                required: false
            enabled:
                type: boolean
                required: true
            published:
                type: boolean
                required: true
            public_key:
                type: string
                required: false
            private_key_fn:
                type: string
                required: false
            versionNumber:
                type: string
                required: false

    tosca.nodes.VPGWCTenant:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The vPGWC Tenant
        properties:
            xos_base_tenant_props
            display_message:
                type: string
                required: false
            s5s8_pgw_tag:
                type: string
                required: false
            image_name:
                type: string
                required: false