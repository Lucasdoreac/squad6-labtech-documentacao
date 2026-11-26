# Especificação funcional e técnica — continuação

## 5. Casos de uso — especificação de design, não relato de funcionamento

### UC01 — Acessar como organizador (RF01; B01)
- **Ator:** organizador. **Pré-condições:** ambiente disponível e endereço autorizado conforme regra ainda a definir.
- **Fluxo principal proposto:** (1) abrir acesso do organizador; (2) informar e-mail; (3) solicitar link; (4) receber o e-mail com o link; (5) abrir o link; (6) sistema valida a sessão e conduz à área permitida. O recebimento, a abertura do link e a validação são hipóteses de design, não resultados observados.
- **Exceções propostas:** e-mail malformado recebe mensagem; envio indisponível ou e-mail não recebido não indica acesso concluído; link inválido ou expirado não abre área protegida e oferece recomeçar. Domínio aceito e expiração pendentes de decisão.
- **Pós-condição desejada:** sessão autorizada, sem necessidade de expor token. **Base:** S1, S3; S2 declara callback. Fluxo não executado.

### UC02 — Criar e retomar rascunho (RF02–RF03; B02–B04)
- **Ator:** organizador. **Pré-condições:** sessão autorizada e acesso aos tipos de evento.
- **Fluxo principal:** (1) iniciar pedido; (2) selecionar classificação; (3) informar dados básicos, detalhes e logística; (4) salvar rascunho; (5) posteriormente selecionar o próprio rascunho e continuar.
- **Exceções:** sem classificação ou campos exigidos, informar erro; falha no salvamento preserva dados locais quando possível e não declara persistência remota; rascunho inexistente ou de terceiro é recusado.
- **Pós-condição desejada:** rascunho associado ao organizador, recuperável após confirmação de persistência. Dados apenas locais não satisfazem esse aceite. **Base:** S2, S4, S5; teste pendente.

### UC03 — Escolher data, horário e sala (RF04, RNF02; B05)
- **Ator:** organizador. **Pré-condições:** sessão válida, pedido em edição e catálogo disponível.
- **Fluxo principal:** (1) informar data e horário em Brasília; (2) consultar opções de espaço; (3) escolher sala e intervalo; (4) visualizar escolha no resumo.
- **Exceções:** nenhuma opção disponível ou erro de consulta gera mensagem distinta; horário inválido é recusado; conflito ou mudança entre consulta e confirmação exige nova escolha. Requisições concorrentes devem ser validadas atomicamente no servidor.
- **Pós-condição desejada:** seleção associada ao pedido; sem presumir reserva definitiva antes de decisão. **Base:** S2–S3, H1 histórica; regra de atomicidade e fuso são propostas.

### UC04 — Revisar e enviar para análise (RF05; B06)
- **Ator:** organizador. **Pré-condições:** sessão válida, rascunho identificável, dados obrigatórios e horário escolhidos.
- **Fluxo principal:** (1) conferir resumo do evento; (2) corrigir dados se necessário; (3) confirmar envio; (4) sistema valida e envia; (5) após resposta positiva exibe confirmação com identificador e estado de análise.
- **Exceções:** dados faltantes levam ao campo relevante; falha ou timeout não gera confirmação fictícia; repetição deve evitar duplicata; conflito de horário permite alterar seleção.
- **Pós-condição desejada:** pedido enviado para análise com identificador rastreável, não necessariamente aprovado. **Base:** S3 e S5; não executado.

### UC05 — Consultar meus eventos (RF06; B07)
- **Ator:** organizador. **Pré-condições:** sessão válida.
- **Fluxo principal:** (1) abrir meus eventos; (2) consultar lista; (3) examinar dados, horário e situação de item próprio.
- **Exceções:** nenhum registro apresenta lista vazia; falha de rede é erro com opção de tentar novamente; item não autorizado é recusado; status desconhecido permanece explicitamente desconhecido.
- **Pós-condição desejada:** consulta sem alterar a situação nem expor dados de terceiros. **Base:** S3–S5; não executado.

### UC06 — Analisar pedido (RF07; B08–B09)
- **Ator:** coordenação ou reitoria/administração, conforme autorização institucional a definir. **Pré-condições:** sessão com perfil autorizado e pedido elegível à análise.
- **Fluxo principal proposto:** (1) localizar pedido; (2) examinar dados e disponibilidade; (3) aprovar, rejeitar ou solicitar alteração conforme política; (4) registrar decisão, ator e data; (5) disponibilizar situação atual ao organizador.
- **Exceções:** ator não autorizado é recusado; pedido já decidido ou situação incompatível não sofre transição indevida; indisponibilidade preserva estado anterior.
- **Pós-condição desejada:** decisão rastreável; aprovação final só após critérios institucionais. **Base:** H1 pp. 7–8 (histórica), S4 (constantes). Sequência coordenação→reitoria e aprovação direta precisam ser definidas; não há prova de tela ou processamento efetivos.

