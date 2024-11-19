# trie-compressor

### Usando o pytest:

Para rodar todos os testes basta executar pytest -v -s que será exibido todos os testes.

Para rodar um teste específico, basta executar pytest -v -s nome_do_teste.

Para exibir o coverage do teste, basta executar pytest --cov --cov-report=term-missing --cov-report=html


### Usando o memray:

Para gerar um sumário no terminal, navegue até a pasta "Analysis" e execute memray summary memray_output.bin.

Para gerar estatístiscas de uso de memória no terminal navegue até a pasta "Analysis" e execute memray stats memray_output.bin

Para gerar um flamegraph, navegue até "Analysis" e execute: memray flamegraph memray_output.bin
