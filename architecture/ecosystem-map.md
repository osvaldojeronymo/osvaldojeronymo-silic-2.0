# Mapa do Ecossistema

## Objetivo

Responder quais são os módulos do ecossistema SILIC 2.0, quais responsabilidades cada um assume e como eles se relacionam no fluxo macro do módulo de imóveis de uso da CAIXA.

## Visão Estrutural

O ecossistema hoje se comporta, no código disponível, mais como uma constelação de aplicações web conectadas por navegação entre URLs do que como um conjunto de módulos já integrados por APIs entre si. O portal centraliza o acesso e vários módulos satélite implementam retorno ao portal, persistência local e protótipos de funcionalidade especializada.

## Critério de Confiabilidade

- `Evidência`: existe prova direta no código-fonte do repositório.
- `Hipótese`: o nome do repositório, o README ou a intenção documental sugerem a relação, mas o código ainda não a comprova.
- `Divergência`: nome do repositório, README e implementação não estão alinhados entre si.

## Módulos do Ecossistema

| Módulo | Repositório | Situação atual no código | Confiabilidade |
| --- | --- | --- | --- |
| Portal Principal | `silic-portal-imoveis` | Central de navegação com links explícitos para gestão, solicitações, hands-on e ações rápidas. | Evidência |
| Gestão de Imóveis SAP (protótipo legado) | `silic-request-service` | O código, o `package.json`, o README e os scripts internos descrevem um protótipo de gestão de imóveis e locadores com carga SAP, não um módulo de solicitações. | Evidência |
| Gestão e Perfis Operacionais | `silic-input-doc` | Aplicação mais rica do ecossistema atual, com rotas internas de perfis, fila formal, busca de contratos, persistência local e API local opcional. | Evidência |
| Tratamento Operacional | `silic-hands-on` | Dashboard operacional estático com dados simulados e retorno ao portal. | Evidência |
| Processo Digital | `silic-digital-process` | Protótipo estático com tabela local e retorno ao portal. | Evidência |
| Assinador Digital | `silic-digital-signer` | Protótipo de assinatura com retorno ao portal e endpoint futuro de API ainda não integrado. | Evidência |
| Motivos de Devolução | `silic-catalog-reasons` | Catálogo estático carregado de arquivos JSON e CSV locais, sem integração cruzada encontrada. | Evidência |
| Gerador de Documentos | `silic-call-for-tenders` | Aplicação React para edição e montagem de edital, com arquivos locais, drag and drop e link de retorno ao portal. | Evidência |

## Decisão de Relabel Documental

- Para documentação arquitetural baseada em código, `silic-request-service` deve deixar de ser rotulado como `Solicitação de Serviços`.
- O rótulo mais fiel ao repositório atual é `Gestão de Imóveis SAP (protótipo legado)`.
- Motivo: o repositório publica `name: show-input-doc`, `description: Sistema de Gestão de Imóveis`, homepage `show-input-doc`, carregador SAP, entidades de imóveis e locadores, além de persistência local para avaliações.

## Relações Confirmadas no Código

- Portal Principal -> Gestão de Imóveis SAP (protótipo legado): o portal abre `silic-request-service` por URL direta, mas o repositório hoje representa um protótipo legado paralelo ao papel atual de gestão.
- Portal Principal -> Gestão e Perfis Operacionais: o portal abre `silic-input-doc` por URL direta e usa âncoras como `#cadastro` e `#sipge`.
- Portal Principal -> Tratamento Operacional: o portal abre `silic-hands-on` por URL direta.
- Portal Principal -> Processo Digital: botão de ação rápida abre `silic-digital-process`.
- Portal Principal -> Motivos de Devolução: botão de ação rápida abre `silic-catalog-reasons`.
- Portal Principal -> Assinador Digital: botão de ação rápida abre `silic-digital-signer`.
- Portal Principal -> Gerador de Documentos: botão de ação rápida abre `silic-call-for-tenders`.
- Gestão de Imóveis SAP (protótipo legado) -> Portal Principal: função `voltarAoPortal()` usa `referrer`, `from=portal` e fallback por URL.
- Gestão e Perfis Operacionais -> Portal Principal: função `voltarAoPortal()` usa `referrer`, `from=portal` e fallback por URL.
- Tratamento Operacional -> Portal Principal: função `voltarAoPortal()` redireciona ao portal.
- Processo Digital -> Portal Principal: função `voltarAoPortal()` redireciona ao portal.
- Assinador Digital -> Portal Principal: script principal e arquivo `service-config.json` apontam para a URL do portal.
- Gerador de Documentos -> Portal Principal: a interface expõe link direto para o portal.

