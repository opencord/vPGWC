
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



from core.admin import ReadOnlyAwareAdmin, SliceInline
from core.middleware import get_request
from core.models import User
from django import forms
from django.contrib import admin
from services.vpgwc.models import VPGWCService, VPGWCTenant, MCORD_KIND

class VPGWCServiceForm(forms.ModelForm):

    class Meta:
        model = VPGWCService
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VPGWCServiceForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return super(VPGWCServiceForm, self).save(commit=commit)

# The class to provide an admin interface on the web for the service.
# We do only configuration here and don't change any logic because the logic
# is taken care of for us by ReadOnlyAwareAdmin
class VPGWCServiceAdmin(ReadOnlyAwareAdmin):
    # We must set the model so that the admin knows what fields to use
    model = VPGWCService
    verbose_name = "vPGWC Service"
    verbose_name_plural = "vPGWC Services"
    # Inlines are used to denote other models that can be edited on the same
    # form as this one. In this case the service form also allows changes
    # to slices.
    inlines = [SliceInline]

    # Setting list_display creates columns on the admin page, each value here
    # is a column, the column is populated for every instance of the model.
    list_display = ("backend_status_icon", "name", "enabled")

    # Used to indicate which values in the columns of the admin form are links.
    list_display_links = ('backend_status_icon', 'name', )

    # Denotes the sections of the form, the fields in the section, and the
    # CSS classes used to style them. We represent this as a set of tuples, each
    # tuple as a name (or None) and a set of fields and classes.
    # Here the first section does not have a name so we use none. That first
    # section has several fields indicated in the 'fields' attribute, and styled
    # by the classes indicated in the 'classes' attribute. The classes given
    # here are important for rendering the tabs on the form. To give the tabs
    # we must assign the classes suit-tab and suit-tab-<name> where
    # where <name> will be used later.
    fieldsets = [(None, {'fields': ['backend_status_text', 'name', 'enabled',
                                    'versionNumber', 'description', "view_url"],
                         'classes':['suit-tab suit-tab-general']})]

    # Denotes the fields that are readonly and cannot be changed.
    readonly_fields = ('backend_status_text', )

    extracontext_registered_admins = True

    # Denotes the fields that can be changed by an admin but not be all users
    user_readonly_fields = ["name", "enabled", "versionNumber", "description"]

    # Associates fieldsets from this form and from the inlines.
    # The format here are tuples, of (<name>, tab title). <name> comes from the
    # <name> in the fieldsets.
    suit_form_tabs = (('general', 'vPGWC Service Details'),
                      ('administration', 'Components'),
                      ('slices', 'Slices'),)

    # Used to include a template for a tab. Here we include the
    # helloworldserviceadmin template in the top position for the administration
    # tab.
    suit_form_includes = (('mcordadmin.html',
                           'top',
                           'administration'),)

    # Used to get the objects for this model that are associated with the
    # requesting user.
    def queryset(self, request):
        return VPGWCService.get_service_objects_by_user(request.user)

# Class to represent the form to add and edit tenants.
# We need to define this instead of just using an admin like we did for the
# service because tenants vary more than services and there isn't a common form.
# This allows us to change the python behavior for the admin form to save extra
# fields and control defaults.
class VPGWCTenantForm(forms.ModelForm):

    class Meta:
        model = VPGWCTenant
        fields = '__all__'
    # Defines a field for the creator of this service. It is a dropdown which
    # is populated with all of the users.
    creator = forms.ModelChoiceField(queryset=User.objects.all())
    # Defines a text field for the display message, it is not required.
    display_message = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(VPGWCTenantForm, self).__init__(*args, **kwargs)
        # Set the kind field to readonly
        self.fields['kind'].widget.attrs['readonly'] = True
        self.fields['kind'].initial = "vpgwc"
        # Define the logic for obtaining the objects for the provider_service
        # dropdown of the tenant form.
        self.fields[
            'provider_service'].queryset = VPGWCService.get_service_objects().all()
        # Set the initial kind to HELLO_WORLD_KIND for this tenant.
        self.fields['kind'].initial = MCORD_KIND
        # If there is an instance of this model then we can set the initial
        # form values to the existing values.
        if self.instance:
            self.fields['creator'].initial = self.instance.creator
            self.fields[
                'display_message'].initial = self.instance.display_message
            self.fields[
                'image_name'].initial = self.instance.image_name

        # If there is not an instance then we need to set initial values.
        if (not self.instance) or (not self.instance.pk):
            self.fields['creator'].initial = get_request().user
            if VPGWCService.get_service_objects().exists():
                self.fields["provider_service"].initial = VPGWCService.get_service_objects().all()[0]
    # This function describes what happens when the save button is pressed on
    # the tenant form. In this case we set the values for the instance that were
    # entered.
    def save(self, commit=True):
        self.instance.creator = self.cleaned_data.get("creator")
        self.instance.display_message = self.cleaned_data.get(
            "display_message")
        return super(VPGWCTenantForm, self).save(commit=commit)


# Define the admin form for the tenant. This uses a similar structure as the
# service but uses HelloWorldTenantCompleteForm to change the python behavior.
class VPGWCTenantAdmin(ReadOnlyAwareAdmin):
    verbose_name = "vPGWC Service Tenant"
    verbose_name_plural = "vPGWC Service Tenants"
    form = VPGWCTenantForm

    list_display = ('id', 'backend_status_icon', 'instance', 'display_message', 'image_name')
    list_display_links = ('backend_status_icon', 'instance', 'display_message', 'id', 'image_name')
    fieldsets = [(None, {'fields': ['backend_status_text', 'kind',
                                    'provider_service', 'instance', 'creator',
                                    'display_message'],
                         'classes': ['suit-tab suit-tab-general']})]
    readonly_fields = ('backend_status_text', 'instance',)


    suit_form_tabs = (('general', 'Details'),)

    def queryset(self, request):
        return VPGWCTenant.get_tenant_objects_by_user(request.user)

# Associate the admin forms with the models.
admin.site.register(VPGWCService, VPGWCServiceAdmin)
admin.site.register(VPGWCTenant, VPGWCTenantAdmin)
