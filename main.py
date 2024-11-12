from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from typing import Optional
from config import Config
from network.socket_client import SocketClient
from models.user import User, Email
from ui.custom_widgets import LoginWindow, EmailWindow, DialogWindow

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_window = LoginWindow()
        self.add_widget(self.login_window)

class EmailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class EmailClientApp(App):
    def __init__(self):
        super().__init__()
        self.current_user: Optional[User] = None
        self.socket_client = SocketClient(Config.DEFAULT_HOST, Config.DEFAULT_PORT)
        self.screen_manager = ScreenManager()
        
        # Create screens
        self.login_screen = LoginScreen(name='login')
        self.email_screen = EmailScreen(name='email')
        
        # Add screens to manager
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.email_screen)
        
        # Bind buttons
        self.login_screen.login_window.login_button.bind(
            on_release=self.handle_login
        )
        self.login_screen.login_window.register_button.bind(
            on_release=self.handle_register
        )
    
    def build(self):
        """Builds and returns the main widget."""
        return self.screen_manager
    
    def handle_login(self, instance):
        """Processes login attempt."""
        username, password, host, port = (
            self.login_screen.login_window.get_credentials()
        )
        
        try:
            port = int(port)
            self.socket_client = SocketClient(
                host or Config.DEFAULT_HOST,
                port or Config.DEFAULT_PORT
            )
            
            response = self.socket_client.send_request({
                "flag": 0,
                "User": username,
                "Pass": password
            })
            
            if isinstance(response, dict):
                self.current_user = User(username, password)
                self.current_user.emails = [
                    Email.from_dict(email_data) 
                    for email_data in response.get("Email", [])
                ]
                self.show_email_interface()
            else:
                DialogWindow.show_error("Invalid credentials or connection error.")
                
        except ValueError:
            DialogWindow.show_error("Invalid port number")
    
    def handle_register(self, instance):
        """Processes registration attempt."""
        username, password, host, port = (
            self.login_screen.login_window.get_credentials()
        )
        
        try:
            port = int(port)
            self.socket_client = SocketClient(
                host or Config.DEFAULT_HOST,
                port or Config.DEFAULT_PORT
            )
            
            response = self.socket_client.send_request({
                "flag": 3,
                "User": username,
                "Pass": password
            })
            
            message = {
                0: "Invalid username",
                1: "User created successfully!",
                3: "Username already exists"
            }.get(response, "Unknown error")
            
            if response == 1:
                DialogWindow.show_success(message)
            else:
                DialogWindow.show_error(message)
                
        except ValueError:
            DialogWindow.show_error("Invalid port number")
    
    def show_email_interface(self):
        """Switches to the email interface."""
        email_window = EmailWindow(self.current_user.username)
        self.email_screen.clear_widgets()
        self.email_screen.add_widget(email_window)
        
        # Bind email window buttons
        email_window.send_button.bind(on_release=self.handle_send_email)
        email_window.refresh_button.bind(on_release=self.handle_refresh)
        
        if self.current_user and self.current_user.emails:
            email_window.update_email_list(self.current_user.emails)
        
        self.screen_manager.current = 'email'
    
    def handle_send_email(self, instance):
        """Processes email sending."""
        email_window = self.email_screen.children[0]
        message = email_window.get_compose_text()
        
        if not message.strip():
            DialogWindow.show_error("Message cannot be empty")
            return
        
        def send_email_callback(recipient):
            """Callback function that actually sends the email"""
            if recipient:
                response = self.socket_client.send_request({
                    "flag": 1,
                    "User": self.current_user.username,
                    "destinatario": recipient,
                    "conteudo_email": message
                })
                
                if response == 1:
                    DialogWindow.show_success("Email sent successfully!")
                    email_window.clear_compose()
                else:
                    DialogWindow.show_error("Recipient not found")
    
        # Chama get_recipient com o callback
        DialogWindow.get_recipient(send_email_callback)
    
    def handle_refresh(self, instance):
        """Updates the email list."""
        if self.current_user:
            response = self.socket_client.send_request({
                "flag": 0,
                "User": self.current_user.username,
                "Pass": self.current_user.password
            })
            
            if isinstance(response, dict):
                self.current_user.emails = [
                    Email.from_dict(email_data) 
                    for email_data in response.get("Email", [])
                ]
                email_window = self.email_screen.children[0]
                email_window.update_email_list(self.current_user.emails)

if __name__ == "__main__":
    app = EmailClientApp()
    app.run()