## Hipóteses Ainda Não Confirmadas

- Fluxo de `Solicitação de Serviços` como módulo distinto, já implementado em repositório específico.
- Gestão de Imóveis SAP (protótipo legado) -> Gestão e Perfis Operacionais.
- Gestão e Perfis Operacionais -> Tratamento Operacional.
- Tratamento Operacional -> Processo Digital por integração técnica real, e não apenas por navegação manual.
- Tratamento Operacional -> Assinador Digital por integração técnica real, e não apenas por navegação manual.
- Tratamento Operacional -> Motivos de Devolução por integração automática em runtime.
- Tratamento Operacional -> Gerador de Documentos por integração automática em runtime.

## Evidências Adicionais de Integração Técnica

### `silic-request-service`

- `src/utils/sapDataLoader.ts` busca JSON de dados SAP por `fetch()` e mapeia imóveis e locadores.
- `script.js` persiste avaliações por imóvel em `localStorage` usando chaves `avaliacao_imovel_*`.
- O repositório não apresentou API backend própria nem chamadas HTTP para outros módulos do ecossistema.

### `silic-input-doc`

- `api/server.js` expõe endpoints REST em SQLite e o estado de fila formal em `/api/formal-work-queue`.
- `src/main.ts` consome `GET` e `PUT` em `http://localhost:3333/api/formal-work-queue` quando roda em ambiente local.
- `src/main.ts` também suporta endpoint remoto configurável por `window.SILIC_CONTRATO_BUSCA_ENDPOINT`.
- `src/utils/sapDataLoader.ts` e `src/utils/dijurDataLoader.ts` funcionam como adapters de carga local de dados SAP e DIJUR.
- O estado compartilhado interno é fortemente apoiado em `localStorage` para filtros, favoritos, fila formal, avisos e rascunhos.

### `silic-hands-on`

- A documentação `docs/API.md` descreve `Bearer token` e `fetch()` para endpoints de dashboard.
- O runtime inspecionado em `assets/js/dashboard.js` não mostrou chamadas reais para essa API; a evidência atual continua documental, não operacional.

### `silic-digital-signer`

- `js/script.js` declara `this.apiEndpoint = '/api/v1/sign'`, mas o próprio comentário o trata como endpoint futuro.
- `js/i18n.js` persiste idioma preferido em `localStorage`.
- `service-config.json` explicita a URL de retorno ao portal.

### `silic-call-for-tenders`

- `src/form-renderer/FormRendererApp.tsx` persiste preferências de UI em `localStorage`.
- O mesmo arquivo usa `fetch(url)` para importar DOCX base do repositório.
- `src/form-renderer/schemaAdapter.ts` e o schema JSON materializam um adapter local entre campos do formulário e `tokens_docx` do documento.

## Dependências Arquiteturais

