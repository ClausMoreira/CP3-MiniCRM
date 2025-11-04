# repository.py
from pathlib import Path
import json
import csv
from models import Lead, QualifiedLead

class LeadRepository:
    """Classe para gerenciar persistência de leads com herança"""
    
    def __init__(self, db_path=None):
        self.DATA_DIR = Path(__file__).resolve().parent / "data"
        self.DATA_DIR.mkdir(exist_ok=True)
        self.DB_PATH = db_path or (self.DATA_DIR / "leads.json")
    
    def _load_leads(self):
        """Carrega leads do arquivo JSON - compatível com estrutura existente"""
        if not self.DB_PATH.exists():
            return []
        try:
            data = json.loads(self.DB_PATH.read_text(encoding="utf-8"))
            return self._deserialize_leads(data)
        except json.JSONDecodeError:
            return []
    
    def _deserialize_leads(self, data_list):
        """Desserializa dados JSON para objetos Lead/QualifiedLead (polimorfismo)"""
        leads = []
        for data in data_list:
            if data.get("type") == "qualified":
                leads.append(QualifiedLead.from_dict(data))
            else:
                leads.append(Lead.from_dict(data))
        return leads
    
    def _save_leads(self, leads):
        """Salva lista de leads no arquivo JSON"""
        serialized_data = [lead.to_dict() for lead in leads]
        self.DB_PATH.write_text(
            json.dumps(serialized_data, ensure_ascii=False, indent=2), 
            encoding="utf-8"
        )
    
    def list_all(self):
        """Retorna todos os leads"""
        return self._load_leads()
    
    def add(self, lead):
        """Adiciona um novo lead (polimorfismo na aceitação)"""
        if not isinstance(lead, (Lead, QualifiedLead)):
            raise TypeError("Objeto deve ser do tipo Lead ou QualifiedLead")
        
        leads = self._load_leads()
        leads.append(lead)
        self._save_leads(leads)
        return lead
    
    def search(self, query):
        """Busca leads por termo (nome, empresa ou email)"""
        if not query:
            return []
        
        query = query.lower()
        leads = self._load_leads()
        results = []
        
        for lead in leads:
            search_text = f"{lead.name} {lead.company} {lead.email}".lower()
            if query in search_text:
                results.append(lead)
        
        return results
    
    def get_by_email(self, email):
        """Busca lead específico por e-mail"""
        leads = self._load_leads()
        for lead in leads:
            if lead.email.lower() == email.lower():
                return lead
        return None
    
    def export_csv(self, path=None):
        """Exporta leads para CSV - mantém funcionalidade existente"""
        path = Path(path) if path else (self.DATA_DIR / "leads.csv")
        leads = self._load_leads()
        
        try:
            with path.open("w", newline="", encoding="utf-8") as f:
                # Fieldnames compatíveis com estrutura existente
                fieldnames = ["name", "company", "email", "stage", "created"]
                
                # Verifica se há leads qualificados para adicionar campo score
                if any(isinstance(lead, QualifiedLead) for lead in leads):
                    fieldnames.append("score")
                    fieldnames.append("type")
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for lead in leads:
                    writer.writerow(lead.to_dict())
            
            return path
        except PermissionError:
            return None
    
    def count(self):
        """Retorna quantidade total de leads"""
        return len(self._load_leads())

# Instância global para compatibilidade
lead_repository = LeadRepository()