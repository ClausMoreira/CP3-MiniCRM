# app.py
from service import lead_service
from models import Lead, QualifiedLead

class CRMApp:
    """Classe principal da aplicação CRM"""
    
    def __init__(self):
        self.service = lead_service
        self.running = False
    
    def display_menu(self):
        """Exibe menu principal com todas as opções"""
        print("\n" + "="*50)
        print("Mini CRM - Sistema Orientado a Objetos")
        print("="*50)
        print("[1] Adicionar lead")
        print("[2] Adicionar lead qualificado")
        print("[3] Listar todos os leads")
        print("[4] Listar leads qualificados")
        print("[5] Buscar leads")
        print("[6] Estatísticas")
        print("[7] Promover lead para qualificado")
        print("[8] Exportar para CSV")
        print("[0] Sair")
        print("="*50)
    
    def add_lead_interaction(self, qualified=False):
        """Gerencia interação de adição de lead (regular ou qualificado)"""
        try:
            print(f"\nAdicionar {'Lead Qualificado' if qualified else 'Lead'}")
            print("-" * 30)
            
            name = input("Nome: ").strip()
            company = input("Empresa: ").strip()
            email = input("E-mail: ").strip()
            
            if qualified:
                score_input = input("Score (0-100): ").strip()
                score = int(score_input) if score_input.isdigit() else 0
                score = max(0, min(100, score))  # Garante range 0-100
                
                lead = self.service.create_lead(
                    name, email, company, qualify=True, score=score
                )
                print(f"Lead qualificado adicionado! Score: {score}/100")
            else:
                lead = self.service.create_lead(name, email, company)
                print("Lead adicionado com sucesso!")
            
            print(f"Detalhes: {lead}")
            
        except ValueError as e:
            print(f"Erro de validação: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
    
    def list_leads_interaction(self, qualified_only=False):
        """Exibe lista de leads formatada"""
        try:
            if qualified_only:
                leads = self.service.list_qualified()
                title = "LEADS QUALIFICADOS"
            else:
                leads = self.service.list_all()
                title = "TODOS OS LEADS"
            
            if not leads:
                print(f"Nenhum lead{' qualificado ' if qualified_only else ' '}encontrado.")
                return
            
            print(f"\n{title}")
            print("="*80)
            print(f"{'#':2} | {'Tipo':<10} | {'Nome':<20} | {'Empresa':<18} | {'E-mail':<20} | {'Info':<10}")
            print("-" * 80)
            
            for i, lead in enumerate(leads):
                lead_type = "Qualificado" if isinstance(lead, QualifiedLead) else "Regular"
                extra_info = f"Score: {lead.score}" if isinstance(lead, QualifiedLead) else lead.stage
                
                print(f"{i:02d} | {lead_type:<10} | {lead.name:<20} | {lead.company:<18} | {lead.email:<20} | {extra_info:<10}")
            
            print(f"\nTotal: {len(leads)} lead(s)")
                
        except Exception as e:
            print(f"Erro ao listar leads: {e}")
    
    def search_leads_interaction(self):
        """Gerencia busca de leads"""
        try:
            query = input("\nBuscar por (nome, empresa ou e-mail): ").strip()
            if not query:
                print("Digite um termo para buscar.")
                return
            
            results = self.service.search(query)
            
            if not results:
                print("Nenhum lead encontrado com esses critérios.")
                return
            
            print(f"\nRESULTADOS DA BUSCA: '{query}'")
            print("="*60)
            for i, lead in enumerate(results):
                lead_type = "[Q]" if isinstance(lead, QualifiedLead) else "[R]"
                print(f"{i+1:2d}. {lead_type} {lead.name} | {lead.company} | {lead.email}")
            
            print(f"\nEncontrados: {len(results)} lead(s)")
            
        except Exception as e:
            print(f"Erro na busca: {e}")
    
    def show_statistics(self):
        """Exibe estatísticas dos leads"""
        try:
            stats = self.service.get_stats()
            print("\nESTATÍSTICAS DOS LEADS")
            print("="*30)
            print(f"Total de leads: {stats['total']}")
            print(f"Leads regulares: {stats['regular']}")
            print(f"Leads qualificados: {stats['qualified']}")
            print(f"High-value leads: {stats['high_value']}")
            
            if stats['total'] > 0:
                qual_rate = (stats['qualified'] / stats['total']) * 100
                high_value_rate = (stats['high_value'] / stats['total']) * 100
                print(f"Taxa de qualificação: {qual_rate:.1f}%")
                print(f"Taxa de high-value: {high_value_rate:.1f}%")
                
        except Exception as e:
            print(f"Erro ao gerar estatísticas: {e}")
    
    def promote_lead_interaction(self):
        """Gerencia promoção de lead regular para qualificado"""
        try:
            email = input("\nE-mail do lead a promover: ").strip()
            if not email:
                print("E-mail é obrigatório.")
                return
            
            score_input = input("Score (0-100): ").strip()
            score = int(score_input) if score_input.isdigit() else 0
            
            qualified_lead = self.service.promote_lead(email, score)
            print("Lead promovido para qualificado!")
            print(f"Detalhes: {qualified_lead}")
            
        except ValueError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
    
    def export_csv_interaction(self):
        """Gerencia exportação para CSV"""
        try:
            path = self.service.export_to_csv()
            if path is None:
                print("Nao foi possivel escrever o CSV. Verifique se o arquivo esta aberto.")
            else:
                print(f"Exportado com sucesso para: {path}")
                
        except Exception as e:
            print(f"Erro na exportacao: {e}")
    
    def run(self):
        """Método principal que executa a aplicação"""
        self.running = True
        print("Mini CRM OOP Iniciado!")
        print("Sistema desenvolvido com Orientacao a Objetos: Classes, Heranca e Polimorfismo")
        
        while self.running:
            try:
                self.display_menu()
                choice = input("Escolha uma opcao: ").strip()
                
                if choice == "1":
                    self.add_lead_interaction(qualified=False)
                elif choice == "2":
                    self.add_lead_interaction(qualified=True)
                elif choice == "3":
                    self.list_leads_interaction(qualified_only=False)
                elif choice == "4":
                    self.list_leads_interaction(qualified_only=True)
                elif choice == "5":
                    self.search_leads_interaction()
                elif choice == "6":
                    self.show_statistics()
                elif choice == "7":
                    self.promote_lead_interaction()
                elif choice == "8":
                    self.export_csv_interaction()
                elif choice == "0":
                    print("\nObrigado por usar o Mini CRM! Ate mais!")
                    self.running = False
                else:
                    print("Opcao invalida. Tente novamente.")
                    
            except KeyboardInterrupt:
                print("\nAplicacao interrompida pelo usuario.")
                self.running = False
            except Exception as e:
                print(f"Erro inesperado: {e}")

def main():
    """Função principal para compatibilidade"""
    app = CRMApp()
    app.run()

# Funções de compatibilidade com código existente
def add_flow():
    """Compatibilidade com app.py original"""
    app = CRMApp()
    app.add_lead_interaction(qualified=False)

def list_flow():
    """Compatibilidade com app.py original"""
    app = CRMApp()
    app.list_leads_interaction(qualified_only=False)

def print_menu():
    """Compatibilidade com app.py original"""
    print("\nMini CRM de Leads — Sistema OOP")
    print("[1] Adicionar lead")
    print("[2] Listar leads")
    print("[0] Sair")

if __name__ == "__main__":
    main()