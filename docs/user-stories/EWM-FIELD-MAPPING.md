# Mapeamento fechado entre front matter e payload IBM Jazz / EWM

> Aviso de conectividade: neste momento, este repositorio gera apenas o payload canonico de integracao e nao realiza conexao direta com o IBM Jazz / EWM, porque o ambiente corporativo esta hospedado na intranet da CAIXA e depende de acesso de rede, autenticacao e configuracoes internas nao disponiveis neste workspace.

## Objetivo

Este documento define um mapeamento fechado entre o front matter das HUs canonicas e o payload de integracao para IBM Jazz / Engineering Workflow Management (EWM). O objetivo e eliminar inferencias soltas e garantir que a exportacao para EWM seja deterministica.

## Escopo atual

No estado atual, o projeto cobre:

- geracao local de payload estruturado para EWM;
- exportacao de HU para Markdown, PDF e DOCX;
- indexacao automatica das historias de usuario.

Nao faz parte do escopo atual:

- autenticacao contra o ambiente IBM Jazz / EWM da CAIXA;
- envio HTTP direto para endpoints corporativos;
- resolucao de URIs internas, areas administrativas e enumeracoes do servidor intranet.

## Principio de integracao

O payload gerado pelo repositorio usa dois niveis complementares:

1. `fields`: representacao fechada dos campos reais do Work Item no EWM, em nomes de negocio estaveis.
2. `oslc_cm`: projecao pronta para um adaptador REST/OSLC, usando nomes de propriedades portaveis.

Campos dependentes de URI do servidor, identificadores internos, enumeracoes configuradas ou areas administrativas permanecem no payload como valores textuais controlados. A resolucao final para URIs de servidor fica a cargo do sincronizador EWM.

## Front matter de referencia

```yaml
id: HU-PD-001
title: Consulta de Processo Digital
module: Processo Digital
status: Homologado
owner: Product Owner
repository: silic-digital-process
prototype: https://osvaldojeronymo.github.io/silic-digital-process/
version: 1.0
last_update: 2026-05-24
export_targets:
  - pdf
  - docx
  - md
  - ewm
ewm:
  work_item_type: Story
  project_area: SILIC 2.0
  team_area: Arquitetura e Produto
  category: Processo Digital
  planned_for: A definir
  iteration: A definir
  priority: Medium
  severity: Normal
  work_item_id: A definir
  parent_work_item_id: A definir
  tags:
    - silic-2.0
    - processo-digital
    - user-story
    - homologado
```

## Tabela de mapeamento fechado

| Front matter              | Campo EWM                    | Campo no payload `fields` | Campo no payload `oslc_cm`                                              | Regra                                         |
| ------------------------- | ---------------------------- | ------------------------- | ----------------------------------------------------------------------- | --------------------------------------------- |
| `id`                      | Work Item External ID        | `externalId`              | `rtc_ext:externalId`                                                    | Copia direta do identificador canonico da HU  |
| `title`                   | Summary                      | `summary`                 | `dcterms:title`                                                         | Concatenado com `id` no formato `ID - titulo` |
| `module`                  | Filed Against / Category     | `filedAgainst`            | `rtc_cm:filedAgainst`                                                   | Usa o valor textual do modulo                 |
| `status`                  | Status                       | `status`                  | `oslc_cm:status`                                                        | Valor textual normalizado                     |
| `owner`                   | Owned By                     | `ownedBy`                 | `rtc_cm:ownedBy`                                                        | Valor textual do responsavel                  |
| `repository`              | Repository Link label        | `repository`              | `rtc_ext:repository`                                                    | Nome curto do repositorio                     |
| `prototype`               | Related Link / External Link | `prototype`               | `rtc_cm:com.ibm.team.workitem.linktype.relatedartifact.relatedArtifact` | URL do prototipo                              |
| `version`                 | Document Version             | `documentVersion`         | `rtc_ext:documentVersion`                                               | Copia direta                                  |
| `last_update`             | Last Modified                | `lastUpdate`              | `dcterms:modified`                                                      | Data ISO                                      |
| `export_targets`          | Export profile               | `exportTargets`           | `rtc_ext:exportTargets`                                                 | Lista ordenada                                |
| `ewm.work_item_type`      | Work Item Type               | `workItemType`            | `rtc_cm:workItemType`                                                   | Ex.: `Story`                                  |
| `ewm.project_area`        | Project Area                 | `projectArea`             | `rtc_cm:projectArea`                                                    | Valor textual controlado                      |
| `ewm.team_area`           | Team Area                    | `teamArea`                | `rtc_cm:teamArea`                                                       | Valor textual controlado                      |
| `ewm.category`            | Category                     | `category`                | `rtc_cm:category`                                                       | Normalmente igual ao modulo                   |
| `ewm.planned_for`         | Planned For                  | `plannedFor`              | `rtc_cm:plannedFor`                                                     | Iteracao macro alvo                           |
| `ewm.iteration`           | Iteration                    | `iteration`               | `rtc_cm:iteration`                                                      | Sprint ou ciclo                               |
| `ewm.priority`            | Priority                     | `priority`                | `rtc_cm:priority`                                                       | Valor textual controlado                      |
| `ewm.severity`            | Severity                     | `severity`                | `rtc_cm:severity`                                                       | Valor textual controlado                      |
| `ewm.work_item_id`        | Work Item ID                 | `workItemId`              | `rtc_cm:identifier`                                                     | Preenchido apos sincronizacao                 |
| `ewm.parent_work_item_id` | Parent Work Item             | `parentWorkItemId`        | `rtc_cm:parent`                                                         | Preenchido quando houver vinculo              |
| `ewm.tags`                | Tags                         | `tags`                    | `rtc_cm:tags`                                                           | Lista ordenada                                |

