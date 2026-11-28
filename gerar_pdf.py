#!/usr/bin/env python3
"""Gera o relatório acadêmico da entrega."""
from pdf_componentes import *

def page(canvas, doc):
    w,h = doc.pagesize
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#d8e1e8')); canvas.line(20*mm, 16*mm, w-20*mm, 16*mm)
    canvas.setFont('DejaVu', 8); canvas.setFillColor(GRAY)
    canvas.drawString(20*mm, 11*mm, 'Reservas UDF | Squad 6')
    canvas.drawRightString(w-20*mm, 11*mm, str(doc.page))
    canvas.restoreState()

portrait=A4; wide=landscape(A4)
doc=BaseDocTemplate(str(OUT), pagesize=portrait, pageCompression=1, title='Relatório Squad 6 — Reservas UDF', author='Lucas Dórea Cardoso', subject='Modelagem, backlog e especificação')
for name, size in [('portrait',portrait),('wide',wide)]:
    w,h=size
    frame=Frame(20*mm, 21*mm, w-40*mm, h-39*mm, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id=name)
    doc.addPageTemplates(PageTemplate(id=name, frames=[frame], pagesize=size, onPage=page))

story=[Spacer(1,48*mm), P('RELATÓRIO ACADÊMICO','subtitle'), Paragraph('Reservas UDF<br/>Squad 6', styles['cover']), HRFlowable(width='100%', color=BLUE, thickness=1), Spacer(1,9*mm), P('Modelagem UML, backlog de produto e especificação funcional e técnica','subtitle'), Spacer(1,15*mm), P('**Integrante:** Lucas Dórea Cardoso — único integrante da Squad 6.'), P('**Assistência de IA:** material elaborado com apoio de inteligência artificial; revisão por Lucas e validação acadêmica ainda pendentes.'), P('**Data da investigação:** 26/11/2026. **Preparação local desta versão:** 28/11/2026.'), Spacer(1,8*mm), P('**Limites da investigação:** análise de fontes públicas e documentação histórica. Não houve teste autenticado, teste de backend, criação de evento ou chamada de escrita à API. As regras e os fluxos propostos dependem de validação.'), PageBreak()]
# Inclui integralmente as três fontes finalizadas; cabeçalhos e itens de tabela tornam-se parágrafos.
for idx, filename in enumerate(['MODELAGEM.md','BACKLOG.md','ESPECIFICACAO.md','ESPECIFICACAO-parte-2.md']):
    if idx: story.append(PageBreak())
    story.extend(md_flowables(BASE/filename))

figures=[
 ('portrait','Diagrama 1 — Casos de uso','casos-de-uso.png','Interações do organizador identificadas no código do cliente; a figura não comprova a execução dos casos de uso.','MODELAGEM.md, seção Diagramas finais; diagramas/casos-de-uso.dot e fontes S1–S5.'),
 ('wide','Diagrama 2 — Classes de domínio','classes-dominio.png','Modelo conceitual: atributos não implicam colunas persistidas; relações tracejadas são inferências, sem cardinalidades pressupostas.','MODELAGEM.md, seção Diagramas finais; diagramas/classes-dominio.dot e fontes S3–S4.'),
 ('portrait','Diagrama 3 — Atividade','atividade.png','Síntese inferida do pedido de acesso e do fluxo de evento; não representa gravação da navegação ou verificação operacional.','MODELAGEM.md, seção Diagramas finais; diagramas/atividade.dot e fontes S2–S5.')]
for template,title,filename,legend,source in figures:
    story.extend([NextPageTemplate(template),PageBreak(),P(title,'h1'),P('**Legenda:** '+legend,'caption'),P('**Fonte:** elaboração com assistência de IA a partir de '+source,'caption'),Spacer(1,3*mm)])
    png=BASE/'diagramas'/filename
    if not png.exists():
        import shutil, subprocess
        dot_source = png.with_suffix('.dot')
        svg_source = png.with_suffix('.svg')
        if shutil.which('dot') and dot_source.exists():
            subprocess.run(['dot', '-Tpng', str(dot_source), '-o', str(png)], check=True)
        elif svg_source.exists():
            import cairosvg
            cairosvg.svg2png(url=str(svg_source), write_to=str(png))
        else:
            raise FileNotFoundError(f'Diagrama sem renderização ou fonte SVG/DOT: {png}')
    iw,ih=PILImage.open(png).size
    w,h=wide if template=='wide' else portrait
    maxw=w-40*mm; maxh=h-84*mm
    scale=min(maxw/iw,maxh/ih)
    story.append(Image(str(BASE/'diagramas'/filename),width=iw*scale,height=ih*scale,hAlign='CENTER'))

