from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Listing, Bid, Comment

User = get_user_model()

class CommerceModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='taylor', password='swift')
        self.single_category = Category.objects.create(categoryName='Single')
        self.album_category = Category.objects.create(categoryName='Albums')
        self.single_bid = Bid.objects.create(bid=10.99, user=self.user)
        self.album_bid = Bid.objects.create(bid=19.99, user=self.user)
        self.single_listing = Listing.objects.create(
            title='Love Story',
            description='Taylor Swift song',
            price=self.single_bid,
            owner=self.user,
            category=self.single_category
        )
        self.album_listing = Listing.objects.create(
            title='1989',
            description='Taylor Swift album',
            price=self.album_bid,
            owner=self.user,
            category=self.album_category
        )
        self.comment = Comment.objects.create(
            author=self.user,
            listing=self.single_listing,
            message='Great song!'
        )

    def test_category_str_representation(self):
        single_category = Category.objects.get(categoryName='Single')
        album_category = Category.objects.get(categoryName='Albums')
        self.assertEqual(str(single_category), 'Category: Single')
        self.assertEqual(str(album_category), 'Category: Albums')

    def test_listing_str_representation(self):
        single_listing = Listing.objects.get(title='Love Story')
        album_listing = Listing.objects.get(title='1989')
        self.assertEqual(
            str(single_listing),
            'The title of the song: Love Story - and is a: Single'
        )
        self.assertEqual(
            str(album_listing),
            'The title of the song: 1989 - and is a: Albums'
        )

    def test_listing_has_owner(self):
        self.assertEqual(self.single_listing.owner, self.user)
        self.assertEqual(self.album_listing.owner, self.user)

    def test_listing_has_category(self):
        self.assertEqual(self.single_listing.category, self.single_category)
        self.assertEqual(self.album_listing.category, self.album_category)

    def test_listing_price(self):
        self.assertEqual(self.single_listing.price.bid, 10.99)
        self.assertEqual(self.album_listing.price.bid, 19.99)

    def test_comment_str_representation(self):
        self.assertEqual(
            str(self.comment),
            f"{self.user} commented on {self.single_listing}"
        )
