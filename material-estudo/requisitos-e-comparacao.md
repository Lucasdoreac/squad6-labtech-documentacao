# Guia de estudo — requisitos e comparação estrutural

**Projeto analisado:** Reservas UDF / LabTech — Squad 6  
**Natureza deste arquivo:** material de estudo, síntese de fontes e proposta de critérios para revisão. **Não é homologação do sistema nem texto apresentado como trabalho autoral já validado por Lucas.**  
**Revisão necessária:** Lucas deve conferir, adaptar e completar o material; regras de negócio e critérios institucionais precisam ser validados por responsáveis autorizados.

> **Atribuição de IA.** Este guia foi produzido com assistência de IA, a partir dos artefatos fornecidos, da interface pública e do repositório candidato identificado abaixo. A IA auxiliou na leitura, organização, comparação e redação. Lucas deve verificar as fontes, ajustar as propostas e decidir o que aproveitar; nada aqui deve ser assinado ou entregue como se fosse, sem revisão, trabalho próprio já avaliado. Não foram realizadas alterações em registros do sistema nem criados pedidos ou reservas. Uma tentativa de acesso recebeu resposta HTTP 400 “Invalid email”; não se confirmou a causa nem houve sessão autenticada. Este material é preliminar e foi publicado para estudo.

## 1. Leitura rápida e limites

A aplicação pública permite observar uma página inicial com acesso **ORGANIZADOR** e a rota `/organizer` com um formulário de e-mail institucional. O manifesto e bundles públicos do frontend declaram outras telas para classificar e preencher um evento, consultar sala/data/horário, enviar o pedido e acompanhar eventos. O código candidato no GitHub contém fontes de frontend e serviços de API compatíveis com parte desses fluxos.

Essas evidências **não demonstram** que autenticação, persistência, autorização, disponibilidade, envio, aprovação ou reserva funcionem no ambiente publicado. Não houve autenticação bem-sucedida, teste de backend, concorrência ou verificação de dados. A tentativa de acesso submeteu apenas o e-mail e foi rejeitada; não foram criados ou alterados registros de reservas. O commit candidato e os assets publicados são fontes distintas: a relação de implantação entre eles não foi comprovada. As frases abaixo são requisitos candidatos e critérios de verificação — não resultados de testes nem requisitos institucionais já aprovados.

**Revisão independente dos diagramas:** os casos de uso distinguem quem solicita o link de quem executaria as demais ações; sessão e autorização seguem como pré-condições não verificadas. O fluxo de atividade é apenas o ramo feliz declarado pelo cliente; o handler de submit e a reserva de três horas aparecem como código candidato, não como resposta comprovada do site. O DTO candidato `Room` contém `_id: str` e `id: int`, enquanto `Reservation.roomId` é `str`; o vínculo provável com `_id` continua hipótese, sem cardinalidades ou integridade referencial demonstradas. Nenhum ator/regra de aprovação foi inferido.

### Rótulos de evidência usados neste guia

- **[observed in UI]** — elemento visível na interface pública consultada, limitado à tela e à sessão observadas.
- **[code frontend]** — rota, campo, mensagem, validação ou chamada declarada pelo código/bundle do cliente. Não prova resposta de servidor ou sucesso operacional.
- **[candidate repository]** — estrutura/função presente no repositório candidato e commit citados. Não prova que esteja implantado ou em funcionamento.
- **[proposed/unverified]** — requisito, regra, critério ou proteção sugeridos para validação; não são fatos implementados nem decisão institucional confirmada.

Um critério verificável é um alvo para teste futuro. Nenhum critério deste documento foi executado.

## 2. Requisitos funcionais candidatos

Cada RF abaixo é uma declaração individual. “Fonte/estado” identifica por que a necessidade entrou no estudo; não equivale a aceite do requisito.

### RF01 — Abrir o acesso do organizador

- **Declaração:** A aplicação deve oferecer uma entrada para a área do organizador.
- **Fonte/estado:** **[observed in UI]** Página pública `/` exibe “ORGANIZADOR”; `/organizer` exibe o título “Organizador”, campo de e-mail institucional e botão “Próximo”. Isso comprova apenas a apresentação dessas telas.
- **Critério de verificação:** Em ambiente de teste autorizado, abrir a página inicial e seguir a entrada deve mostrar a tela de acesso; a rota direta deve conduzir à mesma tela ou a uma orientação de acesso. Registrar captura sanitizada. Não marcar o acesso como autenticado com base apenas na exibição do formulário.