# Captura real, anterior ao login; os fragmentos base64 recompõem exatamente o JPEG documentado.
import base64, io
pieces=sorted((BASE/'evidencias').glob('organizador-2026-11-26.parte-*.b64'))
if not pieces:
    raise FileNotFoundError('Captura de evidência ausente')
image_bytes=base64.b64decode(''.join(x.read_text() for x in pieces), validate=True)
evidence_image=io.BytesIO(image_bytes)
iw,ih=PILImage.open(evidence_image).size
w,h=wide
scale=min((w-40*mm)/iw,(h-90*mm)/ih)
evidence_image.seek(0)
story.extend([NextPageTemplate('wide'),PageBreak(),P('Evidência — tela pública do organizador','h1'),P('Captura real de 26/11/2026, em https://labtech.dwcorp.com.br/organizer, antes do login. Mostra campo de e-mail e botão Próximo; não comprova autenticação ou operação do sistema.','caption'), P('Imagem reduzida e convertida para JPEG; EVIDENCIAS.md registra limites e contexto.','caption'),Spacer(1,3*mm),Image(evidence_image,width=iw*scale,height=ih*scale,hAlign='CENTER')])

# Capturas originais do ambiente de staging, sem dados de usuário.
# O SHA-256 garante que todos os fragmentos reconstituem o PNG original.
import hashlib
staging_figures = [
    ('staging-home-2026-11-26', '17aacf01b793492ffa8f0cac5891d365d2d3b2a60a91ff1bfeb6738552d03565', 'Evidência de staging — página inicial', 'Captura real de 26/11/2026 da página inicial do staging em https://reservas-staging-web.onrender.com/. A interface exibe a opção Organizador; não é a produção LabTech.'),
    ('staging-organizador-2026-11-26', '6a191bad5d22c4236dc95e86eaa43046750d12b4b75d8d4b912c5ea1c1d3ff75', 'Evidência de staging — tela pública do organizador', 'Captura real de 26/11/2026 do staging em https://reservas-staging-web.onrender.com/, antes do login: campo de e-mail vazio e botão Próximo. Não é a produção LabTech.'),
]
for prefix, expected_sha, title, caption in staging_figures:
    fragments = sorted((BASE/'evidencias').glob(prefix+'.parte-*.b64'))
    if not fragments:
        raise FileNotFoundError(f'Captura de staging ausente: {prefix}')
    content = base64.b64decode(''.join(p.read_text(encoding='ascii') for p in fragments), validate=True)
    if hashlib.sha256(content).hexdigest() != expected_sha:
        raise ValueError(f'Integridade da captura de staging inválida: {prefix}')
    image = io.BytesIO(content)
    iw, ih = PILImage.open(image).size
    scale = min((wide[0]-40*mm)/iw, (wide[1]-100*mm)/ih)
    image.seek(0)
    story.extend([NextPageTemplate('wide'), PageBreak(), P(title, 'h1'), P(caption, 'caption'), P('Sem dados de usuário. Login não comprovado; a requisição POST de login estava pendente. A captura não comprova operação autenticada, backend ou reservas.', 'caption'), Spacer(1, 3*mm), Image(image, width=iw*scale, height=ih*scale, hAlign='CENTER')])

# Complemento preserva o roteiro útil da p. 19 do relatório publicado de 20 páginas.
# A nota técnica Java da p. 20 não estabelece vínculo com a implantação e é omitida nesta preparação.
story.extend([NextPageTemplate('portrait'), PageBreak(), P('Complemento integrado — estudo e apresentação', 'h1'),
    P('Preparação local: 28/11/2026. Relatório-base histórico de referência (não este documento atual): a versão anterior de 20 páginas na branch docs/pagina-labtech-rascunho. O roteiro de apresentação e os limites de revisão foram preservados; a nota histórica Java da cópia anterior foi retirada porque não comprova relação com a aplicação atual ou com o Squad 6.', 'body'),
    P('Limites e honestidade', 'h2'),
    P('As três páginas de capturas reais já presentes no relatório-base foram preservadas; duas novas capturas reais de 28/11 estão acrescentadas adiante. Não houve teste do MVP, acesso autenticado, operação de escrita ou demonstração funcional. Lucas ainda precisa revisar o material e não se declara validação institucional. Lucas relatou chamadas com Darlas, mas não há registros preservados; não se atribuem quantidade, data, duração, pauta, conteúdo, encaminhamentos ou decisões, nem participação de Darlas em reunião do grupo.', 'body'),
    P('Roteiro de apresentação — 30 minutos', 'h2')])
