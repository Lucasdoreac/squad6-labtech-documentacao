#!/usr/bin/env python3
"""Gera o relatório acadêmico a partir dos Markdown e diagramas da entrega."""
from pathlib import Path
import re, html
from reportlab import rl_config
rl_config.useA85 = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfdoc
# Fontes TrueType criam streams Flate explícitos sem ASCII85; adicioná-lo
# antes da serialização faz ReportLab calcular comprimentos e xref corretos.
_original_stream_format = pdfdoc.PDFStream.format
def _ascii_stream_format(self, document):
    if self.filters is not None and 'Filter' not in self.dictionary.dict:
        filters = list(self.filters)
        if not any(getattr(f, 'pdfname', '') == 'ASCII85Decode' for f in filters):
            self.filters = [pdfdoc.PDFBase85Encode] + filters
    return _original_stream_format(self, document)
pdfdoc.PDFStream.format = _ascii_stream_format
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, NextPageTemplate, Image, KeepTogether, HRFlowable)
from PIL import Image as PILImage

BASE = Path(__file__).resolve().parent
OUT = BASE / 'Relatorio-Squad-6.pdf'
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVu-Bold', italic='DejaVu', boldItalic='DejaVu-Bold')
NAVY = colors.HexColor('#16324f'); BLUE = colors.HexColor('#28618b'); GRAY = colors.HexColor('#536273')
styles = {
 'body': ParagraphStyle('body', fontName='DejaVu', fontSize=9.1, leading=13.4, textColor=colors.HexColor('#1b2834'), spaceAfter=5, splitLongWords=1),
 'bullet': ParagraphStyle('bullet', fontName='DejaVu', fontSize=9, leading=13, leftIndent=12, firstLineIndent=-9, spaceAfter=4, splitLongWords=1),
 'table': ParagraphStyle('table', fontName='DejaVu', fontSize=8.7, leading=12.7, leftIndent=8, spaceAfter=7, splitLongWords=1),
 'h1': ParagraphStyle('h1', fontName='DejaVu-Bold', fontSize=17, leading=22, textColor=NAVY, spaceBefore=3, spaceAfter=12, keepWithNext=1),
 'h2': ParagraphStyle('h2', fontName='DejaVu-Bold', fontSize=12, leading=16, textColor=BLUE, spaceBefore=11, spaceAfter=6, keepWithNext=1),
 'h3': ParagraphStyle('h3', fontName='DejaVu-Bold', fontSize=10.2, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4, keepWithNext=1),
 'caption': ParagraphStyle('caption', fontName='DejaVu', fontSize=8.4, leading=12, textColor=GRAY, spaceAfter=5, splitLongWords=1),
 'cover': ParagraphStyle('cover', fontName='DejaVu-Bold', fontSize=26, leading=33, textColor=NAVY, spaceAfter=18),
 'subtitle': ParagraphStyle('subtitle', fontName='DejaVu', fontSize=13, leading=19, textColor=BLUE, spaceAfter=14),
}

def inline(text):
    # Preserva o destino dos links no texto extraível e também como link clicável.
    parts = []
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    last = 0
    def format_plain(s):
        s = html.escape(s, quote=False)
        s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
        s = re.sub(r'`([^`]+)`', r'\1', s)
        return s
    for m in pattern.finditer(text):
        parts.append(format_plain(text[last:m.start()]))
        label, url = m.groups()
        label, url_esc = html.escape(label), html.escape(url, quote=True)
        if url.startswith(('https://','http://')):
            parts.append(f'<link href="{url_esc}" color="#28618b">{label}</link> ({html.escape(url)})')
        else:
            parts.append(f'{label} ({html.escape(url)})')
        last = m.end()
    parts.append(format_plain(text[last:]))
    return ''.join(parts)

def P(text, style='body'):
    return Paragraph(inline(text), styles[style])

def md_flowables(path):
    lines = path.read_text(encoding='utf-8').splitlines()
    result=[]; i=0
    while i < len(lines):
        line=lines[i].strip()
        if not line:
            i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i+=1
            if len(rows)>1 and all(re.fullmatch(r':?-{3,}:?', c.replace(' ','')) for c in rows[1]):
                headers=rows[0]
                for row in rows[2:]:
                    entries=[]
                    for j, cell in enumerate(row):
                        if cell:
                            label=headers[j] if j < len(headers) else f'Coluna {j+1}'
                            entries.append('**'+label+':** '+cell)
                    result.append(P('  ·  '.join(entries),'table'))
            else:
                for row in rows: result.append(P(' · '.join(row),'table'))
            continue
        m=re.match(r'^(#{1,3})\s+(.*)',line)
        if m:
            result.append(P(m.group(2), 'h'+str(len(m.group(1)))))
        elif re.match(r'^[-*]\s+',line):
            result.append(P('• '+re.sub(r'^[-*]\s+','',line),'bullet'))
        elif re.match(r'^\d+\.\s+',line):
            result.append(P(line,'bullet'))
        else:
            # Markdown contíguo é um parágrafo; quebras de linha são preservadas como espaço.
            block=[line]; i+=1
            while i<len(lines):
                nxt=lines[i].strip()
                if not nxt or re.match(r'^(#{1,3}\s|[-*]\s|\d+\.\s|\|)',nxt): break
                block.append(nxt); i+=1
            result.append(P(' '.join(block))); continue
        i+=1
    return result

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

story=[Spacer(1,48*mm), P('RELATÓRIO ACADÊMICO','subtitle'), Paragraph('Reservas UDF<br/>Squad 6', styles['cover']), HRFlowable(width='100%', color=BLUE, thickness=1), Spacer(1,9*mm), P('Modelagem UML, backlog de produto e especificação funcional e técnica','subtitle'), Spacer(1,15*mm), P('**Integrante:** Lucas Dórea Cardoso — único integrante da Squad 6.'), P('**Assistência de IA:** material elaborado com apoio de inteligência artificial; revisão e validação acadêmica cabem ao integrante.'), P('**Data da investigação:** 26/11/2026.'), Spacer(1,8*mm), P('**Limites da investigação:** análise de fontes públicas e documentação histórica. Não houve teste autenticado, teste de backend, criação de evento ou chamada de escrita à API. As regras e os fluxos propostos dependem de validação.'), PageBreak()]
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
        import subprocess
        subprocess.run(['dot', '-Tpng', str(png.with_suffix('.dot')), '-o', str(png)], check=True)
    iw,ih=PILImage.open(png).size
    w,h=wide if template=='wide' else portrait
    maxw=w-40*mm; maxh=h-84*mm
    scale=min(maxw/iw,maxh/ih)
    story.append(Image(str(BASE/'diagramas'/filename),width=iw*scale,height=ih*scale,hAlign='CENTER'))
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
