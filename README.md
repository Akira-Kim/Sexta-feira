# Sexta-feira

Assistente pessoal em Python — destino **Visão 3** (Jarvis / Sexta-feira):
ajuda, lembra, raciocina local, guia e, quando preciso, elogia ou puxa a orelha.

| | |
|---|---|
| **Partida** | v01.00 (herança Dona Maria) |
| **Meta** | v02.00 — Visão 3 utilizável no dia a dia |
| **Princípio** | Local primeiro · API sob interruptor · você no controle |

Esta árvore de pastas e arquivos (muitos ainda vazios) é o **mapa fixo da V3**.
Não criar módulos “soltos” fora dela até o fim do plano.

---

## Norte — Visão 3 (completa)

```text
MENU / INTERRUPTORES
  API_RESPOSTAS · API_CONFERENCIA · WEB · AGENTE_PC · VOZ
        │
   PERGUNTA / CONVERSA
        │
   PIPELINE DE INTERPRETAÇÃO
   (normalizar → digitação → contexto)
        │
   NÚCLEO LOCAL
   conhecimento + memória + BD raciocínios (rastreio)
        │
   resposta/composição suficiente?
      SIM → organizar + contextualizar + rastreio
      NÃO → ROTEADOR DE DOMÍNIOS
              pessoal · projetos · educação
              filosofia · ciência · conhecimento
              math/calc · hipóteses · outros
            → compositor de trechos + rastreio
            → se ainda faltar E API_RESPOSTAS=on → CASCATA API
            → senão → política “não sei” / ensinar
        │
   CAMADA MENTOR / GUIA  (elogio · orelha · 2 lados · próximo passo)
        │
   RESPOSTA AO USUÁRIO

TRILHO MANUTENÇÃO (à parte)
  API_CONFERENCIA → verificação → yellow/red/estável → correção

FUTURO NO MESMO ESPÍRITO
  Web · PC · Voz · máx. 2 sessões · protocolo SURTO · dados no SSD
```

---

## Árvore oficial (não fugir disto)

```text
Sexta-feira/
├── README.md
├── requirements.txt
├── .gitignore
├── iniciar.py                 # launcher GUI / console
├── chat.py                    # fachada de transição (v01 → core)
│
├── core/                      # cérebro
│   ├── config.py
│   ├── interpretacao.py
│   ├── conhecimento.py
│   ├── tipos_conhecimento.py
│   ├── rastreio.py
│   ├── aprender.py
│   ├── nucleo_local.py
│   ├── compositor.py
│   ├── roteador_dominios.py
│   ├── cascata_api.py
│   ├── memoria_pessoal.py
│   ├── filosofia.py
│   ├── ciencia.py
│   ├── hipoteses.py
│   ├── projetos.py
│   ├── educacao.py
│   ├── mentor.py
│   ├── guia.py
│   ├── politica_nao_sei.py
│   ├── ferramentas_web.py
│   ├── agente_pc.py
│   ├── voz.py
│   ├── sessao.py
│   ├── surto.py
│   └── paths_dados.py
│
├── manutencao/                # trilho de base (≠ conversa)
│   ├── flags_base.py
│   ├── checkpoint.py
│   ├── verificacao.py
│   ├── correcao.py
│   └── info_fixa.py
│
├── ui/                        # interface nova (não a GUI legada)
│   ├── tema.py
│   ├── shell.py
│   ├── menu_view.py
│   ├── chat_view.py
│   ├── rastreio_view.py
│   └── painel.py
│
├── dados/                     # runtime — segredos/íntimo FORA do Git
│   ├── bases/                 # .db (conhecimento, pessoal, filosofia…)
│   ├── historico/
│   ├── raciocinios/
│   ├── seguranca/incidentes/  # relatórios SURTO legíveis offline
│   └── backups/
│
├── scripts/
│   ├── criar_bases.py
│   ├── importar_info.py
│   └── backup_dados.py
│
├── testes/
│   ├── teste_regressao.py
│   ├── teste_banco.py
│   ├── teste_fallback.py
│   └── teste_rastreio.py
│
├── docs/
│   ├── VISAO3.md
│   ├── PLANO_ACAO.md
│   └── MODULOS.md
│
└── legado/                    # código v01 até migrar
    └── README.md
```

---

## Módulos × o que a V3 exige

### Core — entrada e conhecimento
| Arquivo | Responsabilidade V3 |
|---------|---------------------|
| `config.py` | Interruptores, paths, limiares, nomes |
| `interpretacao.py` | Normalizar, digitação, contexto |
| `conhecimento.py` | SQLite geral, match, similaridade, usos |
| `tipos_conhecimento.py` | Tags social/fato/procedimento/opiniao |
| `rastreio.py` | Origem de cada resposta |
| `aprender.py` | Gravar no BD só com critério/confirmação |

### Core — raciocínio local
| Arquivo | Responsabilidade V3 |
|---------|---------------------|
| `nucleo_local.py` | Orquestra memória + bases + raciocínios |
| `compositor.py` | Junta 2–3 trechos em resposta lógica |
| `roteador_dominios.py` | Encaminha para domínio certo |
| `politica_nao_sei.py` | Não inventar fato nem vida pessoal |

