from django import forms
from .models import Listing, Bid

class ListingForm(forms.ModelForm):
    custom_price = forms.FloatField(label='Custom Price', required=False)

    class Meta:
        model = Listing
        exclude = ['id', 'owner', 'isActive', 'price']

    def create_custom_price_bid(self):
        custom_price = self.cleaned_data.get('custom_price')
        if custom_price is not None:
            bid = Bid.objects.create(bid=custom_price)
            return bid
        return None

    def save(self, commit=True):
        listing = super().save(commit=False)
        custom_price_bid = self.create_custom_price_bid()
        if custom_price_bid:
            listing.price = custom_price_bid
        if commit:
            listing.save()
        return listing