for interval, focus in [
    ('00:00–02:00','Objetivo e limites: análise documental, não homologação; apresentar os rótulos de evidência.'),
    ('02:00–05:00','Objetivo proposto e percurso sugerido; envio para análise não equivale a reserva aprovada.'),
    ('05:00–09:00','Fontes e níveis de evidência; código do cliente não prova resposta ou persistência no backend.'),
    ('09:00–15:00','UML: ações/elementos observados versus relações e ordem inferidas; execução não validada.'),
    ('15:00–20:00','Requisitos e critérios de aceite como propostas, não resultados testados ou aprovados.'),
    ('20:00–24:00','Backlog e método: prioridades sugeridas, não tarefas concluídas ou cronograma acordado.'),
    ('24:00–27:00','Pendências, ausência de testes e relato sobre Darlas sem registros preservados.'),
    ('27:00–30:00','Síntese e perguntas sobre a documentação; manter explícito o que ainda não foi validado.')]:
    story.append(P(f'**{interval}** — {focus}', 'bullet'))
story.append(P('Vocabulário: OBSERVADO = consta em fonte/artefato, sem provar execução; INFERIDO = interpretação que requer confirmação; PROPOSTO = orientação para revisão, não regra institucional aprovada.', 'caption'))

# Integra os arquivos de apoio entregues, explicitando que são estudo assistido por IA.
for title, path in [
    ('Material de apoio — requisitos e comparação', BASE/'material-estudo'/'requisitos-e-comparacao.md'),
    ('Comparação estrutural — modelo Squad 3 e relatório atual Squad 6', BASE/'material-estudo'/'comparacao-modelo-squad3-vs-relatorio-atual.md'),
    ('Fontes e ressalvas dos diagramas de estudo', BASE/'material-estudo'/'diagramas'/'README.md')]:
    story.extend([NextPageTemplate('portrait'), PageBreak(), P(title, 'h1')])
    story.extend(md_flowables(path))

# Diagramas de estudo: apresentados como propostas, não arquitetura implantada.
study_figures = [
    ('portrait','Estudo — casos de uso','01-casos-de-uso.png','Capacidades visíveis no cliente; não demonstram execução. Estudo assistido por IA, sujeito à revisão de Lucas.'),
    ('wide','Estudo — classes conceituais','02-classes-conceituais.png','DTOs de repositório candidato; relações tracejadas são hipóteses, sem cardinalidades. Identidade do deployment não confirmada.'),
    ('wide','Estudo — atividade por categorias','03-atividade-categorias.png','Ramo de navegação conferido no cliente; bloco de API é candidato, não comprovação de servidor implantado.')]
for template, title, filename, caption in study_figures:
    story.extend([NextPageTemplate(template), PageBreak(), P(title, 'h1'),
        P(caption + ' Diagramas preliminares, não definitivos; não validam backend, implantação ou comportamento operacional.', 'caption')])
    png = BASE/'material-estudo'/'diagramas'/filename
    iw, ih = PILImage.open(png).size
    w, h = wide if template == 'wide' else portrait
    scale = min((w-40*mm)/iw, (h-80*mm)/ih)
    story.append(Image(str(png), width=iw*scale, height=ih*scale, hAlign='CENTER'))

# Capturas reais novas, datadas de 28/11/2026, verificadas sem dados pessoais visíveis.
new_screenshots = [
    ('app-home-2026-11-28.png', 'Captura real — home pública', 'Captura de tela real de 28/11/2026. Mostra somente a página inicial pública; não comprova autenticação, backend ou reserva.'),
    ('organizer-email-gate-2026-11-28.png', 'Captura real — acesso do organizador', 'Captura de tela real de 28/11/2026. Campo de e-mail vazio; não comprova envio de link, autenticação, backend ou reserva.')]
for filename, title, caption in new_screenshots:
    path = BASE/'material-estudo'/'evidencias'/filename
    iw, ih = PILImage.open(path).size
    scale = min((wide[0]-40*mm)/iw, (wide[1]-95*mm)/ih)
    story.extend([NextPageTemplate('wide'), PageBreak(), P(title, 'h1'), P(caption + ' Sem informação pessoal visível.', 'caption'),
        Image(str(path), width=iw*scale, height=ih*scale, hAlign='CENTER')])

doc.build(story)
# Comentário binário tradicional do cabeçalho PDF: normalização estritamente 1:1,
# sem mexer em streams nem alterar offsets de xref.
b=OUT.read_bytes(); lines=b.splitlines(keepends=True)
assert lines[0].startswith(b'%PDF-') and lines[1].startswith(b'%')
header=lines[1]
assert all(c < 128 for c in header[:1])
normalized=bytes(c if c < 128 else ord('X') for c in header)
assert len(normalized)==len(header)
b=lines[0]+normalized+b''.join(lines[2:])
if any(c>=128 for c in b):
    raise ValueError('PDF contém bytes não ASCII fora do comentário do cabeçalho; não alterado.')
OUT.write_bytes(b)
print(f'{OUT}: {len(b)} bytes, ASCII validado')
