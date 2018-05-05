from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    email = forms.CharField(max_length=200, required=True)
    comments = forms.CharField(max_length=1000, required=False)