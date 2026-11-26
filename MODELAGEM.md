# Modelagem UML — Reservas UDF / LabTech

**Integrante:** Lucas Dórea Cardoso (único integrante informado).  
**Assistência de IA:** material elaborado com apoio de inteligência artificial; revisão por Lucas e validação acadêmica ainda pendentes.  
**Referência da aplicação:** https://labtech.dwcorp.com.br/ — consulta pública em 26/11/2026, sem login nem alteração de produção.

## Escopo e limites
Modelagem conceitual da interface de organização de eventos e reserva. O código público indica telas, campos e chamadas HTTP, mas não comprova que as requisições funcionem ou como o backend, o banco e a autenticação são implementados. Não houve teste autenticado, criação de evento nem chamada de escrita à API. Relacionamentos e sequência de atividades são hipóteses explicitadas; não são especificação do banco nem prova de funcionamento. O fluxo de eventos é uma síntese das rotas e métodos, não uma gravação de navegação.

## Diagramas finais
1. [Casos de uso](diagramas/casos-de-uso.svg) ([fonte DOT](diagramas/casos-de-uso.dot)): interações do organizador com a interface; ações identificadas no código, sem afirmar sucesso.
2. [Classes / domínio](diagramas/classes-dominio.svg) ([fonte DOT](diagramas/classes-dominio.dot)): abstrações a partir de campos do formulário e do cliente HTTP. Atributos não implicam colunas persistidas. Relações tracejadas são inferências; sem cardinalidades pressupostas.
3. [Atividade](diagramas/atividade.svg) ([fonte DOT](diagramas/atividade.dot)): pedido de acesso, recebimento e abertura do link e fluxo de evento propostos; sequência é inferida, não executada. Falhas e modo de teste são caminhos possíveis, não verificação operacional.

## Evidências e rastreabilidade
- [Página inicial](https://labtech.dwcorp.com.br/) e [rota Organizador](https://labtech.dwcorp.com.br/organizer). Módulo [home](https://labtech.dwcorp.com.br/assets/home-BLMlH2t-.js) oferece ORGANIZADOR e verifica token/e-mail armazenados; [organizer](https://labtech.dwcorp.com.br/assets/organizer-CAguo40Y.js) contém formulário de e-mail institucional, pedido de link, mensagem de erro e mensagem de modo de teste.
- [Manifesto de rotas](https://labtech.dwcorp.com.br/assets/manifest-9c1f6854.js): `/organizer`, `/auth/callback`, `/event/type-selection`, `/event/basic-info`, `/event/details`, `/event/logistics`, `/event/schedule`, `/event/confirm-data`, `/event/confirmation`, `/event/mine`. São rotas declaradas, não prova de acesso ou execução.
- [Contexto do formulário](https://labtech.dwcorp.com.br/assets/FormContext-KFWRUNFg.js): referências a `name`, `description`, `organizer.phone`, `eventTypeId`, `graduationId`, `targetPublic`, `resources`, `expectedSubscribers` e `roomType`; código de rascunho. São campos trafegados/manipulados no frontend.
- [Cliente HTTP](https://labtech.dwcorp.com.br/assets/client-DoLUnVFW.js): chamadas pretendidas para `/auth/send-link`, `/auth/validate`, `/rooms/available-rooms`, `/events`, `/events/{id}/submit` e `/reservations`; token e e-mail são referenciados no cliente. Não se verificou resposta da API nem autorização.
- [Apresentação histórica de 26/09/2026](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/docs/apresentacao-reservas-udf-2026-09-26.pdf), especialmente p. 3–11: apresenta arquitetura, login, salas e aprovação. É referência histórica declarativa, não confirmação do estado atual ou do backend publicado. As afirmações nele sobre MongoDB, serviços, e-mail, aprovação e comprovantes não foram verificadas e não foram assumidas nos diagramas.

## Pontos a validar
- Autenticação, políticas de domínio e comportamento real do envio de link.
- Sequência obrigatória, possibilidade de editar rascunho e resposta ao envio; transições reais de status e atores de aprovação.
- Estrutura persistida, cardinalidades, autorização, prevenção de conflitos e integração com serviços externos.
- Correspondência entre os campos conceituais e os contratos efetivos da API.
