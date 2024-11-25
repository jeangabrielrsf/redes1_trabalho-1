from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from typing import Callable, List, Tuple, Optional
from models.user import Email

class LoginWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # Title
        title = Label(
            text='Client Login',
            font_size='20sp',
            size_hint_y=None,
            height='40dp'
        )
        self.add_widget(title)
        
        # Username field
        self.username_input = TextInput(
            hint_text='Nickname',
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        self.add_widget(self.username_input)
        
        # Password field
        self.password_input = TextInput(
            hint_text='Senha',
            password=True,
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        self.add_widget(self.password_input)
        
        # IP field
        self.ip_input = TextInput(
            hint_text='IP',
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        self.add_widget(self.ip_input)
        
        # Port field
        self.port_input = TextInput(
            hint_text='Porta',
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        self.add_widget(self.port_input)
        
        # Buttons
        buttons = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='40dp',
            spacing=10
        )
        self.login_button = Button(text='Login')
        self.register_button = Button(text='Criar Usuário')
        buttons.add_widget(self.login_button)
        buttons.add_widget(self.register_button)
        self.add_widget(buttons)
    
    def get_credentials(self) -> Tuple[str, str, str, str]:
        """Returns the credentials entered in the fields."""
        return (
            self.username_input.text,
            self.password_input.text,
            self.ip_input.text,
            self.port_input.text
        )

class EmailWindow(BoxLayout):
    def __init__(self, username: str, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # Welcome message
        welcome = Label(
            text=f'Olá, {username}!',
            font_size='20sp',
            size_hint_y=None,
            height='40dp'
        )
        self.add_widget(welcome)
        
        # Email list
        inbox_label = Label(
            text='Inbox',
            font_size='16sp',
            size_hint_y=None,
            height='30dp'
        )
        self.add_widget(inbox_label)
        
        self.email_list = TextInput(
            readonly=True,
            size_hint=(1, 0.6)
        )
        self.add_widget(self.email_list)
        
        # Compose area
        compose_label = Label(
            text='Escreva uma nova mensagem',
            font_size='16sp',
            size_hint_y=None,
            height='30dp'
        )
        self.add_widget(compose_label)
        
        self.compose_area = TextInput(
            size_hint=(1, 0.3)
        )
        self.add_widget(self.compose_area)
        
        # Buttons
        buttons = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='40dp',
            spacing=10
        )
        self.send_button = Button(text='Enviar Mensagem')
        self.refresh_button = Button(text='Atualizar')
        buttons.add_widget(self.send_button)
        buttons.add_widget(self.refresh_button)
        self.add_widget(buttons)
    
    def update_email_list(self, emails: List[Email]) -> None:
        """Updates the email list in the interface."""
        email_text = ''
        for email in emails:
            email_text += f'De: {email.sender}\n'
            email_text += f'Mensagem: {email.message}\n'
            email_text += '-' * 30 + '\n\n'
        
        self.email_list.text = email_text
    
    def get_compose_text(self) -> str:
        """Returns the composed email text."""
        return self.compose_area.text
    
    def clear_compose(self) -> None:
        """Clears the compose field."""
        self.compose_area.text = ''

class DialogWindow:
    @staticmethod
    def show_error(message: str):
        """Shows an error message."""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
    
    @staticmethod
    def show_success(message: str):
        """Shows a success message."""
        popup = Popup(
            title='Success',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
    
    @staticmethod
    def get_recipient(callback) -> None:
        """
        Requests the recipient's nickname and calls the callback function
        with the recipient value when done.
        """
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        text_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        
        popup = Popup(
            title='Enviar Mensagem',
            content=content,
            size_hint=(None, None),
            size=(300, 200),
            auto_dismiss=False
        )
        
        def set_recipient(instance):
            recipient = text_input.text
            popup.dismiss()
            if recipient.strip():  # Só chama o callback se houver um destinatário
                callback(recipient)
            
        def cancel(instance):
            popup.dismiss()
        
        content.add_widget(Label(text='Entre com o nickname do destinatário:'))
        content.add_widget(text_input)
        
        buttons = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='40dp',
            spacing=10
        )
        ok_button = Button(text='OK')
        ok_button.bind(on_release=set_recipient)
        cancel_button = Button(text='Cancelar')
        cancel_button.bind(on_release=cancel)
        buttons.add_widget(ok_button)
        buttons.add_widget(cancel_button)
        content.add_widget(buttons)
        
        popup.open()