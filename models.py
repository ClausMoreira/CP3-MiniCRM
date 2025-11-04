# models.py
from datetime import date
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Classe abstrata base para todos os modelos do sistema"""
    
    def __init__(self, created=None):
        self.created = created or date.today().isoformat()
    
    @abstractmethod
    def to_dict(self):
        """Método abstrato para converter objeto em dicionário"""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """Método abstrato para criar objeto a partir de dicionário"""
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__}"

class Lead(BaseModel):
    """Classe representando um lead no sistema CRM"""
    
    def __init__(self, name, email, company="", stage="novo", created=None):
        super().__init__(created)
        self._name = name
        self._email = email
        self.company = company
        self.stage = stage
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Nome não pode ser vazio")
        self._name = value.strip()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not value or "@" not in value:
            raise ValueError("E-mail deve conter @ e ser válido")
        self._email = value.strip()
    
    def to_dict(self):
        """Converte o lead para dicionário (compatível com JSON existente)"""
        return {
            "name": self.name,
            "company": self.company,
            "email": self.email,
            "stage": self.stage,
            "created": self.created
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria um lead a partir de dicionário"""
        return cls(
            name=data["name"],
            email=data["email"],
            company=data.get("company", ""),
            stage=data.get("stage", "novo"),
            created=data.get("created")
        )
    
    def __str__(self):
        return f"Lead: {self.name} ({self.email}) - {self.company} - {self.stage}"

class QualifiedLead(Lead):
    """Classe especializada para leads qualificados com scoring"""
    
    def __init__(self, name, email, company="", score=0, created=None):
        super().__init__(name, email, company, "qualificado", created)
        self.score = max(0, min(100, score))  # Pontuação de 0-100
    
    def to_dict(self):
        """Polimorfismo - adiciona campo score mantendo compatibilidade"""
        data = super().to_dict()
        data["score"] = self.score
        data["type"] = "qualified"  # Marca como lead qualificado
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Polimorfismo - trata campo score"""
        lead = cls(
            name=data["name"],
            email=data["email"],
            company=data.get("company", ""),
            score=data.get("score", 0),
            created=data.get("created")
        )
        return lead
    
    def is_high_value(self):
        """Método específico para identificar leads de alto valor"""
        return self.score >= 80
    
    def __str__(self):
        return f"QualifiedLead: {self.name} - Score: {self.score}/100 - {self.company}"