### Core — domínios / bases
| Arquivo | Base / papel |
|---------|----------------|
| `memoria_pessoal.py` | pessoal.db — vida, com permissão |
| `filosofia.py` | filosofia.db — bússola |
| `ciencia.py` | ciencia.db — fato com fonte |
| `hipoteses.py` | hipoteses.db — observação + confiança |
| `projetos.py` | projetos.db — Omega e outros |
| `educacao.py` | educacao.db — faculdade / estudo |

### Core — API e mentor
| Arquivo | Responsabilidade V3 |
|---------|---------------------|
| `cascata_api.py` | Gemini → Groq → OpenRouter → reserva |
| `mentor.py` | Elogio, orelha, dois lados, anti-bajulação |
| `guia.py` | Próximo passo, “da última vez…” |

### Core — mundo e segurança
| Arquivo | Responsabilidade V3 |
|---------|---------------------|
| `ferramentas_web.py` | Buscar/ler web (interruptor) |
| `agente_pc.py` | Lista branca PC; pasta dela bloqueada |
| `voz.py` | STT/TTS; silenciar |
| `sessao.py` | Máximo 2 instâncias |
| `surto.py` | Relatório offline + kill do núcleo |
| `paths_dados.py` | Onde vivem bases, histórico, backups |

### Manutenção
| Arquivo | Responsabilidade V3 |
|---------|---------------------|
| `flags_base.py` | yellow, red, estavel |
| `checkpoint.py` | Continuar verificação de onde parou |
| `verificacao.py` | Lotes com API_CONFERENCIA |
| `correcao.py` | Prioridade red; relatório |
| `info_fixa.py` | Marcar estável (liga na UI) |

### UI nova
| Arquivo | Responsabilidade V3 |
|---------|---------------------|
| `tema.py` | Cores, fontes, estilo produto |
| `shell.py` | Janela principal |
| `menu_view.py` | Interruptores e status |
| `chat_view.py` | Histórico e input |
| `rastreio_view.py` | “Por que essa resposta?” |
| `painel.py` | Totais, top usos, exportar |

---

## Ordem de programação (preencher o vazio, não reinventar)

```text
P1  config · interpretacao · conhecimento · rastreio · aprender · cascata_api
P2  tipos · flags · checkpoint · verificacao · correcao · info_fixa
P3  teste_regressao · nucleo_local · compositor · roteador · politica_nao_sei
P4  tema · shell · menu_view · chat_view · rastreio_view · painel
P5  memoria_pessoal · filosofia · ciencia · hipoteses · projetos · educacao
    mentor · guia
P6  ferramentas_web · agente_pc · voz
P7  paths_dados · sessao · surto · scripts/backup
```

Arquivos já existem (vazios ou legado). **Só implementar na ordem acima.**

---

## Dados runtime (V3)

| Caminho | Conteúdo |
|---------|----------|
| `dados/bases/conhecimento.db` | FAQ / fatos gerais |
| `dados/bases/pessoal.db` | Vida (não versionar conteúdo) |
| `dados/bases/filosofia.db` | Bússola |
| `dados/bases/ciencia.db` | Com fonte |
| `dados/bases/hipoteses.db` | Observações |
| `dados/bases/projetos.db` | Omega + projetos |
| `dados/bases/educacao.db` | Estudos |
| `dados/raciocinios/` | Logs de caminho / rastreio |
| `dados/historico/` | Conversas longas |
| `dados/seguranca/incidentes/` | SURTO_*.md legível offline |
| `dados/backups/` | Cópias datadas |

`.gitignore` deve ignorar `dados/**/*.db`, keys, histórico íntimo; versionar só `.gitkeep` e docs.

---

## Interruptores (config / menu)

| Flag | Efeito |
|------|--------|
| `API_RESPOSTAS` | Liga/desliga IA na conversa |
| `API_CONFERENCIA` | Liga/desliga IA na manutenção da base |
| `FERRAMENTAS_WEB` | Busca/leitura de sites |
| `AGENTE_PC` | Ações no computador |
| `VOZ` | STT/TTS |
| `AUTO_APRENDER` | Gravar no BD (preferência: conservador) |

---

## O que *não* está fora da V3

Tudo abaixo **já tem** pasta/arquivo nesta árvore:

- Interpretação na porta  
- Local antes de API  
- Composição e domínios  
- Rastreio e BD de raciocínios  
- Mentor e guia  
- Todas as bases (geral, pessoal, filosofia, ciência, hipóteses, projetos, educação)  
- Manutenção yellow/red/estável  
- UI nova completa  
- Web, PC, voz  
- Sessão (2 máquinas) e SURTO  
- Paths e backup  

Se surgir ideia nova, **encaixar** num módulo existente ou registrar em `docs/` antes de criar arquivo solto.

---

## Frase-guia

> Esta árvore é a Visão 3 em forma de pastas. Preencher até a Sexta-feira guiar de verdade — sem desviar do mapa.

---

*Estrutura congelada para o ciclo v01 → v02. Atualizar só status (vazio → implementado) nos docs.*
