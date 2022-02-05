from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from booking import models


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_action = "."
        self.helper.layout = Layout(
            Fieldset(
                '',
                'user',
                'start_date',
                'end_date',
                'scheduled_room',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-sm btn-primary')
            )
        )

    class Meta:
        model = models.Booking
        fields = [
            "user",
            "start_date",
            "end_date",
            "scheduled_room",
        ]