### RF02 — Solicitar e validar o acesso

- **Declaração:** O organizador deve poder solicitar o meio de acesso permitido e, após validação válida, entrar somente na área autorizada.
- **Fonte/estado:** **[code frontend]** O bundle da rota de organizador referencia envio de link, estados de erro e modo de teste; o cliente declara chamadas `/auth/send-link` e `/auth/validate`. **[candidate repository]** Há código de rotas de autenticação. A resposta do servidor para uma tentativa de acesso foi HTTP 400 “Invalid email”; a interface apresentou orientação sobre domínios institucionais, mas isso não prova a política efetiva ou a inexistência de exceções. Expiração, envio real e validação do link não foram confirmados.
- **Critério de verificação:** Com conta fictícia e ambiente autorizado, testar e-mail malformado, domínio não permitido (quando a política for definida), link inválido/expirado, indisponibilidade do serviço e acesso válido. Exibir êxito apenas após resposta positiva; não expor token em tela, URL de captura ou log de teste. Validar com responsáveis a política de domínio e expiração antes de fixar valores.

### RF03 — Selecionar a classificação do evento

- **Declaração:** O organizador deve selecionar uma classificação disponível antes de prosseguir com a solicitação.
- **Fonte/estado:** **[code frontend]** O manifesto declara a rota `/event/type-selection`; o bundle cliente e o código candidato contêm seleção/validação de classificação. A lista vigente de opções e a regra de obrigatoriedade devem ser confirmadas.
- **Critério de verificação:** Com a sessão de teste, verificar que as opções vêm da fonte aprovada, que a seleção permanece ao avançar/retornar e que a tentativa de continuar sem seleção apresenta orientação clara. Confirmar o comportamento no servidor, não apenas no navegador.

### RF04 — Informar os dados do evento e da logística

- **Declaração:** O organizador deve poder informar os dados requeridos para análise e planejamento do evento.
- **Fonte/estado:** **[code frontend]** O contexto/bundles do cliente referenciam dados como nome, descrição, contato do organizador, curso, público-alvo, recursos, quantidade esperada de participantes, tipo de sala e informações condicionais de logística. Esses nomes são indícios de campos manipulados pelo frontend, não confirmação de campos obrigatórios, persistidos ou aceitos pela API. **[candidate repository]** Há telas correspondentes de informações, detalhes e logística.
- **Critério de verificação:** Para cada tipo de evento validado pelo negócio, comparar formulário e contrato vigente; testar campos obrigatórios e condicionais, mensagens de validação e preservação dos demais dados quando um campo falhar. Registrar a regra aprovada por campo. Não inventar limites, formatos, obrigatoriedade ou catálogo.

### RF05 — Salvar e retomar um rascunho próprio

- **Declaração:** O organizador deve poder salvar uma solicitação incompleta e retomá-la posteriormente, se essa capacidade for confirmada como escopo.
- **Fonte/estado:** **[code frontend]** O contexto público inclui estado de formulário e uso de `localStorage`, além de referências a rascunho. Isso não comprova persistência remota, recuperação após troca de dispositivo nem isolamento entre usuários. **[proposed/unverified]** A retomada segura é requisito candidato.
- **Critério de verificação:** Em ambiente autorizado, iniciar, salvar e recuperar um rascunho após nova sessão; a interface só deve declarar salvamento remoto depois de confirmação positiva do servidor. Testar falha/timeout e verificar que uma conta de teste não lê o rascunho de outra, inclusive por alteração de identificador. Definir previamente se rascunho local é permitido e como é limpo.

### RF06 — Consultar e selecionar sala, data e horário

- **Declaração:** O organizador deve consultar opções de sala para a data e o horário escolhidos e associar uma opção ao pedido.
- **Fonte/estado:** **[code frontend]** O cliente declara consulta de salas disponíveis e a tela de agenda contém seletor de data/período, busca por nome e seleção de sala. A chamada e os controles não comprovam disponibilidade real nem reserva. **[candidate repository]** O commit contém rotas de consulta de salas e reservas; execução/implantação não comprovadas.
- **Critério de verificação:** Em ambiente de teste, consultar uma combinação de data/horário e verificar com fonte autorizada que as opções exibidas correspondem ao resultado. Diferenciar lista vazia de falha da consulta; confirmar que seleção e resumo usam a mesma sala e intervalo. Validar com o negócio definição de “disponível”, duração, intervalos e ocupações antes dos testes.