- O Portal Principal depende apenas da disponibilidade das URLs dos módulos publicados.
- Gestão de Imóveis SAP (protótipo legado) depende de arquivos SAP locais, entidades de imóveis e locadores e persistência de avaliação em `localStorage`.
- Gestão e Perfis Operacionais depende fortemente de `localStorage`, dados locais SAP e, em ambiente local, da API `http://localhost:3333/api/formal-work-queue`.
- Gestão e Perfis Operacionais também suporta endpoint remoto configurável para busca de contratos, via `window.SILIC_CONTRATO_BUSCA_ENDPOINT`.
- Tratamento Operacional, Processo Digital e Assinador Digital funcionam hoje como frontends autônomos com baixo acoplamento técnico direto.
- Motivos de Devolução depende de arquivos estáticos locais normalizados do próprio repositório.
- Gerador de Documentos depende de schema local, arquivos DOCX e estado persistido em `localStorage`.

## Matriz de Dependências entre Módulos

Na matriz abaixo, a linha representa o módulo de origem e a coluna representa o módulo do qual ele depende.

Legenda:

- `N` = navegação por URL confirmada em código.
- `V` = retorno ao portal confirmado em código.
- `H` = hipótese arquitetural ainda não comprovada por integração real.
- `-` = sem dependência direta mapeada neste nível.

| Origem \ Dependência | Portal Principal | Gestão de Imóveis SAP (protótipo legado) | Gestão e Perfis Operacionais | Tratamento Operacional | Processo Digital | Assinador Digital | Motivos de Devolução | Gerador de Documentos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Portal Principal | - | N | N | N | N | N | N | N |
| Gestão de Imóveis SAP (protótipo legado) | V | - | H | - | - | - | - | - |
| Gestão e Perfis Operacionais | V | - | - | H | - | - | - | - |
| Tratamento Operacional | V | - | - | - | H | H | H | H |
| Processo Digital | V | - | - | - | - | - | - | - |
| Assinador Digital | V | - | - | - | - | - | - | - |
| Motivos de Devolução | - | - | - | - | - | - | - | - |
| Gerador de Documentos | V | - | - | - | - | - | - | - |

## Leitura da Matriz

- A dependência mais forte confirmada em código é `Portal Principal -> demais módulos`, por navegação direta entre aplicações publicadas.
- O retorno para o portal também está implementado em vários módulos, formando uma topologia predominantemente radial.
- `silic-request-service` deixou de ser tratado aqui como módulo de solicitações e passou a ser documentado pelo papel realmente comprovado no código.
- As dependências `H` ainda representam intenção arquitetural, não integração verificada.
- A matriz representa o estado atual observado no código-fonte disponível, não o fluxo desejado de negócio.

## Como Refinar com Base no Código

Quando os repositórios dos módulos estiverem abertos no workspace, esta matriz deve ser revisada com base em evidências verificáveis, como:

- rotas que redirecionam ou apontam para outro módulo;
- chamadas HTTP, clients ou adapters entre aplicações;
- compartilhamento de modelos, estados ou catálogos;
- fluxos documentados em código, comentários, testes e arquivos de configuração;
- dependências de autenticação, autorização e observabilidade.

## Fluxo Macro

### Fluxo Atual Comprovado no Código

1. O usuário acessa o Portal Principal.
2. O portal abre outros módulos por links diretos publicados em GitHub Pages.
3. Alguns módulos satélite executam sua própria lógica local e oferecem retorno explícito ao portal.
4. Há coexistência entre um protótipo legado de gestão de imóveis em `silic-request-service` e uma aplicação mais recente de gestão e perfis operacionais em `silic-input-doc`.
5. Gestão e Perfis Operacionais concentra hoje a maior complexidade funcional observada no código, com rotas internas, persistência local, carga SAP e sincronização opcional com API local.

### Fluxo de Negócio Desejado

O fluxo desejado foi movido para um artefato separado em `architecture/fluxo-negocio-desejado.md`, para evitar mistura entre arquitetura comprovada e intenção futura.

## Observações

- Este documento representa o mapa estrutural do ecossistema.
- O código atual revela divergência entre nomes de alguns repositórios e a funcionalidade realmente implementada.
- As conexões precisam continuar sendo revisadas à medida que contratos técnicos, APIs e integrações reais forem sendo formalizados.
