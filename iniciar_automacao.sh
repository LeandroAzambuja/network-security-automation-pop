#!/bin/bash
# Script de inicialização da automação RustScan+DefectDojo

echo "🚀 Iniciando Automação de Segurança"
echo "===================================="

# Ativar ambiente virtual
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
else
    echo "❌ Ambiente virtual não encontrado. Execute: python3 -m venv venv"
    exit 1
fi

# Verificar dependências
echo "Verificando dependências..."
python3 -c "import yaml, nmap, requests; print('✅ Dependências OK')" 2>/dev/null || {
    echo "❌ Algumas dependências faltando"
    echo "Instalando..."
    pip install -r requirements.txt 2>/dev/null || echo "⚠️  Verifique manualmente"
}

# Menu principal
echo ""
echo "OPÇÕES DISPONÍVEIS:"
echo "1. Modo teste (verificar ambiente)"
echo "2. Executar com alvos de teste"
echo "3. Executar com alvos personalizados"
echo "4. Ajuda"
echo ""
read -p "Escolha uma opção (1-4): " opcao

case $opcao in
    1)
        python3 main_simples.py --test
        ;;
    2)
        python3 main_simples.py --alvos alvos_teste.conf
        ;;
    3)
        read -p "Digite o alvo (ex: 192.168.1.1) ou caminho do arquivo: " entrada
        if [ -f "$entrada" ]; then
            python3 main_simples.py --alvos "$entrada"
        else
            python3 main_simples.py --target "$entrada"
        fi
        ;;
    4)
        python3 main_simples.py --help
        ;;
    *)
        echo "Opção inválida"
        ;;
esac

echo ""
echo "✅ Execução concluída!"
