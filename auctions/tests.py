from django.test import TestCase
from .models import Category, Listing
from django.contrib.auth.models import User
from .models import User

class CommerceModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='taylor', password='swift')
        self.single_category = Category.objects.create(categoryName='Single')
        self.album_category = Category.objects.create(categoryName='Albums')
        self.single_listing = Listing.objects.create(
            title='Love Story',
            description='Taylor Swift song',
            price=10.99,
            owner=self.user,
            category=self.single_category
        )
        self.album_listing = Listing.objects.create(
            title='1989',
            description='Taylor Swift album',
            price=19.99,
            owner=self.user,
            category=self.album_category
        )

    def test_category_str_representation(self):
        single_category = Category.objects.get(categoryName='Single')
        album_category = Category.objects.get(categoryName='Albums')
        self.assertEqual(str(single_category), 'Category: Single')
        self.assertEqual(str(album_category), 'Category: Albums')

    def test_listing_str_representation(self):
        single_listing = Listing.objects.get(title='Love Story')
        album_listing = Listing.objects.get(title='1989')
        self.assertEqual(str(single_listing), 'The title of the song: Love Story - and is a: Single')
        self.assertEqual(str(album_listing), 'The title of the song: 1989 - and is a: Albums')

    def test_listing_has_owner(self):
        single_listing = Listing.objects.get(title='Love Story')
        album_listing = Listing.objects.get(title='1989')
        self.assertEqual(single_listing.owner, self.user)
        self.assertEqual(album_listing.owner, self.user)

    def test_listing_has_category(self):
        single_listing = Listing.objects.get(title='Love Story')
        album_listing = Listing.objects.get(title='1989')
        self.assertEqual(single_listing.category, self.single_category)
        self.assertEqual(album_listing.category, self.album_category)

    def test_listing_price(self):
        single_listing = Listing.objects.get(title='Love Story')
        album_listing = Listing.objects.get(title='1989')
        self.assertEqual(single_listing.price, 10.99)
        self.assertEqual(album_listing.price, 19.99)


