# Comparação estrutural correta — modelo Squad 3 e relatório atual Squad 6

**Uso:** material de estudo assistido por IA, sujeito à revisão por Lucas. Não é trabalho avaliado apresentado como autoria exclusiva nem validação do sistema.

## Fontes corretas

- **Modelo:** [Google Docs fornecido como documento-modelo da Squad 3](https://docs.google.com/document/d/182Jc_898nU85mBViSAnfwYo3R61YOYjU/edit). Pertence à Squad 3 e a outro projeto. Serve somente como referência estrutural.
- **Relatório-base histórico comparado:** [versão de 20 páginas fixada pelo commit 254972e](https://github.com/Lucasdoreac/squad6-labtech-documentacao/blob/254972e7d9305425c54eae74fc465052dd78a385/Relatorio-Squad-6.pdf). Não é a versão atual. Na consulta de 28/11, o [PDF publicado](https://lucasdoreac.github.io/squad6-labtech-documentacao/Relatorio-Squad-6.pdf) tinha 36 páginas, com materiais de estudo, diagramas e capturas adicionais; o link pode mudar.

## Estrutura do modelo Squad 3

Capa e identificação; critérios de evidência e sumário; síntese executiva; histórico de encontros e marcos; composição da equipe e contribuições; problema, objetivo, público, escopo incluído/excluído e arquitetura; requisitos funcionais e não funcionais; UML, casos de uso e dicionário físico de dados; backlog e testes; tutorial das telas; pré-requisitos e instruções de uso; declaração de IA; reflexão/conclusões; apêndices de evidências de encontros e rastreabilidade técnica.

## Estrutura do relatório-base histórico Squad 6 (20 páginas)

Capa, autoria/assistência e limites; modelagem UML e fontes públicas; backlog e critérios de aceite propostos; especificação funcional/técnica com requisitos, casos de uso, modelo lógico conceitual, plano de verificação e pendências; três diagramas; capturas de 26/11; complemento de apresentação e limites de revisão na p. 19; e nota técnica sobre snapshot Java histórico na p. 20. O relatório separa observação, inferência e proposta. Não houve teste autenticado, teste de backend, escrita ou criação de reserva. A nota da p. 20 não demonstra ligação ao cliente atual; nesta preparação ela é removida para evitar que modelos de código não vinculados sejam lidos como arquitetura da Squad 6. O roteiro útil da p. 19 é preservado.

## Correspondências úteis e lacunas legítimas

- A Squad 6 já cobre rastreabilidade, RF/RNF, UML, backlog, casos de uso, dados conceituais, plano de verificação e limites. Um sumário/resumo executivo e subseções explícitas de problema, escopo e fora de escopo podem melhorar navegação, desde que Lucas revise e não apresente sugestões como decisões confirmadas.
- Um tutorial deve se limitar às telas efetivamente observadas; as capturas de 28/11/2026 mostram a home pública e o formulário de e-mail institucional vazio, não login nem reserva.
- Não se deve acrescentar dicionário físico, cardinalidades ou esquema persistido sem evidência. O backend de repositório é apenas candidato: não há identidade de implantação confirmada.
- Não importar da Squad 3 nomes, papéis, reuniões, contribuições, stack, bancos/tabelas, regras, resultados de testes, prioridades ou conclusões. O documento-modelo não é aplicação nem especificação da Squad 6.
- O horário de Brasília (`America/Sao_Paulo`) é requisito expresso de Lucas para o projeto; não é prova de implementação nem conteúdo transferido do modelo.
- Os diagramas de estudo são proposta informada por leitura do cliente/frontend e do repositório candidato. O ramo de navegação descrito foi conferido no código do cliente; isso não valida backend, implantação ou comportamento real. Os diagramas não são definitivos.

## Proveniência e assistência

Esta comparação foi organizada com assistência de IA com base na estrutura informada do modelo da Squad 3, no relatório histórico de 20 páginas e nos arquivos de estudo fornecidos. O Google Doc não pôde ser lido integralmente nesta verificação; a descrição da estrutura precisa de conferência. Lucas deve verificar fontes, corrigir interpretações e decidir o que aproveitar antes de qualquer apresentação ou entrega. Nenhum dado, status, implementação ou resultado do projeto da Squad 3 foi atribuído à Squad 6.