### RF07 — Revisar e enviar o pedido para análise

- **Declaração:** Antes do envio, o organizador deve revisar os dados e, mediante confirmação, submeter o pedido para análise.
- **Fonte/estado:** **[code frontend]** O cliente declara envio por `/events/{id}/submit`; a interface de confirmação usa linguagem de pedido enviado para análise. Isso não prova que a API recebeu ou gravou o pedido, nem que houve aprovação ou reserva definitiva. **[candidate repository]** Há rota de submissão de evento no código candidato.
- **Critério de verificação:** Em ambiente autorizado, o resumo deve permitir correção; campos inválidos devem apontar o problema. Após envio, mostrar confirmação/identificador/status somente com resposta positiva. Em falha ou timeout, não afirmar sucesso e permitir recuperação sem duplicar pedido. A mensagem deve distinguir “enviado para análise” de “aprovado” ou “reserva confirmada”.

### RF08 — Consultar os próprios pedidos e suas situações

- **Declaração:** O organizador deve consultar os pedidos que tem autorização para ver e suas situações atuais.
- **Fonte/estado:** **[code frontend]** O manifesto declara `/event/mine`; o cliente declara consulta de eventos por e-mail e busca de informações de reserva. **[candidate repository]** O commit contém rotas para eventos/reservas. Não há teste autenticado ou prova de que a filtragem por titular seja aplicada no servidor.
- **Critério de verificação:** Em ambiente autorizado, comparar os pedidos retornados com contas de teste; distinguir lista vazia, erro e situação desconhecida; disponibilizar nova tentativa após erro. Confirmar que a interface não mostra como aprovada uma solicitação pendente, rejeitada ou com alteração solicitada. Não assumir nomes/transições de status apenas por constantes no cliente.

### RF09 — Registrar análise e decisão institucional (escopo pendente)

- **Declaração:** Se a análise administrativa fizer parte do escopo confirmado, somente um perfil autorizado deve registrar uma decisão e torná-la rastreável ao organizador.
- **Fonte/estado:** **[proposed/unverified]** O cliente contém referências a estados, e o repositório candidato inclui código associado a eventos e aprovação; a interface publicada consultada não mostrou área de análise. A narrativa histórica não confirma o fluxo atual.
- **Critério de verificação:** Antes de implementar ou aceitar, definir atores, autorização, estados e transições, decisões permitidas, possibilidade de alteração/reenvio, autor/data e efeito da decisão sobre a sala. Depois, testar cada transição em ambiente de homologação com contas autorizadas e trilha auditável. Até lá, este RF é proposta, não funcionalidade entregue.

## 3. Requisitos não funcionais candidatos

### RNF01 — Exibir e tratar horários no fuso de Brasília

- **Declaração:** Para o projeto Reservas, os horários apresentados e tratados pela jornada de reserva devem seguir o horário de Brasília (**America/Sao_Paulo**).
- **Origem/estado:** **[proposed/unverified]** Este é requisito explícito de Lucas para o projeto, não uma constatação de implementação. A referência de fuso não foi inferida do modelo da Squad 3.
- **Critério de verificação:** Em ambiente autorizado, confrontar a data/hora escolhida, resumo, pedido recebido e registro retornado para a mesma reserva fictícia; confirmar representação consistente no fuso acordado e conversão inequívoca entre cliente e servidor. Definir formato/contrato com a equipe antes de aceitar. Não afirmar que o código atual implementa Brasília sem teste e inspeção específica.

### RNF02 — Autenticação e autorização server-side

- **Declaração:** Operações protegidas devem validar identidade e permissão no servidor; ocultar uma rota na interface não é controle de acesso suficiente.
- **Origem/estado:** **[proposed/unverified]** O frontend referencia token/e-mail e rotas privadas; isso não prova autorização do backend. O domínio de e-mail e os papéis ainda precisam de decisão.
- **Critério de verificação:** Em ambiente autorizado, usar duas contas de teste e tentar leitura/alteração cruzada por rota e identificador; requisições sem sessão válida ou sem papel requerido devem ser recusadas pelo servidor sem revelar dados. Não executar contra produção.

### RNF03 — Confidencialidade e minimização de dados

