# service.py
from models import Lead, QualifiedLead
from repository import lead_repository

class LeadService:
    """Classe de serviço para operações de negócio com leads"""
    
    def __init__(self, repository=None):
        self.repository = repository or lead_repository
    
    def create_lead(self, name, email, company="", qualify=False, score=0):
        """Factory method para criar leads (aplicando polimorfismo)"""
        # Validações compatíveis com sistema existente
        if not name or not name.strip():
            raise ValueError("Nome é obrigatório")
        if not email or "@" not in email:
            raise ValueError("E-mail válido é obrigatório")
        
        # Verifica duplicata
        existing_lead = self.repository.get_by_email(email)
        if existing_lead:
            raise ValueError(f"Lead com e-mail {email} já existe")
        
        # Cria o lead apropriado baseado no tipo
        if qualify:
            lead = QualifiedLead(name.strip(), email.strip(), company.strip(), score)
        else:
            lead = Lead(name.strip(), email.strip(), company.strip())
        
        self.repository.add(lead)
        return lead
    
    def list_all(self):
        """Retorna todos os leads"""
        return self.repository.list_all()
    
    def list_qualified(self):
        """Retorna apenas leads qualificados"""
        all_leads = self.repository.list_all()
        return [lead for lead in all_leads if isinstance(lead, QualifiedLead)]
    
    def search(self, query):
        """Busca leads por termo"""
        return self.repository.search(query)
    
    def get_stats(self):
        """Retorna estatísticas dos leads"""
        leads = self.repository.list_all()
        total = len(leads)
        qualified = len([lead for lead in leads if isinstance(lead, QualifiedLead)])
        high_value = len([lead for lead in leads 
                         if isinstance(lead, QualifiedLead) and lead.is_high_value()])
        
        return {
            "total": total,
            "qualified": qualified,
            "high_value": high_value,
            "regular": total - qualified
        }
    
    def promote_lead(self, email, score=0):
        """Promove um lead regular para qualificado"""
        lead = self.repository.get_by_email(email)
        if not lead:
            raise ValueError("Lead não encontrado")
        
        if isinstance(lead, QualifiedLead):
            raise ValueError("Lead já é qualificado")
        
        # Remove lead regular e adiciona como qualificado
        leads = self.repository.list_all()
        leads = [l for l in leads if l.email != email]
        
        qualified_lead = QualifiedLead(
            name=lead.name,
            email=lead.email,
            company=lead.company,
            score=score,
            created=lead.created
        )
        
        leads.append(qualified_lead)
        self.repository._save_leads(leads)
        return qualified_lead
    
    def export_to_csv(self):
        """Exporta leads para CSV"""
        return self.repository.export_csv()

# Instância global do serviço
lead_service = LeadService()