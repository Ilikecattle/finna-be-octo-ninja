from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit

from userena.forms import EditProfileForm
from userena.utils import get_profile_model

class EditProfileFormExtra(EditProfileForm):
    class Meta:
        model = get_profile_model()
        exclude = ['user', 'mugshot', 'privacy']

    def __init__(self, *args, **kwargs):
        super(EditProfileFormExtra, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'edit-profile-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.add_input(Submit('submit', 'Save', css_class='green'))
        self.helper.layout = Layout(
            Field('first_name', placeholder="First Name"),
            Field('last_name', placeholder="Last Name"),
        )