- **Declaração:** Dados pessoais e credenciais usados na solicitação devem ficar limitados a pessoas e sistemas autorizados; tokens e dados pessoais desnecessários não devem aparecer em logs, capturas ou material público.
- **Origem/estado:** **[proposed/unverified]** Requisito de proteção a validar, motivado pelo formulário e pelo fluxo de acesso; política de retenção, limpeza e visibilidade não está estabelecida pelas evidências examinadas.
- **Critério de verificação:** Revisar dados coletados, permissões, armazenamento local, logs, mensagens de erro e evidências antes de homologar. Usar dados fictícios nos testes; sanitizar capturas; definir retenção e exclusão com responsáveis. Não anexar credenciais, tokens, endereços pessoais ou conteúdo de usuário a este estudo.

### RNF04 — Integridade de disponibilidade e prevenção de conflito

- **Declaração:** A decisão final sobre disponibilidade deve ser consistente no servidor, inclusive se pedidos concorrentes disputarem o mesmo recurso e intervalo.
- **Origem/estado:** **[code frontend]** O cliente contém tratamento/mensagem para conflito de envio; isso é apenas uma intenção do cliente. **[proposed/unverified]** Atomicidade e prevenção de corrida precisam de validação técnica e regra de negócio.
- **Critério de verificação:** Com ambiente e dados de teste autorizados, enviar duas solicitações concorrentes para a mesma combinação e confirmar o resultado real no servidor e na interface; no máximo uma pode ser aceita como exclusiva, se essa for a regra institucional. Definir antes se “pedido enviado”, “pedido pendente” ou “aprovação” bloqueia o horário e como intervalos sobrepostos são tratados.

### RNF05 — Erros sem falso sucesso

- **Declaração:** Falha de autenticação, catálogo, consulta ou envio deve ser distinguível de resultado vazio e nunca apresentada como sucesso.
- **Origem/estado:** **[code frontend]** Há caminhos/mensagens de erro no cliente; sua correspondência com erros reais da API não está verificada. **[proposed/unverified]** A consistência da experiência e recuperação deve ser aceita em teste.
- **Critério de verificação:** Em ambiente de teste, provocar respostas de vazio, indisponibilidade, validação, não autorizado e conflito; confirmar mensagem apropriada, possibilidade de nova tentativa e ausência de duplicidade/falso sucesso. Registrar status e resultado efetivamente observados.

### RNF06 — Usabilidade, acessibilidade e compatibilidade

- **Declaração:** A jornada deve ser utilizável por teclado e leitor de tela, apresentar rótulos/mensagens associados aos campos e manter conteúdo legível nos dispositivos e navegadores oficialmente suportados.
- **Origem/estado:** **[observed in UI]** Apenas a inicial e a tela pública de organizador foram observadas nesta consulta. **[proposed/unverified]** Acessibilidade e compatibilidade não foram testadas e a matriz suportada não foi definida.
- **Critério de verificação:** Definir a matriz com responsáveis e testar navegação por teclado, foco, rótulos, contraste, mensagens de validação e layouts nas combinações acordadas; registrar ambiente e resultado. Não afirmar responsividade ou conformidade antes dos ensaios.

### RNF07 — Meta de desempenho definida antes de medir

- **Declaração:** O responsável pelo produto deve definir metas mensuráveis de desempenho para as jornadas e dependências críticas antes de aceitar o requisito de desempenho.
- **Origem/estado:** **[proposed/unverified]** As fontes analisadas não estabelecem uma meta atual verificável; não foi importada a meta numérica do documento-modelo da Squad 3.
- **Critério de verificação:** Acordar ambiente, carga, percentis e limite aceitável antes do teste; medir leitura de disponibilidade e envio em ambiente autorizado e registrar configuração, amostra e resultado. Sem esses parâmetros acordados, não declarar “rápido” nem aprovado por SLA.

## 4. Ambiguidades que precisam de decisão

Não preencher estes pontos por suposição. Registrar decisão, responsável e fonte de validação:

