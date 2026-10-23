# Tabela de disponibilidade dos artistas

## Para que serve

Atende o requisito funcional 5 ("o perfil do artista deve exibir disponibilidade"). Antes não havia onde guardar a agenda do artista. Agora ele marca os dias em que está ocupado ou disponível. Essa informação é usada no match de compatibilidade, no aviso de conflito do painel do artista e no aceite de propostas.

## Criação (schema.sql)

```sql
CREATE TYPE status_agenda AS ENUM ('disponivel', 'ocupado');

CREATE TABLE disponibilidade (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    artista_id  UUID NOT NULL REFERENCES artistas(id) ON DELETE CASCADE,
    data        DATE NOT NULL,
    status      status_agenda NOT NULL DEFAULT 'ocupado',
    observacao  TEXT CHECK (char_length(observacao) <= 120),
    criado_em   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (artista_id, data)
);
CREATE INDEX idx_disponibilidade_data ON disponibilidade (data, status);
```

## Colunas

| Coluna | Tipo | Regra |
|---|---|---|
| id | UUID | Chave primária gerada automaticamente |
| artista_id | UUID | Artista dono da agenda. Se o artista for apagado, a agenda vai junto |
| data | DATE | Dia marcado |
| status | ocupado / disponivel | Ocupado: não recebe propostas nesse dia. Disponível: o artista quer ser contratado |
| observacao | TEXT | Até 120 caracteres (ex.: "Festival em Campinas") |
| criado_em | TIMESTAMPTZ | Quando foi marcado |

## Decisões de modelagem

- **Uma linha por artista e por dia** (`UNIQUE (artista_id, data)`): marcar de novo o mesmo dia atualiza a linha em vez de duplicar.
- **Dia sem linha = livre.** Assim o artista não precisa cadastrar o ano inteiro, só as exceções.
- **Índice por data e status:** a busca pergunta "quem está ocupado no dia X?" para todos os artistas de uma vez, e o índice deixa isso rápido.
- **Integração com contratos:** quando o cliente aceita uma proposta, a data entra automaticamente na agenda como ocupada.

## Dados de exemplo (popular_banco.py)

| Artista | Data | Status | Observação |
|---|---|---|---|
| Selva Ritmo | 21/11/2026 | ocupado | Show particular |
| Selva Ritmo | 05/12/2026 | ocupado | Festival em Campinas |
| Neon Sombra | 12/12/2026 | ocupado | Show já fechado |
| Coletivo Maré | 29/11/2026 | ocupado | Viagem |
| Coletivo Maré | 20/12/2026 | disponivel | Aceita evento de fim de ano |
