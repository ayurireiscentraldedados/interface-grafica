# `modelos/` — o que a equipe copia para o próprio repositório

**Copie esta pasta inteira** para a raiz do repositório da equipe, no encontro 05 (18/09), assim que
a equipe e a trilha estiverem fechadas. Não é material de leitura: é o que vocês preenchem e
entregam.

A divisão é esta:

- os **PDFs** em `extensao/` (plano de ação, rubrica, ficha de entrega, documentação, socialização,
  autoavaliação) explicam o que se espera e como aquilo é avaliado — leia antes de escrever;
- os **arquivos daqui** são os mesmos instrumentos em branco, para preencher no editor e versionar.

Preencher aqui, e não num documento solto, tem uma consequência prática: **o histórico de commits
vira prova de quando cada coisa foi escrita.** A dimensão D4 da rubrica pede exatamente isso, e é a
diferença entre um diário mantido e um diário reconstruído em novembro.

## O que é cada arquivo

| Arquivo | Como nomear a sua cópia | Quando |
| :-- | :-- | :-- |
| `plano-de-acao.md` | `plano-de-acao.md` | rascunho em 11/09, final em 02/10 |
| `diario-de-bordo.md` | `diario-de-bordo.md` | uma entrada por semana, o semestre todo |
| `evidencias.csv` | `evidencias.csv` | uma linha por evidência, no dia em que ela aparece |
| `entrega-de-marco.md` | `marco-1.md`, `marco-2.md`, `marco-3.md` | 02/10, 13/11 e 27/11 |
| `README-produto.md` | `README.md`, na raiz | desde o Marco 1, atualizado a cada marco |
| `socializacao.md` | `socializacao.md` | 04/12 |
| `autoavaliacao.md` | `autoavaliacao-<seu-primeiro-nome>.md` | 04/12, **um por integrante** |

Crie também uma pasta `evidencias/`, com data no nome de cada arquivo
(`evidencias/2026-09-24-email-coordenadora.pdf`). Evidência é subproduto de rotina, não tarefa da
última semana.

## `evidencias.csv`

Uma linha por evidência coletada. As colunas alimentam direto o indicador de **alcançabilidade**
que o professor consolida no relatório anual de extensão do curso:

```csv
data,tipo,indicador,canal,quem_de_fora,valor,descricao,arquivo
```

- `data` — AAAA-MM-DD, do dia em que a evidência apareceu, não do dia em que vocês a anotaram.
- `tipo` — `contagem` ou `qualitativa`. Os dois são exigidos pela D2; um só não fecha 2 pontos.
- `indicador` — qual indicador do Campo 7 do plano esta linha alimenta.
- `canal` — por onde veio (e-mail, oficina, formulário, registro de acessos, conversa).
- `quem_de_fora` — **o vínculo, não o nome** (veja a nota abaixo).
- `valor` — o número, quando for contagem. Vazio quando for qualitativa.
- `descricao` — uma frase. Se for retorno de alguém, a frase da pessoa, entre aspas.
- `arquivo` — caminho em `evidencias/`. Linha sem arquivo é afirmação, não evidência.

Exemplo de três linhas preenchidas:

```csv
data,tipo,indicador,canal,quem_de_fora,valor,descricao,arquivo
2026-09-24,qualitativa,retorno do publico,e-mail,coordenadora pedagogica de escola municipal,,"Disse que hoje faz isso a mao e leva uma tarde",evidencias/2026-09-24-email-coordenadora.pdf
2026-10-15,contagem,acessos ao endereco publico,registro do servidor,,37,Acessos unicos entre 02/10 e 15/10,evidencias/2026-10-15-acessos.png
2026-11-08,qualitativa,teste do estranho,conversa,tecnico de secretaria municipal,,"Travou na terceira etapa por nao saber o formato da data",evidencias/2026-11-08-teste-estranho.md
```

## Dado de terceiro: uma regra

O repositório de vocês é público, e a partir do momento em que a ação encontra o público externo
vocês passam a registrar dados de **outras pessoas** — não de colegas de turma.

Anote **vínculo e papel** (“coordenadora pedagógica da escola X”, “servidor da secretaria”), não o
nome completo. Contato pessoal (e-mail, telefone) só com autorização explícita, e mesmo assim fora
do repositório público. Isso é coerente com o que o Campo 4 do plano já obriga a declarar sobre as
fontes de dados: se vocês exigem procedência e cuidado do órgão que publica, o mesmo vale para
vocês.

Retorno recebido em conversa privada pode ser citado sem identificar quem falou. Uma frase anônima
com data e canal é evidência; um nome sem autorização é um problema.
