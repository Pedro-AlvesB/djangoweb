from django.test import TestCase
from django.contrib.auth.models import User
from perfis.forms import RegisterUserForm

# Create your tests here.
class EmailValidacaoTest(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='febrace',
            email='febrace@email.com',
            password='senha123'
        )

    def test_email_duplicado_invalida_formulario(self):
        form = RegisterUserForm(data={
            'username': 'outro',
            'email': 'febrace@email.com',  # email já existe!
            'password': 'senha123'
        })
        self.assertFalse(form.is_valid())  # deve ser inválido

    def test_email_novo_valida_formulario(self):
        form = RegisterUserForm(data={
            'username': 'novo',
            'email': 'novo@email.com',  # email novo
            'password': 'senha123'
        })
        self.assertTrue(form.is_valid())  # deve ser válido