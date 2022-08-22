from msilib.schema import Class
from re import T
from turtle import pos
from urllib import response
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post, Group, Follow

from django.core.cache import cache

User = get_user_model()
# Create your tests here.

class TestUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'test_user',
            email = 'test@gmail.com',
            password = 'test01'
            )
        self.post = Post.objects.create(
            text = 'this is test text',
            author = self.user
            )
        self.client.login(username = 'test_user', password = 'test01')

    def test_profile(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'test_user'}))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context["page"]), 1)
        self.assertIsInstance(response.context["user"], User)
        self.assertEqual(response.context["current_user"].username, self.user.username)

    def test_new_post_auth(self):
        response = self.client.post(
            reverse('new_post'),
            data = {
                "text": "this is test text"
            }
        )
        response = self.client.get(reverse('profile', kwargs={'username': 'test_user'}))
        self.assertEqual(len(response.context["page"]), 2)
        for url in (
            reverse('index'), 
            reverse('profile', kwargs={'username':'test_user'}), 
            reverse('post', kwargs={'username':'test_user', 'post_id': self.post.id})):

            response = self.client.get(url)
            self.assertContains(response, self.post.text)
        
    def test_new_post_nonauth(self):
        self.client.logout()
        response = self.client.get(reverse('new_post'))
        self.assertRedirects(response, '/auth/login/?next=/new')
    
    def test_post_edit(self):
        self.client.post(
            reverse('post_edit', kwargs={'username': self.user.username, 'post_id': self.post.id}),
            data={
                'text': 'edit text'
            },
            follow=True
            )
        self.post = Post.objects.get(id = self.post.id)
        for url in (
            reverse('index'), 
            reverse('profile', kwargs={'username':'test_user'}), 
            reverse('post', kwargs={'username':'test_user', 'post_id': self.post.id})):

            response = self.client.get(url)
            self.assertContains(response, self.post.text)
 
class TestImage(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'test_user', password = 'test01' )
        self.group = Group.objects.create(title = 'test group', slug = 'test_group', description = 'test group')
        self.client.login(username = 'test_user', password = 'test01') 

    def test_image_on_pages(self):
        cache.clear()
        with open('media/posts/kuni.jpg','rb') as img:
            post = self.client.post(
                reverse('new_post'),
                data = {
                    'text': 'text for twst image',
                    'author': self.user,
                    'group': self.group.id,
                    'image': img

                },
                follow=True
            )
        self.assertEqual(post.status_code, 200),
        self.assertEqual(Post.objects.count(),1)

        post = Post.objects.first()
        
        urls = (
            reverse('index'),
            reverse('group_posts', kwargs = { 'slug':self.group.slug }),
            reverse('profile', kwargs = {'username': post.author.username}),
            reverse('post', kwargs = {'username': post.author.username, 'post_id': post.id})
        )
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<img")
    
    def test_image_proper(self):
        with open('media/posts/koni.txt','rb') as img:
            post = self.client.post(
                reverse('new_post'),
                data = {
                    'text': 'text for twst image',
                    'author': self.user,
                    'group': self.group.id,
                    'image': img

                },
                follow=True
            )
        self.assertEqual(post.status_code, 200)
        self.assertEqual(Post.objects.count(),0)

class TestCache(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = 'test_user', email = 'test@gmail.ru', password = 'test01')
        self.client.force_login(self.user)
    def test_cache_index(self):
        self.client.post(reverse('new_post'), data = {'text':'провкрка кэша'}, follow=True)
        response = self.client.get(reverse('index'))
        self.assertContains(response,'провкрка кэша')
        self.client.post(reverse('new_post'), data = {'text':'провкрка кэша 2'}, follow=True)
        response = self.client.get(reverse('index'))
        self.assertNotContains(response,'провкрка кэша 2')

class TestFollowing(TestCase):
    def setUp(self):
        self.client =Client()
        self.user = User.objects.create_user(username = 'test_user', password = 'test01')
        self.following_user = User.objects.create_user(username = 'following_user', password = 'testfollow')
        self.client.force_login(self.user)
    def test_following(self):
        respomse = self.client.get(reverse('profile_follow', kwargs={'username':self.following_user.username}))
        self.assertEqual(Follow.objects.count(),1)
        respomse = self.client.get(reverse('profile_unfollow', kwargs={'username':self.following_user.username}))
        self.assertEqual(Follow.objects.count(),0)
        self.assertEqual(respomse.status_code,200)




        


        



     
