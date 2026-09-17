from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    # Hidden from people, tempting to bots. A filled value means we drop the message.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
        label="Leave this field empty",
    )

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "interest", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@email.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "Optional"}),
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Tell Miriam who the book is for, how many pages "
                    "you have in mind, and when you need it.",
                }
            ),
        }
        labels = {
            "name": "Name",
            "email": "Email",
            "phone": "Your phone (optional)",
            "interest": "What are you after",
            "message": "Your message",
        }

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError(
                "Add a little more detail so Miriam can quote you properly."
            )
        return message

    def is_spam(self):
        return bool(self.cleaned_data.get("website"))
