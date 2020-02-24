from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from list.views import home_page
from .models import Item, List

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'list/home.html')


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'the first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'the second list item'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'the first (ever) list item')
        self.assertEqual(second_saved_item.text, 'the second list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list/list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_all_items(self):

        correct_list = List.objects.create()
        Item.objects.create(text='itemey1', list=correct_list)
        Item.objects.create(text='itemey2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other itemey1', list=other_list)
        Item.objects.create(text='other itemey2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'itemey1')
        self.assertContains(response, 'itemey2')
        self.assertNotContains(response, 'other itemey1')
        self.assertNotContains(response, 'other itemey2')

class NewListTest(TestCase):

    def test_can_save_a_post_request(self):

        response = self.client.post(f'/lists/new/', 
                                    data={"item_text": "new_item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new_item')

    def test_redirect_to_correct_list_view_after_creating_list(self):
        
         response = self.client.post('/lists/new/', data={'item_text':'new_item'})
         self.assertRedirects(response, f'/lists/{Item.objects.first().list.id}/')

class NewItemTest(TestCase):
    
    def test_can_save_post_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item/',
                                    data={'item_text' : 'a new item for an existing list'}
                                    )

        self.assertEqual(Item.objects.all().count(), 1)
        self.assertEqual(Item.objects.all().first().text, 'a new item for an existing list')
        self.assertEqual(Item.objects.all().first().list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item/',
                                    data={'item_text' : 'a new item for an existing list'}
                                    )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')



