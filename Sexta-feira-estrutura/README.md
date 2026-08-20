```markdown
# Sexta-feira

Assistente pessoal em Python — em evolução de chatbot local para assistente no espírito **Jarvis / Sexta-feira** (Homem de Ferro): ajuda, lembra, guia e, quando preciso, elogia ou puxa a orelha.

| | |
|---|---|
| **Versão de partida** | v01.00 (herança Dona Maria / ProjetoOmega) |
| **Meta** | v02.00 — Visão 3 utilizável no dia a dia |
| **Idioma** | Português (Brasil) |
| **Princípio** | Local primeiro · API sob interruptor · você no controle |

---

## O que é hoje (v01.00 / transição)

- Conversa em português com tolerância a digitação informal  
- Base local em SQLite  
- Contexto curto de conversa (ex.: “e o de C?”)  
- Fallback opcional com IA externa (Gemini)  
- Interface gráfica provisória e terminal  

**Ainda não é:** mentor completo, memória de vida, raciocínio por domínios, GUI de produto, web/PC, voz.

---

## Norte — Visão 3

```text
MENU / INTERRUPTORES
  API_RESPOSTAS · API_CONFERENCIA · WEB · AGENTE_PC · VOZ
        │
   PERGUNTA
        │
   INTERPRETAÇÃO (normalizar → digitação → contexto)
        │
   NÚCLEO LOCAL (conhecimento + memória + rastreio)
        │
   composição / domínios se precisar
        │
   API só se ligada e ainda faltar resposta
        │
   MENTOR / GUIA → RESPOSTA

À parte: manutenção da base (yellow/red/estável)
```

---

## Estrutura do repositório

```text
Sexta-feira/
├── core/           # cérebro (config, interpretação, domínios, API, mentor…)
├── manutencao/     # verificação e correção da base
├── ui/             # interface nova
├── dados/          # runtime (não versionar segredos/íntimo)
├── scripts/
├── testes/
├── docs/
├── legado/         # código v01 até migrar
├── iniciar.py
├── chat.py
└── README.md
```

A árvore de módulos é o mapa fixo da V3: preencher na ordem, sem criar pastas soltas.

---

## Plano de ação (ordem de programação)

| Fase | Foco |
|------|------|
| **P0** | Base herdada (feito) |
| **P1** | `config`, fachada `responder`, rastreio, aprender conservador, cascata API, interruptores |
| **P2** | Tags/tipos, flags yellow/red/estável, verificação, correção, info fixa |
| **P3** | Testes de regressão, compositor, roteador de domínios, política “não sei” |
| **P4** | UI nova (tema, shell, menu, chat, rastreio, painel) |
| **P5** | Memória pessoal, filosofia, ciência, hipóteses, projetos, educação, mentor, guia |
| **P6** | Web, agente PC, voz |
| **P7** | Paths/dados, máx. 2 sessões, protocolo SURTO |

Detalhes: `docs/PLANO_ACAO.md` e `docs/MODULOS.md`.

---

## Módulos principais (`core/`)

| Módulo | Função |
|--------|--------|
| `config` | Interruptores e paths |
| `interpretacao` | Normalizar, digitação, contexto |
| `conhecimento` | Base geral SQLite |
| `rastreio` | Como chegou na resposta |
| `nucleo_local` | Orquestra raciocínio local |
| `compositor` | Junta trechos em resposta lógica |
| `roteador_dominios` | Pessoal, filosofia, ciência, math… |
| `cascata_api` | Gemini → Groq → OpenRouter → reserva |
| `mentor` / `guia` | Tom Jarvis e próximo passo |
| `sessao` / `surto` | Limite de instâncias e incidente |

---

## Como rodar (quando o código v01 estiver na pasta)

```bash
python iniciar.py           # GUI
python iniciar.py console   # terminal
```

Chave de API (opcional): `api_key.txt` **local** — nunca no Git.

---

## Segurança

- Não versionar `api_key*.txt`, `.env`, bancos com dados pessoais  
- API de **respostas** separada da API de **conferência**  
- Dados íntimos em `dados/` (ignorados pelo Git)  
- Você autoriza memória e desliga módulos a qualquer momento  

---

## Versionamento

| Tag | Significado |
|-----|-------------|
| `v01.00` | Base legada (chat + SQLite + contexto + Gemini opcional) |
| `v01.x` | Fundação, base limpa, raciocínio local, UI nova |
| `v02.00` | Assistente com memória, guia e mentor no dia a dia |

```bash
git tag -a v01.00 -m "Sexta-feira v01.00 — estrutura V3"
git push origin v01.00
```

---

## Origem

Parte do assistente **Dona Maria** (ProjetoOmega).  
O nome **Sexta-feira** marca a mudança de objetivo: de chatbot de FAQ para assistente pessoal sob o seu controle.

---

## Frase-guia

> Local primeiro, API sob comando, memória com permissão, resposta com rastreio, tom de mentor — até a Sexta-feira guiar de verdade, não só responder.
