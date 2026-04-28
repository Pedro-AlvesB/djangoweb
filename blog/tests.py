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
        self.user = User.objects.create_user(
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

    def teste_publish_date_maior_create_date(self):
        self.post.publish()
        self.assertGreaterEqual(self.post.published_date, self.post.created_date)

# ============================================================
# TESTES DO VIEW
# ============================================================

class BlogViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='febrace',
            password='febrace123'    
        )

    def teste_post_list_retorna_200(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def teste_acessa_template(self):
        response = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_nao_publicado_nao_aparece_na_lista(self):
        post = Post.objects.create(
            author=self.user,
            title='Post rascunho',
            text='Ainda não publicado'
        )
        response = self.client.get(reverse('post_list'))
        self.assertNotContains(response, 'Post rascunho')

    def test_post_publicado_aparece_na_lista(self):
        post = Post.objects.create(
            author=self.user,
            title='Post publicado',
            text='Texto publicado',
            published_date=timezone.now()
        )
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, 'Post publicado')

class PostDetailViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='febrace',
            password='febrace123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Post detalhado',
            text='Text detalhado',
            published_date=timezone.now()
        )

    def test_post_datail_retorna_200(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_retorna_404_para_post_inexistente(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_exibe_titulo_e_texto(self):
        self.client.login(username="febrace", password="febrace")
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'Post detalhado')
        self.assertContains(response, 'Text detalhado')

class PostNewViewTest(TestCase):

    def setUp(self):
        self.client = Client(),
        self.user = User.objects.create_user(
            username='febrace',
            password='febrace123'
        )
        
    def test_post_new_redireciona_sem_login(self):
        """Criar post sem estar logado redireciona para login"""
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 302)

    def test_post_new_acessivel_com_login(self):
        """Criar post com login retorna 200"""
        self.client.login(username='febrace', password='senha123')
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)

    def test_post_new_cria_post_com_dados_validos(self):
        """POST com dados válidos cria o post e redireciona"""
        self.client.login(username='febrace', password='senha123')
        response = self.client.post(reverse('post_new'), {
            'title': 'Post criado no teste',
            'text': 'Texto do post criado no teste'
        })
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_post_new_nao_cria_com_dados_invalidos(self):
        """POST sem título não cria o post"""
        self.client.login(username='febrace', password='senha123')
        self.client.post(reverse('post_new'), {
            'title': '',  # título vazio = inválido
            'text': 'Texto qualquer'
        })
        self.assertEqual(Post.objects.count(), 0)
    



class PostEditViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='febrace',
            password='senha123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Post original',
            text='Texto original',
            published_date=timezone.now()
        )


    def test_post_edit_redireciona_sem_login(self):
        """Editar post sem login redireciona"""
        response = self.client.get(reverse('post_edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)

    def test_post_edit_acessivel_com_login(self):
        """Editar post com login retorna 200"""
        self.client.login(username='febrace', password='senha123')
        response = self.client.get(reverse('post_edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_edit_atualiza_post(self):
        """Editar post com dados válidos salva as alterações"""
        self.client.login(username='febrace', password='senha123')
        self.client.post(reverse('post_edit', kwargs={'pk': self.post.pk}), {
            'title': 'Título atualizado',
            'text': 'Texto atualizado'
        })
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Título atualizado')