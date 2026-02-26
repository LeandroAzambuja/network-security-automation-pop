#!/bin/bash
echo "========================================="
echo "STATUS DO PROJETO - Hackers do Bem"
echo "========================================="
echo ""
echo "📁 Estrutura de pastas:"
find . -type d -name "__pycache__" -prune -o -type d -print | sort | sed 's/^/  /'
echo ""
echo "📄 Módulos implementados:"
ls -la coletar/ observar/ logs/ utils/ 2>/dev/null | grep -E "\.py$" | sed 's/^/  /'
echo ""
echo "🧪 Teste rápido do sistema:"
python3 -c "
import sys
sys.path.append('.')
try:
    from logs.logger_config import setup_logger
    from coletar.rustscan_wrapper_fast import RustScanWrapperFast
    from observar.analise_resultados import AnalisadorResultados
    print('  ✅ Todos os módulos carregam corretamente')
except Exception as e:
    print(f'  ❌ Erro: {e}')
"
echo ""
echo "🚀 Para testar a automação completa:"
echo "  python3 main.py --target scanme.nmap.org --scan rapido"
echo ""
echo "📊 Para ver ajuda:"
echo "  python3 main.py --help"
echo ""
echo "========================================="
