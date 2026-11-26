# Especificação funcional e técnica — Reservas UDF | Squad 6

**Versão de trabalho:** 26/11/2026 · **Autor responsável pela revisão:** Lucas Dórea Cardoso, único integrante da Squad 6 conforme informação do próprio usuário. Documento de análise e proposta, não laudo de homologação. O backlog complementar está em [BACKLOG.md](BACKLOG.md).

## 1. Objetivo, contexto e fronteira

Proposta de MVP: permitir que um organizador prepare um pedido de evento com espaço e horário, envie para análise e acompanhe sua situação. A apresentação histórica descreve sistema de reservas de espaços e salas (H1); a nomenclatura e as regras atuais devem ser confirmadas. O sistema proposto não deve confundir **envio para análise** com reserva definitivamente aprovada.

**Em escopo proposto:** acesso, dados do evento, rascunho, seleção de espaço/data/horário, revisão/envio, acompanhamento, decisões e tratamento de erros. **Fora do MVP sem decisão:** sincronização Google/Outlook e comprovante PDF (citados em H1), administração de ofertas semestrais e qualquer integração não homologada. Não assumir cronograma de reuniões nem outros integrantes.

## 2. Fontes e níveis de evidência

- **S1 — observação pública:** https://labtech.dwcorp.com.br/ e https://labtech.dwcorp.com.br/organizer. Inicial observada em 26/11, com captura no caderno de apoio local, não publicado neste pacote. Nesta rodada a extração web retornou HTTP 500; navegador sem árvore acessível. Não foi executado fluxo autenticado.
- **S2 — rotas do cliente:** [manifesto](https://labtech.dwcorp.com.br/assets/manifest-9c1f6854.js) lista `organizer`, `auth/callback`, `access-denied` e, sob `event`, `type-selection`, `basic-info`, `details`, `logistics`, `schedule`, `confirm-data`, `confirmation` e `mine`. Nomes indicam desenho de navegação, não acesso ou funcionamento real.
- **S3 — cliente de API:** [client-DoLUnVFW.js](https://labtech.dwcorp.com.br/assets/client-DoLUnVFW.js) usa base `/api` e declara chamadas para `/auth/send-link`, `/auth/validate`, `/types`, `/courses`, `/events` e submissão de evento. Código público do navegador não comprova contrato do servidor nem sucesso da API.
- **S4 — dados e status:** [FormContext-KFWRUNFg.js](https://labtech.dwcorp.com.br/assets/FormContext-KFWRUNFg.js) contém dados de formulário e `localStorage`, salvamento de rascunho e constantes `draft`, `waiting`, `approved_by_coordenacao`, `rejected_by_coordenacao`, `approved_by_reitoria`, `rejected_by_reitoria`, `requested_change`, `direct_approval`. Constantes não provam transições reais.
- **S5 — módulos de frontend:** [tipo](https://labtech.dwcorp.com.br/assets/event-type-selection-DKXtS1Ca.js), [logística](https://labtech.dwcorp.com.br/assets/event-logistics-DSgigHJb.js), [revisão](https://labtech.dwcorp.com.br/assets/event-confirm-data-WrwFW2h9.js), [confirmação](https://labtech.dwcorp.com.br/assets/event-confirmation-CbaE9ZYO.js), [meus eventos](https://labtech.dwcorp.com.br/assets/my-events-n-fQ7PlT.js). Incluem textos, campos e validações de cliente; não são prova de execução em produção.
- **H1 — histórica:** apresentação de 26/09/2026, [arquivo no commit histórico 6e8258bf459d0f564ad626e5bc65ce6246d7010a](https://github.com/Lucasdoreac/labtech-reservas/blob/6e8258bf459d0f564ad626e5bc65ce6246d7010a/docs/apresentacao-reservas-udf-2026-09-26.pdf). Arquitetura, testes, servidores e contagens narrados ali não são evidência do ambiente atual.
- **H2 — apoio:** caderno de apoio local, pp. 4–13, não publicado neste pacote, cujos requisitos e diagramas são preliminares. O usuário esclareceu posteriormente que é o único integrante da Squad 6.

**Observado** = página/asset acessível ou texto presente. **Design proposto** = regra a definir e validar, mesmo quando inspirada em fonte. **Implantação verificada** = apenas o que foi efetivamente exercitado e registrado. Não há evidência nesta investigação de autenticação, persistência, transações, controle de acesso, aprovação ou prevenção de conflitos funcionando em produção; tampouco foram rodados testes de sistema. Assets públicos podem mudar e não identificam versão do backend.

## 3. Atores e premissas

- **Organizador:** pessoa que prepara e acompanha pedido; papel indicado por S1/S5.
- **Coordenação e reitoria/administração:** atores de análise descritos historicamente em H1; permissões, ordem e interfaces atuais não verificadas.
- **Serviço de autenticação, catálogo e API:** dependências técnicas inferidas das chamadas do cliente S3, não disponibilidade comprovada.
- **Premissas propostas:** acesso autenticado aos dados protegidos; credenciais e ambiente de teste autorizados; todos os horários do projeto apresentados em **America/Sao_Paulo**, por preferência informada pelo usuário, sujeito à validação institucional.

## 4. Requisitos e rastreabilidade

| ID | Requisito de design proposto | Aceite verificável resumido | Backlog | Base / situação |
|---|---|---|---|---|
| RF01 | Solicitar acesso e validar sessão | Link válido permite acesso; inválido/expirado não permite; erros distinguíveis | B01 | S3; execução não verificada |
| RF02 | Selecionar tipo e informar dados do evento | Sem tipo não avança; dados obrigatórios apontados sem perda dos demais | B02–B03 | S2, S4, S5; FE, não verificado |
| RF03 | Salvar e recuperar próprio rascunho | Salvamento confirmado por resposta positiva; recuperação não cruza usuários | B04, B09 | S3–S4; persistência não comprovada |
| RF04 | Consultar e selecionar sala e horário | Intervalo disponível é selecionável; conflito não pode ser confirmado | B05 | S2–S3; conflito H1 histórico, não verificado |
| RF05 | Revisar e enviar pedido para análise | Resumo editável; dados válidos; confirmação só após resposta positiva | B06 | S5; envio não verificado |
| RF06 | Acompanhar pedidos e status próprios | Lista e status legíveis; vazio e erro distintos | B07 | S3–S5; não verificado |
| RF07 | Registrar análise e decisão autorizada | Somente perfil autorizado delibera, com autor e data; transições validadas | B08–B09 | H1 histórico e S4; implementação não verificada |
| RNF01 | Controle de acesso no servidor | Dois usuários de teste: A não consegue ler/modificar recurso de B por ID | B09 | proposta baseada em S3–S4; não testado |
| RNF02 | Horário inequívoco e conflito | Seleção e resumo usam Brasília; tentativas simultâneas de mesmo intervalo/sala resultam em no máximo uma confirmação | B05 | preferência do usuário; regra proposta; não testada |
| RNF03 | Tratamento de falhas e rastreabilidade | Em indisponibilidade não mostrar sucesso; registrar resultado, ambiente, data e versão de cada verificação | B10–B11 | proposta baseada em S3/S5 e H2; não testada |
| RNF04 | Minimização de exposição | Não incluir token ou dados pessoais desnecessários em logs/capturas; documentar retenção e limpeza | B09–B11 | proposta a validar; S3–S4 |