1. **Nomenclatura e fronteira:** “evento”, “pedido”, “reserva” e “solicitação” significam a mesma coisa? O que é enviado para análise e em que ponto, se houver, vira reserva confirmada?
2. **Acesso:** Quais endereços/domínios são autorizados? Como funciona expiração, reenvio, revogação e recuperação do link? Qual é o ambiente de demonstração autorizado?
3. **Campos:** Quais campos são obrigatórios por classificação? Quais são condicionais? Quais formatos, limites e catálogos vigem? Evidência frontend não basta para responder.
4. **Rascunho:** Há persistência no servidor ou apenas estado/localStorage? Quanto tempo dura? Quem pode recuperar, editar ou apagar?
5. **Sala e horário:** Qual catálogo é fonte da verdade? Como são definidos duração, intervalos, recorrências, feriados, bloqueios, sobreposição e disponibilidade?
6. **Fuso e conflito:** Brasília é requisito explícito do usuário; falta confirmar contrato técnico e regra institucional de conversão, intervalos e bloqueio entre consulta e decisão.
7. **Análise:** Quem analisa? Qual ordem e quais transições são válidas? Há aprovação direta, rejeição, pedido de alteração ou cancelamento? O que altera a disponibilidade?
8. **Dados e privacidade:** Quais dados precisam ser coletados, por quanto tempo, quem pode acessá-los e como solicitar exclusão? O que pode ser exibido a outros atores?
9. **Aceite e implantação:** Qual versão/ambiente é alvo de homologação? Quem autoriza testes? O commit candidato não foi vinculado tecnicamente à publicação observada.
10. **Qualidade:** Quais navegadores/dispositivos são suportados? Quais limites de desempenho e disponibilidade são necessários? Nenhum valor foi inventado neste guia.

## 5. Comparação estrutural com o documento-modelo fornecido

O documento-modelo é explicitamente da **Squad 3**, sobre outro projeto (reserva de salas/laboratórios em demonstração local). Ele serve como exemplo de organização editorial, **não** como especificação ou evidência para a Squad 6.

### Estrutura que o modelo oferece

O modelo reúne capa/identificação, critérios de evidência e síntese executiva; histórico de encontros e equipe; problema, objetivo, escopo e arquitetura; RF/RNF; UML e dicionário de dados físico; backlog e critérios de aceite; tutorial de telas e pré-requisitos; declaração de IA; reflexão; apêndices de encontros e rastreabilidade técnica.

### O que os artefatos disponíveis da Squad 6 já cobrem

O PDF atual da Squad 6 localizado no repositório público contém 14 páginas. Já apresenta limites epistemológicos claros, três diagramas UML, fontes para o frontend público, backlog com critérios propostos, RF/RNF, casos de uso, modelo de dados conceitual, plano de verificação e decisões pendentes. Diferencia observação, inferência e proposta, e não afirma que uma operação pública teve sucesso.

### Adaptação recomendada — sem transplantar fatos

- **Preservar a cautela de evidência da Squad 6.** Manter separado: tela observada, indício de código do frontend, fonte do repositório candidato, narrativa histórica e proposta. Código presente não é teste, implantação ou aceite.
- **Acrescentar navegação e resumo executivo curtos**, se útil: objetivo, fronteira, evidências disponíveis, o que não foi testado e decisões bloqueadoras.
- **Organizar escopo em subseções explícitas:** problema/objetivo e público pretendido só como proposta quando não confirmados; em escopo, fora de escopo e pressupostos com fonte/status.
- **Usar a lista RF/RNF deste estudo como material de revisão**, vinculando cada requisito a fonte, critério e situação. Confirmar prioridades e regras com responsáveis; não importar prioridade da Squad 3.
- **Manter modelo de dados conceitual.** Não declarar tabela, tipo físico, cardinalidade, chave ou persistência sem inspeção e confirmação do esquema efetivamente implantado.
- **Adicionar tutorial apenas para fluxo seguro e reproduzível.** Capturas devem ser reais, datadas e sanitizadas; marcar como pendente o que não foi percorrido. Não fornecer comandos de inicialização como se o ambiente público tivesse sido reproduzido.
- **Histórico, equipe, autoria, reuniões e contribuições:** incluir somente com fonte e confirmação própria. O modelo da Squad 3 não pode preencher campos da Squad 6.
- **Apêndice de rastreabilidade:** relacionar URL/commit/arquivo e data da consulta; manter assets públicos como evidência mutável, sem tratá-los como contrato estável.

### Fatos do modelo que não podem ser transferidos à Squad 6

Não reutilizar pessoas, matrículas, professora/coordenadora, datas, reuniões, contribuições, semestre, stack, banco, tabelas, código demo, telas, regras de turno, reservas automáticas, métricas, número de testes, status, prioridades, backlog, PRs/issues, aprovação ou conclusão do exemplo. Nem mesmo valores apresentados como critérios no modelo servem como valores da Squad 6 sem validação independente. Em particular, não afirmar que este sistema tem o backend, persistência, testes ou homologação que o projeto da Squad 3 descreve.

