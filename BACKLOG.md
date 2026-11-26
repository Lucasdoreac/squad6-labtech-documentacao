# Backlog de produto — Reservas UDF | Squad 6

**Data da investigação:** 26/11/2026. **Responsável pelo material:** Lucas Dórea Cardoso, único integrante da Squad 6 conforme informação do próprio usuário. Itens e ordem são uma proposta de trabalho individual, não relato de tarefas já realizadas. Prioridades: P0 = segurança/fluxo essencial; P1 = importante para MVP; P2 = evolução. Nenhum item está aceito ou comprovado em execução ponta a ponta.

**Estado de verificação:** FE = indício em código frontend público; HIS = demanda presente em fonte histórica; PRO = proposta de melhoria derivada das fontes. Em todos os casos, execução/backend e aceite **não verificados**. Os critérios abaixo são alvos de aceite, não resultados de teste. Dependências são sugeridas, não afirmam a ordem real da implantação.

## Fontes
- **[S1]** Página inicial https://labtech.dwcorp.com.br/ e https://labtech.dwcorp.com.br/organizer — observadas anteriormente em 26/11; a captura da inicial consta em `../caderno-squad6-revisado.pdf`, páginas finais. Disponibilidade do fluxo não demonstrada; consulta web nesta rodada retornou HTTP 500 e o navegador não expôs conteúdo acessível.
- **[S2]** Manifesto público https://labtech.dwcorp.com.br/assets/manifest-9c1f6854.js — identifica rotas e módulos no cliente; não prova execução.
- **[S3]** Cliente público https://labtech.dwcorp.com.br/assets/client-DoLUnVFW.js — declara chamadas de autenticação, tipos, cursos e eventos e base `/api`; não prova respostas da API.
- **[S4]** Contexto https://labtech.dwcorp.com.br/assets/FormContext-KFWRUNFg.js — dados de formulário, rascunho e constantes de status. Armazenamento local observado no código, não garante persistência no servidor.
- **[S5]** Módulos de tela listados no manifesto, sobretudo [tipo](https://labtech.dwcorp.com.br/assets/event-type-selection-DKXtS1Ca.js), [logística](https://labtech.dwcorp.com.br/assets/event-logistics-DSgigHJb.js), [revisão](https://labtech.dwcorp.com.br/assets/event-confirm-data-WrwFW2h9.js), [envio](https://labtech.dwcorp.com.br/assets/event-confirmation-CbaE9ZYO.js) e [meus eventos](https://labtech.dwcorp.com.br/assets/my-events-n-fQ7PlT.js).
- **[H1] Histórico, não implantação atual:** `../squad6-2026-09-26.pdf`, apresentação de 26/09/2026; cópia versionada na revisão histórica [6e8258bf459d0f564ad626e5bc65ce6246d7010a](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/docs/apresentacao-reservas-udf-2026-09-26.pdf). Suas afirmações de testes e nuvem são históricas e não foram reexecutadas aqui.
- **[H2]** `../caderno-squad6-revisado.pdf`, pp. 4–13: requisitos/modelos preliminares, revisão histórica e limites de evidência. Sua hipótese de vários integrantes foi superada pela informação do usuário.

## Itens priorizados

### B01 — Acesso do organizador
- **Valor:** acesso identificado sem compartilhar credenciais.
- **Prioridade/status:** P0 · FE / execução não verificada. **Fonte:** S1, S3.
- **Aceite:** (1) informar e-mail válido solicita link sem expor token na interface; (2) e-mail inválido recebe mensagem útil; (3) link inválido/expirado não concede acesso; (4) indisponibilidade é apresentada sem indicar sucesso. Confirmar domínios aceitos e tempo de expiração com responsáveis; H1 menciona `@udf.edu.br` apenas historicamente.
- **Dependência:** conta e ambiente de teste autorizados.

### B02 — Iniciar solicitação e classificar evento
- **Valor:** começar a solicitação coerente com o tipo do evento.
- **Prioridade/status:** P0 · FE / execução não verificada. **Fonte:** S2, S4, S5.
- **Aceite:** (1) usuário autenticado inicia solicitação; (2) classifica evento com opção disponível; (3) tentativa de avançar sem classificação mostra erro; (4) avançar preserva a seleção. Dependência: B01 e catálogo disponível.

### B03 — Informar dados e logística
- **Valor:** fornecer informação suficiente para análise e planejamento.
- **Prioridade/status:** P0 · FE / execução não verificada. **Fonte:** S2, S4, S5.
- **Aceite:** (1) coletar título, descrição, contato, curso e dados de público/recursos conforme regras validadas; (2) registrar participantes e espaço solicitado; (3) se trilha empreendedora ou projeto de extensão for marcado como sim, exigir respectiva descrição; (4) apontar campos inválidos sem apagar os demais. Dependência: B02; obrigatoriedade e limites exatos devem ser confirmados.

### B04 — Salvar e retomar rascunho
- **Valor:** evitar perda de progresso em formulários longos.
- **Prioridade/status:** P0 · FE / execução e persistência remota não verificadas. **Fonte:** S3, S4, S5.
- **Aceite:** (1) salvar gera confirmação e identificador apenas após resposta positiva; (2) retomar o próprio rascunho recupera dados salvos; (3) falha não é comunicada como sucesso e permite nova tentativa; (4) outro usuário não acessa o rascunho por troca de ID. Dependências: B01–B03; autorização server-side é requisito proposto, não verificação.

### B05 — Selecionar sala e horário
- **Valor:** escolher espaço e horário compatíveis, reduzindo conflitos.
- **Prioridade/status:** P0 · FE para tela/consultas; regra de conflito PRO/HIS; execução não verificada. **Fonte:** S2, S3, H1 pp. 6–7.
- **Aceite:** (1) consultar disponibilidade para data/hora e selecionar espaço; (2) exibir claramente dia e horário em America/Sao_Paulo; (3) intervalos sobrepostos para a mesma sala não são confirmados, inclusive em requisições simultâneas; (4) se disponibilidade mudar antes do envio, avisar e permitir nova seleção. **Fuso:** Brasília, conforme preferência informada pelo usuário; validar com o negócio. Dependência: B04 e catálogo/ambiente autorizado.

### B06 — Revisar e enviar para análise
- **Valor:** reduzir erros antes de protocolar uma solicitação.
- **Prioridade/status:** P0 · FE / envio efetivo não verificado. **Fonte:** S3, S5.
- **Aceite:** (1) exibir resumo editável com dados e horário escolhido; (2) impedir envio com dados obrigatórios ausentes e sinalizar campos; (3) só apresentar confirmação após resposta positiva e identificador; (4) erro de rede permite recuperação sem criar duplicata; (5) confirmação diz envio para análise, não reserva aprovada. Dependência: B03–B05.

### B07 — Consultar meus eventos e situação
- **Valor:** permitir acompanhamento pelo solicitante.
- **Prioridade/status:** P1 · FE / dados e autorização não verificados. **Fonte:** S3–S5.
- **Aceite:** (1) listar apenas eventos autorizados ao usuário; (2) apresentar dados e status legíveis; (3) lista vazia e erro de carregamento são distintos e erro oferece nova tentativa; (4) status desconhecido não é confundido com aprovação. Dependência: B01 e B06.

### B08 — Deliberação e rastreabilidade da análise
- **Valor:** decisão institucional rastreável e comunicada corretamente.
- **Prioridade/status:** P1 · HIS e FE de constantes / fluxo de decisão não verificado. **Fonte:** H1 pp. 7–8; S4–S5.
- **Aceite:** (1) apenas perfil autorizado decide; (2) registrar decisão, autor e data; (3) disponibilizar ao organizador situação atual; (4) tratar aprovação, rejeição e pedido de alteração sem marcar rejeição como confirmada; (5) validar com negócio ordem, transições, casos de aprovação direta e notificações antes de implementar. Dependências: B06–B07. As constantes não provam quem aprova nem que há telas de aprovação.

### B09 — Proteger dados e sessão
- **Valor:** evitar acesso indevido e exposição de dados pessoais.
- **Prioridade/status:** P0 · PRO, motivado por S3–S4 / não verificado. **Fonte:** S3, S4.
- **Aceite:** (1) API valida identidade e autorização em toda operação protegida; (2) usuário A não lê/altera dados de B mesmo conhecendo ID; (3) sessão inválida impede operações e oferece retorno seguro ao acesso; (4) definir e documentar retenção, limpeza e exposição de token e dados no navegador, avaliando riscos de armazenamento local. Dependência: B01; ensaio apenas em ambiente autorizado.

### B10 — Qualificar disponibilidade e erros
- **Valor:** evitar prometer conclusão quando uma dependência falhar.
- **Prioridade/status:** P1 · PRO / não verificado. **Fonte:** S3, S5.
- **Aceite:** (1) falhas de autenticação, catálogo, consulta e envio exibem mensagem coerente; (2) falhas não são tratadas como lista vazia ou êxito; (3) nova tentativa não duplica solicitação; (4) registrar erro técnico sem tokens ou dados pessoais desnecessários. Dependências: B01–B07.

### B11 — Homologar MVP e registrar evidências
- **Valor:** permitir entrega auditável sem alterar dados reais indevidamente.
- **Prioridade/status:** P0 · PRO / não iniciado e testes não executados. **Fonte:** H2 pp. 9–13, S1–S5.
- **Aceite:** (1) obter ambiente e identidade de teste autorizados; (2) definir matriz de testes nominal, erro, segurança e concorrência de B01–B10; (3) registrar data, versão, ambiente, passos e resultado real, com capturas sem dados sensíveis; (4) defeitos recebem evidência e item de correção; (5) nenhum item é marcado aceito só por estar em código. Dependência: autorização e ambiente adequado.

### B12 — Integração de calendários e comprovante
- **Valor:** facilitar acompanhamento externo e registro formal.
- **Prioridade/status:** P2 · HIS / implementação atual não verificada. **Fonte:** H1 pp. 8 e 11.
- **Aceite:** (1) antes de implementar, validar necessidade e autorização de calendário/comprovante; (2) definir quando gerar, dados, cancelamento e privacidade; (3) demonstrar integração e resultado apenas em ambiente de teste autorizado. Não faz parte do MVP mínimo sem decisão expressa.

## Sequenciamento prático
1. Preparar B11 (permissões, ambiente e rastreabilidade); validar critérios com o responsável pelo produto.
2. Tratar B01/B09 e B02–B06; B05 exige decisão sobre concorrência e fuso.
3. Completar B07–B10, executar a matriz B11 e registrar falhas. B12 fica fora do MVP até decisão.

**Definição de pronto proposta:** critérios aceitos por responsável autorizado, evidência datada de verificação no ambiente correto, tratamento de erro e segurança pertinente, e documentação atualizada. Não há percentual de conclusão confiável; indício em asset não equivale a item concluído.

**Uso de IA:** IA auxiliou na leitura dos artefatos públicos e documentos, organização e redação deste backlog; priorização e critérios são propostas para revisão humana. Nenhuma aprovação, execução de teste, reserva ou publicação foi feita por esta documentação.
