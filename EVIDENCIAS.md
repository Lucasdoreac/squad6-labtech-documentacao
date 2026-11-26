# Evidências da investigação

## Tela pública de organizador — 26/11/2026

A captura real da página https://labtech.dwcorp.com.br/organizer foi feita durante a investigação em 26/11/2026, antes de qualquer login. Apresenta o campo de e-mail institucional e o botão Próximo. Não demonstra autenticação, envio de link, funcionamento do backend ou criação de reserva. A imagem reproduzida no relatório foi reduzida e convertida para JPEG para armazenamento; o conteúdo visual não foi simulado.

Na tentativa posterior do mesmo dia, o endereço não respondeu dentro do tempo de conexão. Isso não prova indisponibilidade permanente. A navegação autenticada e as evidências dos encontros permanecem pendentes.

## Staging — página inicial e tela pública do organizador — 26/11/2026

Duas capturas reais foram feitas sem login e sem dados de usuário em https://reservas-staging-web.onrender.com/. A primeira mostra a página inicial e a opção Organizador; a segunda, a tela pública do organizador, com o campo de e-mail vazio e o botão Próximo. Trata-se do ambiente de **staging**, não da produção LabTech.

As imagens são os PNGs originais, armazenados sem alteração em fragmentos base64 em `evidencias/staging-home-2026-11-26.parte-*.b64` e `evidencias/staging-organizador-2026-11-26.parte-*.b64`. SHA-256, respectivamente: `17aacf01b793492ffa8f0cac5891d365d2d3b2a60a91ff1bfeb6738552d03565` e `6a191bad5d22c4236dc95e86eaa43046750d12b4b75d8d4b912c5ea1c1d3ff75`.

O login não foi comprovado: a requisição POST de login estava pendente. As capturas não demonstram autenticação, funcionamento do backend ou criação de reservas.
