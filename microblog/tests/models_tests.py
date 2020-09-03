from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from microblog.models import Post, Comment


class PostTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@mail.com", password="pass"
        )
        token = Token.objects.create(user=self.user)
        self.client.login(username="test@mail.com", password="pass")
        self.client.credentials(HTTP_TOKEN="Token " + token.key)

    def test_post_add(self):
        data = {"content": "test content"}
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.first().content, "test content")

    def test_post_add_no_data(self):
        data = {}
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

    def test_get_posts_by_user(self):
        user_post = Post.objects.create(
            author=self.user,
            content="test content",
        )
        response = self.client.get("/api/post/get_posts_by_user/testuser")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_post.id, response.data[0].id)

    def test_get_posts_by_user_no_posts(self):
        response = self.client.get("/api/post/get_posts_by_user/testuser")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_posts_by_tag(self):
        user_post = Post.objects.create(
            author=self.user, content="test content #test", tags="test"
        )
        response = self.client.get("/api/post/get_posts_by_tag/test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_post.tags, response.data[0].tags)

    def test_get_posts_by_tag_no_tags(self):
        user_post = Post.objects.create(
            author=self.user,
            content="test content",
        )
        response = self.client.get("/api/post/get_posts_by_tag/test")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data)
