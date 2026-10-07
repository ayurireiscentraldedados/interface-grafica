# Como integrar este pacote ao repositório da disciplina

Este diretório foi montado para substituir os modelos em branco por uma versão de trabalho da **API Segurança Viária CE**.

## 1. Faça backup/commit do estado atual

No repositório da disciplina:

```bash
git status
git add .
git commit -m "chore: snapshot before road safety api adaptation"
```

Se não houver nada para commitar, siga normalmente.

## 2. Copie o conteúdo deste pacote para a raiz

O resultado esperado é ter na raiz:

```text
README.md
plano-de-acao.md
diario-de-bordo.md
evidencias.csv
marco-1.md
marco-2.md
marco-3.md
socializacao.md
app/
scripts/
tests/
...
```

A pasta antiga `03-modelos/` pode ser mantida como referência, mas não deve ser o local principal dos arquivos preenchidos; o modelo recebido orienta que as cópias versionadas fiquem na raiz do repositório da equipe.

## 3. Preencha imediatamente o que o pacote não pode inventar

Procure por:

```bash
grep -R "PREENCHER\|[[]PREENCHER" -n . --exclude-dir=.git
```

Prioridade:

1. matrículas;
2. URL do repositório;
3. contato institucional/durável;
4. pessoas externas reais que aceitarão testar;
5. fatos/horas do diário que tenham acontecido de verdade.

## 4. Conecte a plataforma principal

Primeiro confirme que o projeto principal tem o DuckDB Gold atualizado. Depois, neste repositório:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Exporte os marts:

```bash
python scripts/export_gold.py \
  --source ../ceara-road-safety-data-platform/data/warehouse/ceara_road_safety.duckdb
```

## 5. Rode os testes e suba a API

```bash
pytest -q
uvicorn app.main:app --reload --port 8000
```

Abra:

```text
http://localhost:8000/docs
```

Teste também:

```bash
curl 'http://localhost:8000/health'
curl 'http://localhost:8000/api/v1/municipios?ano=2025'
```

## 6. Primeiro commit recomendado

Depois de confirmar que funciona:

```bash
git add .
git commit -m "feat: adapt project into public road safety API"
git push
```

## 7. O que NÃO fazer

- não inventar evidências antigas;
- não preencher autoavaliações como se o semestre já tivesse terminado;
- não afirmar no Marco 1 que a API estava pública se não estava;
- não commitar o DuckDB real nem logs de acesso;
- não registrar nome/e-mail/telefone de testador externo no repositório público;
- não vender o pipeline preexistente como produção exclusiva da disciplina.
