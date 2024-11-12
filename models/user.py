from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Email:
    sender: str
    message: str

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Email':
        return cls(
            sender=data.get('id', 'Unknown'),
            message=data.get('Mensagem', '')
        )

@dataclass
class User:
    username: str
    password: str
    emails: List[Email] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "User": self.username,
            "Pass": self.password
        }

    def save_emails(self, filename: str) -> None:
        """Salva os emails do usuário em um arquivo JSON."""
        if self.emails:
            with open(f"{filename}.json", "w") as f:
                json.dump({"Email": [
                    {"id": email.sender, "Mensagem": email.message}
                    for email in self.emails
                ]}, f)