## Campos gerados a partir do corpo Markdown

| Origem no documento         | Campo EWM           | Campo no payload `fields` | Campo no payload `oslc_cm`   | Regra                                       |
| --------------------------- | ------------------- | ------------------------- | ---------------------------- | ------------------------------------------- |
| Corpo completo da HU        | Description         | `descriptionMarkdown`     | `dcterms:description`        | Conteudo Markdown completo sem front matter |
| Conversao HTML do corpo     | Description (HTML)  | `descriptionHtml`         | `dcterms:description`        | HTML gerado para integracao REST/OSLC       |
| `## Criterios de aceitacao` | Acceptance Criteria | `acceptanceCriteria`      | `rtc_ext:acceptanceCriteria` | Lista estruturada extraida da tabela        |
| `## Regras de negocio`      | Business Rules      | `businessRules`           | `rtc_ext:businessRules`      | Lista estruturada extraida da tabela        |
| `## Rastreabilidade`        | Traceability        | `traceability`            | `rtc_ext:traceability`       | Lista chave-valor extraida da tabela        |

## Payload de integracao gerado

```json
{
  "schema": "silic.hu.ewm.payload.v1",
  "source": {
    "path": "docs/user-stories/HU-PD-001.md",
    "id": "HU-PD-001"
  },
  "fields": {
    "externalId": "HU-PD-001",
    "summary": "HU-PD-001 - Consulta de Processo Digital",
    "workItemType": "Story",
    "status": "Homologado",
    "ownedBy": "Product Owner",
    "projectArea": "SILIC 2.0",
    "teamArea": "Arquitetura e Produto",
    "filedAgainst": "Processo Digital",
    "category": "Processo Digital",
    "plannedFor": "A definir",
    "iteration": "A definir",
    "priority": "Medium",
    "severity": "Normal",
    "tags": ["silic-2.0", "processo-digital", "user-story", "homologado"]
  },
  "oslc_cm": {
    "dcterms:title": "HU-PD-001 - Consulta de Processo Digital",
    "dcterms:modified": "2026-05-24",
    "oslc_cm:status": "Homologado",
    "rtc_cm:ownedBy": "Product Owner",
    "rtc_cm:filedAgainst": "Processo Digital",
    "rtc_cm:plannedFor": "A definir",
    "rtc_cm:priority": "Medium",
    "rtc_cm:severity": "Normal"
  }
}
```

## Regras obrigatorias

- O bloco `ewm` do front matter e obrigatorio para qualquer HU que declare `ewm` em `export_targets`.
- O campo `summary` e sempre derivado de `id` + `title`.
- O campo `descriptionMarkdown` e sempre o corpo completo do documento sem o front matter.
- Os campos `workItemId` e `parentWorkItemId` podem permanecer `A definir` antes da primeira sincronizacao.
- O sincronizador nao deve sobrescrever a fonte canonica sem atualizacao versionada do Markdown.
