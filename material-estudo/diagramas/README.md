# LabTech — material de estudo assistido

**Propósito e limite.** Estes três diagramas são um estudo/revisão assistidos por IA, não uma especificação definitiva, não uma declaração de que o candidato de código é o backend implantado e não um trabalho para apresentar como autoria própria. Este material de estudo e seus diagramas foram publicados na página do projeto e integrados ao relatório; permanecem sujeitos à revisão de Lucas e à validação técnica.

## Diagrama e leitura

- `01-casos-de-uso.svg` / `.png` / `.mmd`: capacidades declaradas pelo cliente; pessoa solicitando link separada do organizador. A sessão/autorização para as demais operações não foi verificada no deployment; sem ator aprovador ou regra de aprovação inventados.
- `02-classes-conceituais.svg` / `.png` / `.mmd`: recorte de atributos selecionados de `Event`, `Reservation`, `Room`, `Graduation` e `Type` dos DTOs do commit candidato (não exaustivo). No candidato, `Room` tem `_id: str` e `id: int`, enquanto `Reservation.roomId` é `str`; a hipótese `roomId ↔ Room._id` não está confirmada pelo contrato ou persistência, e não se presume vínculo com `Room.id`. Ligações tracejadas são referências por ID ou hipótese de mapeamento; **cardinalidades foram omitidas**, pois as fontes consultadas não demonstram multiplicidades/restrições definitivas. O formato de formulário do bundle e o modelo DTO não foram tratados como equivalentes.
- `03-atividade-categorias.svg` / `.png` / `.mmd`: ramo feliz declarado no cliente: `class`/`exam` salva rascunho e vai direto à agenda; outros tipos passam por informações básicas, detalhes e logística antes da agenda. Pré-condições, respostas de erro/conflito e tratamento de submit não foram verificados; API separada como código candidato.

Todos os desenhos incluem a marca exigida: “Material de estudo assistido por IA • sujeito à validação de Lucas e do responsável técnico”. SVG é o vetor de referência; PNG acompanha para visualização rápida. Os `.mmd` são esboços Mermaid editáveis de conteúdo, não as fontes que geram o layout detalhado SVG/PNG; diferenças de detalhe devem ser reconciliadas antes de tratar um formato como normativo.

## Evidência consultada e afirmações rastreáveis

**Cliente publicado (assets públicos; consulta anterior registrada; revalidação nesta auditoria bloqueada por HTTP 500):**

- [client-DoLUnVFW.js](https://labtech.dwcorp.com.br/assets/client-DoLUnVFW.js): cliente chama `POST /auth/send-link`, busca `/courses`, consulta `GET /events` com `userEmail`, usa `/rooms/available-rooms`, e expõe `submitEventForApproval` para `POST /events/{id}/submit`. Também expõe operações de draft por `POST /events` e `PUT /events/{id}`.
- [manifest-9c1f6854.js](https://labtech.dwcorp.com.br/assets/manifest-9c1f6854.js), [FormContext-KFWRUNFg.js](https://labtech.dwcorp.com.br/assets/FormContext-KFWRUNFg.js): rotas de seleção de tipo, informações, detalhes, logística, agenda e confirmação; contexto mantém dados de formulário/reserva localmente e consulta catálogos.
- [event-type-selection-DKXtS1Ca.js](https://labtech.dwcorp.com.br/assets/event-type-selection-DKXtS1Ca.js): ao escolher `class` ou `exam`, cliente salva draft e navega a `/event/schedule`; outros tipos vão a `/event/basic-info`. Módulos de informações/detalhes/logística protegem essas etapas para `class`/`exam` com fallback `/event/schedule`.
- [event-schedule-CkH4420g.js](https://labtech.dwcorp.com.br/assets/event-schedule-CkH4420g.js) e [event-confirm-data-WrwFW2h9.js](https://labtech.dwcorp.com.br/assets/event-confirm-data-WrwFW2h9.js): busca de salas por data/horário, escolha da sala, revisão e chamada do submit. Isso é comportamento de cliente, não prova do backend ativo.

**Fonte candidata (repositório e commit fixados; identidade do deployment não verificada):**

- [DTO/index.py](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/api/src/DTO/index.py): define DTOs `Event`, `Reservation`, `Room`, `Graduation` e `Type`; `Reservation` contém `eventId`, `roomId`, `startAt`, `endAt` e `status`.
- [SLL/events_routes.py](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/api/src/SLL/events_routes.py): candidato para `POST /events/<id>/submit`; recebe `roomId`/`reservationDate`, define status `requested`, chama reserva e desfaz reserva nova se a atualização do evento falhar.
- [BLL/index.py](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/apps/api/src/BLL/index.py): candidato usa janela de três horas para indisponibilidade e reserva; inclui salas ocupadas por aulas na consulta de disponibilidade; contém timezone fixo `UTC−03:00` nomeado `BRASILIA`.

## Decisões e perguntas para validação

1. O repositório/commit escolhido é **candidato**, não prova da implementação do site correto; confirmar com responsável técnico qual revisão de backend está implantada.
2. A regra pedida é horário de Brasília. O valor `UTC−03:00` do código candidato é apenas indício, não valida parsing, persistência, horário de verão, resposta da API ou exibição no cliente. Confirmar semântica ponta a ponta.
3. Validar se o mapeamento entre campos do formulário e DTOs é real e quais campos são persistidos como entidades/coleções.
4. Validar multiplicidades e integridade referencial entre evento, reserva, sala e curso; este material não afirma uma cardinalidade.
5. Validar política/atores/estados de aprovação com o responsável. O cliente expõe strings de status na UI, e o candidato usa `requested`; isso não basta para inferir aprovadores ou regras.

## Qualidade

SVG e PNG foram renderizados a partir do mesmo desenho; há esboço Mermaid por diagrama. Os arquivos estão publicados como material de estudo e não comprovam a implementação.