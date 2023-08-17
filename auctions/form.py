from django import forms
from .models import Listing, Bid

class ListingForm(forms.ModelForm):
    custom_price = forms.FloatField(label='Custom Price', required=False)

    class Meta:
        model = Listing
        exclude = ['id', 'owner', 'isActive', 'price']

    def save(self, commit=True):
        custom_price = self.cleaned_data.get('custom_price')
        listing = super().save(commit=False)
        if custom_price is not None:
            bid = Bid.objects.create(bid=custom_price)
            bid.save()
            listing.price = bid
        if commit:
            listing.save()
        return listing
