#!/usr/bin/env python3
"""
Script principal para executar a interface gráfica do Sistema de Gestão de Pedidos
"""

import sys
import os

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    try:
        import matplotlib
        matplotlib.use('TkAgg')  # Configurar backend para tkinter
        import matplotlib.pyplot as plt
    except ImportError:
        print("AVISO: matplotlib não encontrado. Instale com: pip install matplotlib")
        print("Os gráficos não estarão disponíveis até a instalação.")
        input("Pressione Enter para continuar sem gráficos ou Ctrl+C para sair...")
    
    from gui_main import SistemaGestorPedidosGUI
    
    def main():
        """Função principal"""
        print("=" * 60)
        print("    SISTEMA DE GESTÃO DE PEDIDOS - VERSÃO PROFISSIONAL")
        print("=" * 60)
        print("Interface Gráfica com Login e Gráficos Avançados")
        print("Desenvolvido por: Caio Mega")
        print("Contato: (19) 99713-7010 | caioh.mega2018@gmail.com")
        print("-" * 60)
        
        try:
            # Criar e executar aplicação
            app = SistemaGestorPedidosGUI()
            if hasattr(app, 'root'):  # Verifica se o login foi bem-sucedido
                print("Sistema iniciado com sucesso!")
                print("Feche a janela ou use Ctrl+C para encerrar.")
                app.run()
            else:
                print("Login cancelado ou falhou. Sistema não iniciado.")
            
        except KeyboardInterrupt:
            print("\nSistema encerrado pelo usuário.")
        except Exception as e:
            print(f"Erro ao executar sistema: {str(e)}")
            print("\nPossíveis soluções:")
            print("1. Verifique se todos os arquivos estão no mesmo diretório")
            print("2. Instale as dependências: pip install matplotlib")
            print("3. Verifique se o Python tem suporte ao tkinter")
            input("Pressione Enter para sair...")
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Erro ao importar módulos: {str(e)}")
    print("\nDependências necessárias:")
    print("- Python 3.7+")
    print("- tkinter (geralmente incluído com Python)")
    print("- matplotlib (para gráficos): pip install matplotlib")
    print("\nCertifique-se de que todos os arquivos estão no mesmo diretório.")
    input("Pressione Enter para sair...")
except Exception as e:
    print(f"Erro inesperado: {str(e)}")
    input("Pressione Enter para sair...")
