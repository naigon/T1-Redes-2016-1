* O trabalho foi desenvolvido em python versao 3.4
* A versão do node utilizada foi a 4.4.3
* O servidor executa a aplicação escrita em javascript com o seguinte comando:
	node exemplo.js
* Medidas de segurança adicionadas:
	- SSL com verificação de certificados¹
	- Limite de tempo para execução da aplicação do cliente (10 segundos)
	- Limite de memória utilizada por cada cliente na execução da aplicação (512MB)

¹ Os certificados(auto assinados) e chaves usadas no programa foram geradas usando a ferramenta OpenSSL 