## 6. Fontes e rastreabilidade

### Interface publicada e bundles do frontend

Consulta pública sem autenticação registrada anteriormente: a inicial e `/organizer` foram abertas/inspecionadas. Nesta auditoria independente (2026-11-28), a página retornou HTTP 500 no fetch ao vivo e uma página vazia no navegador; os bundles citados também retornaram HTTP 500. Portanto, os achados atuais do cliente são revalidação bloqueada, não confirmação de disponibilidade presente. Essa auditoria não enviou formulário; em tentativa posterior, um endereço foi rejeitado antes de qualquer autenticação ou operação sobre reservas.

- [Página inicial — Reservas UDF](https://labtech.dwcorp.com.br/)
- [Rota Organizador](https://labtech.dwcorp.com.br/organizer)
- [Manifesto público de rotas](https://labtech.dwcorp.com.br/assets/manifest-9c1f6854.js) — registra os módulos públicos de inicial, organizador, callback, fluxo de evento e meus eventos.
- [Módulo inicial](https://labtech.dwcorp.com.br/assets/home-BLMlH2t-.js) e [módulo Organizador](https://labtech.dwcorp.com.br/assets/organizer-CAguo40Y.js)
- [Contexto do formulário](https://labtech.dwcorp.com.br/assets/FormContext-KFWRUNFg.js) e [cliente HTTP](https://labtech.dwcorp.com.br/assets/client-DoLUnVFW.js)
- [Módulo de seleção de tipo](https://labtech.dwcorp.com.br/assets/event-type-selection-DKXtS1Ca.js), [agenda/salas](https://labtech.dwcorp.com.br/assets/event-schedule-CkH4420g.js), [revisão/envio](https://labtech.dwcorp.com.br/assets/event-confirm-data-WrwFW2h9.js), [confirmação](https://labtech.dwcorp.com.br/assets/event-confirmation-CbaE9ZYO.js) e [meus eventos](https://labtech.dwcorp.com.br/assets/my-events-n-fQ7PlT.js).

### Repositório candidato

O clone de leitura foi conferido em `6e8258bf459d0f564ad626e5bc65ce6246d7010a`, que corresponde ao `HEAD` público verificado. Isso identifica a revisão analisada; não prova que seja a versão em produção. Não foi alterado o repositório do usuário.

- [Repositório `Lucasdoreac/labtech-reservas`](https://github.com/Lucasdoreac/labtech-reservas/tree/6e8258bf459d0f564ad626e5bc65ce6246d7010a)
- [README do commit candidato](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/README.md) — descrição declarativa do projeto; não tratada como teste.
- [Frontend: rotas](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/web/src/App.jsx), [tela de agenda](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/web/src/pages/event-schedule/EventSchedule.jsx), [acesso do organizador](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/web/src/pages/organizer/Organizer.jsx), [meus eventos](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/web/src/pages/meus-eventos/MyEvents.jsx) e [cliente HTTP](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/web/src/services/client.js).
- [API de eventos](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/api/src/SLL/events_routes.py), [rotas de reserva](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/api/src/SLL/reservation_routes.py) e [autenticação da API](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/api/src/SLL/auth_routes.py). Inspecionar código não substitui teste da instância publicada.

### Materiais de comparação fornecidos

- `analysis_artifacts/model.txt` — extração do modelo DOCX fornecido, incluindo tabelas; fonte restrita ao exemplo Squad 3.
- `analysis_artifacts/comparison.md` — comparação estrutural e notas sobre o PDF da Squad 6.
- [PDF da Squad 6 no repositório de documentação](https://raw.githubusercontent.com/Lucasdoreac/squad6-labtech-documentacao/main/Relatorio-Squad-6.pdf) — arquivo comparado, reportado com 14 páginas. A URL GitHub Pages mencionada nas notas de comparação não foi usada como fonte do PDF, pois havia sido registrada como indisponível.

## 7. Próximo passo de revisão

Lucas pode revisar cada linha e marcar: **confirmado como necessidade**, **ajustar**, **descartar** ou **aguardar responsável**. Antes de declarar qualquer requisito “implementado” ou “aceito”, anexar evidência datada de teste autorizado, versão/ambiente, passos e resultado; manter requisitos propostos e questões abertas identificáveis. Este arquivo não publica, altera nem homologa o produto.
