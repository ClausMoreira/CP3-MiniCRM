# stages.py
from datetime import date
from models import Lead

# Mantém compatibilidade com código existente
STAGES = ["novo", "qualificado", "contatado", "proposta", "fechado"]

class StageManager:
    """Gerenciador de estágios do lead com métodos de classe"""
    
    @classmethod
    def get_available_stages(cls):
        """Retorna estágios disponíveis"""
        return STAGES.copy()
    
    @classmethod
    def get_stage_display_name(cls, stage):
        """Retorna nome amigável do estágio"""
        stage_names = {
            "novo": "Novo Lead",
            "qualificado": "Qualificado", 
            "contatado": "Contatado",
            "proposta": "Proposta Enviada",
            "fechado": "Fechado"
        }
        return stage_names.get(stage, stage)
    
    @classmethod
    def create_lead_object(cls, name, email, company=""):
        """Factory method para criar objeto Lead"""
        return Lead(name, email, company)

# Funções de compatibilidade com sistema existente
def new_lead(name, company, email):
    """Função de compatibilidade - cria lead como dicionário"""
    lead = Lead(name, email, company)
    return lead.to_dict()

def model_lead(name, company, email):
    """Função de compatibilidade com app10.py"""
    return new_lead(name, company, email)