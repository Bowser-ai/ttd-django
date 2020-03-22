from django.test import TestCase
from django.core.exceptions import ValidationError
from list.models import Item, List


class ItemModelsTest(TestCase):
    
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='bla', list=list_)
        with self.assertRaises(ValidationError):
            new_item = Item(text='bla', list=list_)
            new_item.full_clean()

    def test_can_save_duplicate_items_to_different_lists(self):
        list_1 = List.objects.create()
        list_2 = List.objects.create()
        Item.objects.create(text='bla', list=list_1)
        item_2 = Item(text='bla', list=list_2)
        item_2.full_clean() #should not raise

    def test_list_ordering(self):
        list_1 = List.objects.create()
        item_1 = Item.objects.create(text='il1', list=list_1)
        item_2 = Item.objects.create(text='item_2', list=list_1)
        item_3 = Item.objects.create(text='3', list=list_1)
        self.assertEqual(list(Item.objects.all()), [item_1, item_2, item_3])

    def test_string_representation(self):
        item = Item(text='Some text')
        self.assertEqual(str(item), 'Some text')

class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
