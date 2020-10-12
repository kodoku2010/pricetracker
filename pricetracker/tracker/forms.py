from django import forms

class AddNewItemForm(forms.Form):
    url = forms.CharField(max_length=200)
    requested_price = forms.IntegerField()