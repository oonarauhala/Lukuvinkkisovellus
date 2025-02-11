import unittest
from repositories.user_repository import UserRepository
from repositories.blog_repository import BlogRepository
from app import app
from db import db
from entities.blog import Blog
from entities.user import User
from tests.database_test_helper import Database_test_helper as dth


class TestBlogRepository(unittest.TestCase):
    def setUp(self):
        self.dth = dth(db)
        self.dth.delete()
        self.blog_repository = BlogRepository(db)
        self.user_repository = UserRepository(db)
        self.test_blog = Blog("test_author", "blog_title", "www.blog.com", "a fine blog")
        self.other_blog = Blog("test_author", "other_blog_title", "www.blog.com", "another fine blog")
        self.empty_blog = None
        self.test_user = User("tester", "tester123")
        self.other_user = User("other", "other123")
        self.user_repository.add_user(self.test_user)
        self.user_repository.add_user(self.other_user)
        self.user_id = self.user_repository.get_user(self.test_user)[0]
        self.other_id = self.user_repository.get_user(self.other_user)[0]

    def test_add_book_with_valid_params(self):
        self.assertTrue(self.blog_repository.add_blog(self.test_blog, self.user_id))

    def test_add_book_with_invalid_params(self):
        self.assertFalse(self.blog_repository.add_blog(self.empty_blog, self.user_id))

    def test_user_gets_all_blogs(self):
        self.blog_repository.add_blog(self.test_blog, self.user_id)
        self.blog_repository.add_blog(self.other_blog, self.user_id)
        blogs = self.blog_repository.get_users_blogs(self.user_id)

        self.assertTrue(len(blogs), 2)
        
    def test_user_gets_does_not_get_others_blogs(self):
        self.blog_repository.add_blog(self.test_blog, self.user_id)
        self.blog_repository.add_blog(self.other_blog, self.other_id)
        blogs = self.blog_repository.get_users_blogs(self.user_id)

        self.assertTrue(len(blogs), 1)
        
    def test_user_marks_blog_finished_and_it_is(self):
        self.blog_repository.add_blog(self.test_blog, self.user_id)
        
        blogs = self.blog_repository.get_users_blogs(self.user_id)
        blog_id = blogs[0][0]
        self.blog_repository.mark_finished(blog_id)

        blogs = self.blog_repository.get_users_blogs(self.user_id)
        blog = blogs[0]
        time_stamp = blog.marked_read
        self.assertIsNotNone(time_stamp)

    def test_is_user_owner_of_blog(self):
        self.blog_repository.add_blog(self.test_blog, self.user_id)

        blogs = self.blog_repository.get_users_blogs(self.user_id)
        blog = blogs[0]
        
        result = self.blog_repository.is_owner(self.user_id, blog.id)
        
        self.assertTrue(result)
        
    def test_user_is_not_owner_of_blog(self):
        self.blog_repository.add_blog(self.test_blog, self.other_id)

        blogs = self.blog_repository.get_users_blogs(self.other_id)
        blog = blogs[0]
        
        result = self.blog_repository.is_owner(self.user_id, blog.id)
        
        self.assertFalse(result)
        