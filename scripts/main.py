#!/usr/bin/env python3
"""
Sistema de Gestão de Pedidos
Versão 1.0

Sistema completo para gerenciamento de clientes, produtos e pedidos
com interface de linha de comando e relatórios avançados.

Autor: caio mega 
Data: 2025
"""

import sys
import os
from interface_usuario import InterfaceUsuario

def main():
    """Função principal do sistema"""
    try:
        print("Inicializando Sistema de Gestão de Pedidos...")
        print("Versão 1.0 - Sistema Profissional Completo\n")
        
        # Criar instância da interface
        interface = InterfaceUsuario()
        
        # Executar sistema
        interface.executar()
        
    except KeyboardInterrupt:
        print("\n\nSistema interrompido pelo usuário.")
        print("Até logo!")
        
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("Por favor, contate o suporte técnico.")
        sys.exit(1)

if __name__ == "__main__":
    main()
