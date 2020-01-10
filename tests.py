from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

from bson.objectid import ObjectId
from app import app
from unittest import TestCase, main as unittest_main, mock
from unittest.mock import patch

