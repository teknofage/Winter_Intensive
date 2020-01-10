from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

from bson.objectid import ObjectId
from app import app
from unittest import TestCase, main as unittest_main, mock
from unittest.mock import patch
from datetime import datetime

sample_id_list = ['hY7m5jjJ9mM','CQ85sUNBK7w']
# All of these are new mock data that we'll use
sample_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_boycott = {
    'title': 'Donald Trump',
    'description': 'Evil Overlord',
    'time_frame': "datetime.datetime.now()",
    'links': "https://en.wikipedia.org/wiki/Charles_Boycott",
    'comments': "lalala I can't hear you"
}
sample_form_data = {
    'title': sample_boycott['title'],
    'description': sample_boycott['description'],
    'links': sample_boycott['links']
}

class AppTests(TestCase): 
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 
    
    @patch('pymongo.collection.Collection.find')
    def test_show_boycotts(self, mock_find):
        """Test the All boycotts page."""
        # Set up our fake data.
        fake_boycotts = [
            {'title': 'Phillip Morris'},
            {'title': 'Diageo'}
        ]
        # Set fake data as the mock return value for `find`.
        mock_find.return_value = fake_boycotts

        # Load the URL being tested.
        result = self.app.get('/boycotts_show')

        # Check that status code is OK.
        self.assertEqual(result.status_code, 200)

        # Check that the page content contains the 2 songs in our test data.
        page_content = result.get_data(as_text=True)
        self.assertIn('Phillip Morris', page_content)
        self.assertIn('Diageo', page_content)
        
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_boycott(self, mock_find):
        """Test showing a boycott field."""
        mock_find.return_value = sample_boycott

        result = self.app.get(f'/boycott/{sample_id}')
        self.assertEqual(result.status, '200 OK')

# Testing Routes
    def test_index(self):
        """Test the app's homepage."""
        result = self.app.get('/')
        self.assertEqual(result.status, '200 OK')
        
    def test_login(self):
        """Test the app's login page."""
        result = self.app.get('/login')
        self.assertEqual(result.status, '200 OK')
        
    def test_index(self):
        """Test the app's boycotts index page."""
        result = self.app.get('/')
        self.assertEqual(result.status, '200 OK')
        
    def test_boycott_submit(self):
        """Test the app's boycott submit page."""
        result = self.app.get('/boycotts')
        self.assertEqual(result.status, '200 OK')
        
    def test_bocycotts_new(self):
        """Test the app's create new coach page."""
        result = self.app.get('/boycotts/new')
        self.assertEqual(result.status, '200 OK')
        
    def test_boycotts_show(self):
        """Test the app's show all boycotss page."""
        result = self.app.get('/boycotts')
        self.assertEqual(result.status, '200 OK')
        
    def test_boycotts_edit(self):
        """Test the app's Show the edit form for a boycott."""
        result = self.app.get(f'/boycotts/{str(sample_id)}/edit')
        self.assertEqual(result.status, '200 OK')
        page_content = result.get_data(as_text=True)
        self.assertIn('description', page_content)