## 6. Dados e regras conceituais

Este é um **modelo lógico proposto**, não esquema real de banco. Campos e tipos devem ser acordados; não inferir tamanho ou chave física.

| Entidade | Campos conceituais | Regras propostas |
|---|---|---|
| Organizador | identificador, e-mail, contato | identificação e autorização no servidor; limitar dados expostos |
| Evento/pedido | identificador, título, classificação, descrição, curso, público, recursos, participantes, situação | tipo e obrigatórios validados; somente titular/perfil autorizado acessa |
| Reserva pretendida | evento, sala, início, fim, fuso | início anterior ao fim; intervalo inequívoco; conflito validado no servidor |
| Análise | pedido, decisão, autor, data, justificativa quando exigida | transições e níveis definidos institucionalmente; registrar histórico |

S4 também menciona telefone, ODS, trilha empreendedora, projeto de extensão e alunos monitores. S5 exige descrição condicional de trilha/projeto no cliente. Não se afirma que todos sejam obrigatórios, persistidos ou aceitos pela API.

**Estados:** S4 fornece as constantes listadas em §2. Um possível caminho é rascunho → aguardando → decisão, mas a tabela de transições, reenvio, aprovação direta, ordem de instâncias, cancelamento e efeito sobre a sala estão **pendentes**. Rejeitado ou alteração solicitada nunca devem ser apresentados como aprovação. Não inferir que `waiting` bloqueia espaço.

**Fuso e concorrência:** apresentar data/hora em America/Sao_Paulo e conservar instante inequívoco no contrato proposto; documentar conversão e formatar nos resumos. Ao submeter, verificar sobreposição de intervalos da mesma sala e assegurar atomicidade no servidor; consulta inicial não garante disponibilidade posterior. Testar fronteiras, concorrência e datas com autorização, sem reservas reais.

## 7. Separação entre desenho e implantação

| Aspecto | Design a validar | Evidência de implantação |
|---|---|---|
| Interface | Etapas em S2 e campos em S4–S5 | Assets públicos acessíveis; execução autenticada não demonstrada |
| API | Validar contratos, autenticação, autorização e erros | S3 declara chamadas; servidor e dados não verificados |
| Banco e persistência | Rascunho e dados recuperáveis com controle de acesso | localStorage aparece em S4; banco, persistência remota e segurança não verificados |
| Aprovação | Decisão auditável e política institucional | Constantes no frontend e narrativa H1 histórica; fluxo atual não verificado |
| Tecnologias | Definir por revisão do projeto real implantado | React Router aparente no manifesto; arquitetura em H1 é histórica, não conclusão sobre implantação atual |
| Testes | Matriz de aceite e registros B11 | Não executados neste trabalho; alegações de H1 são históricas |

## 8. Plano de verificação proposto

Antes de qualquer ensaio obter ambiente, versão, conta e autorização. Não enviar dados reais ou criar reserva real apenas para demonstração. Para cada execução registrar identificador do critério, data/hora, ambiente, versão, dados fictícios, passos, resultado observado e evidência sanitizada.

1. **Acesso:** e-mail inválido, link inválido/expirado, falha de serviço e acesso autorizado (B01).
2. **Formulário:** tipo ausente, campos obrigatórios e condicionais, preservação de dados e rascunho (B02–B04).
3. **Salas:** disponibilidade, horários no fuso definido, sobreposição, concorrência e mudança de disponibilidade (B05).
4. **Envio:** revisão, falha/timeout, tentativa repetida, confirmação apenas mediante resposta; verificar estado real (B06).
5. **Consulta/segurança:** vazio vs erro, status desconhecido, contas A/B e tentativa de acesso por ID (B07/B09/B10).
6. **Aprovação:** papel autorizado, transições e registro de decisão, apenas após regras definidas (B08).

Esses são cenários planejados, **não resultados**. Qualquer falha gera item com evidência, e só após critérios satisfeitos pode haver aceite.

## 9. Decisões pendentes e declaração

Prioridades de decisão: (1) regras de acesso/domínio/expiração; (2) campos obrigatórios por tipo; (3) política de fuso, ocupação e concorrência; (4) atores, transições e aprovação direta; (5) efeito do envio sobre a disponibilidade; (6) ambiente e conta de teste; (7) retenção e segurança de dados; (8) necessidade de calendário e comprovante. Confirmar com responsáveis institucionais antes de afirmar implementação.

**Uso de IA:** IA auxiliou na leitura e organização das fontes, elaboração dos requisitos, cenários e redação. A revisão por Lucas e a validação acadêmica estão pendentes; quando necessário, cabe também validação pelo responsável institucional. Não se atribui aprovação nem testes a ninguém. Nenhuma alteração de produção foi realizada nesta investigação.
