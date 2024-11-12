import socket
import json
from typing import Any, Dict, Optional
from config import Config

class SocketClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        
    def _recv_full_data(self, sock: socket.socket) -> bytes:
        """Recebe o comprimento da mensagem seguido da mensagem completa."""
        try:
            message_length = int(sock.recv(10).decode().strip())
            data = b""
            while len(data) < message_length:
                data += sock.recv(1024)
            return data
        except ValueError:
            return b'{"erro": "Erro ao receber dados"}'

    def _send_encrypted_data(self, data: str, sock: socket.socket) -> None:
        """Criptografa e envia o JSON via socket."""
        encrypted_data = Config.CIPHER_SUITE.encrypt(data.encode())
        encrypted_length = f"{len(encrypted_data):<10}"
        sock.sendall(encrypted_length.encode() + encrypted_data)

    def send_request(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Envia requisição ao servidor e retorna a resposta processada."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.host, self.port))
                json_data = json.dumps(data)
                self._send_encrypted_data(json_data, sock)
                
                response = self._recv_full_data(sock)
                decrypted_response = Config.CIPHER_SUITE.decrypt(response).decode()
                return json.loads(decrypted_response)
                
            except Exception as e:
                print(f"Error in network communication: {e}")
                return None
