from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from .models import Post

# Create your tests here.

# ============================================================
# TESTES DO MODEL POST
# ============================================================

class PostModelTest(TestCase):

    def setUp(self):
        self.user = user.objects.create_user(
            username='febrace',
            password='febrace123'
        )
        self.post = Post.objects.create(
            author = self.user,
            title='Primeiro Post e único Teste',
            text='Texto de exemplo para o teste'
        )

    def teste_post_criado_corretamente(self):
        self.assertEqual(self.post.author.username, 'febrace')
        self.assertEqual(self.post.title, 'Primeiro Post e único Teste')
        self.assertEqual(self.post.text, 'Texto de exemplo para o teste')

    def teste_post_criado_sem_publish_data (self):
        self.assertIsNone(self.post.published_date)

    def teste_post_publicado(self):
        self.post.publish()
        self.assertIsNotNone(self.post.published_date)

    def teste_publish_define_data_proxima_ao_momento_atual():
        antes = timezone.now()
        self.post.publish()
        depois = timezone.now()
        self.assertGreaterEqual(self.post.published_date, antes)
        self.assertLessEqual(self.post.published_date, depois)

# ============================================================
# TESTES DO VIEW POST
# ============================================================

class ModelViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='febrace',
            password='febrace123'    
        )

    def teste_post_list_retorna_200():
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_nao_publicado_nao_aparece_na_lista(self):
        Post.objects.create(
            author=self.user,
            title='Post rascunho',
            text='Ainda não publicado'
        )
        response = self.client.get(reverse('post_list'))
        self.assertNotContains(response, 'Post rascunho')