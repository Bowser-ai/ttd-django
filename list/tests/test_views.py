from unittest import skip

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.utils.html import escape

from list.views import home_page
from list.models import Item, List
from list.forms import ItemForm, ExistingListItemForm,  EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'list/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.pk}/',
                data={'text': ''}
                )

    def test_for_invalid_data_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list/list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_errors_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_validation_errors_shows_on_page(self):
        list_1 = List.objects.create()
        Item.objects.create(text='textey', list=list_1)
        response = self.client.post(f'/lists/{list_1.id}/',
                data={'text': 'textey'})

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list/list.html')
        self.assertEqual(Item.objects.all().count(), 1)

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

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

class NewListTest(TestCase):

    def test_can_save_a_post_request(self):

        response = self.client.post(f'/lists/new/', 
                                    data={"text": "new_item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new_item')

    def test_redirect_to_correct_list_view_after_creating_list(self):
         response = self.client.post('/lists/new/', data={'text':'new_item'})
         self.assertRedirects(response, f'/lists/{Item.objects.first().list.id}/')

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new/', data={'text' : ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new/', data={'text' : ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new/', data={'text' : ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        response = self.client.post('/lists/new/', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(List.objects.all().count(), 0)
        self.assertEqual(Item.objects.all().count(), 0)

    def test_can_save_post_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text' : 'a new item for an existing list'}
                                    )

        self.assertEqual(Item.objects.all().count(), 1)
        self.assertEqual(Item.objects.all().first().text, 'a new item for an existing list')
        self.assertEqual(Item.objects.all().first().list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text' : 'a new item for an existing list'}
                                    )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validations_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list/list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
