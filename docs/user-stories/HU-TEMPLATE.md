---
id: HU-XXX-000
title: Titulo da Historia de Usuario
module: Nome do Modulo
status: Rascunho
owner: Product Owner
repository: nome-do-repositorio
prototype: https://exemplo.com/prototipo
version: 0.1
last_update: AAAA-MM-DD
export_targets:
  - pdf
  - docx
  - md
  - ewm
ewm:
  work_item_type: Story
  project_area: SILIC 2.0
  team_area: A definir
  category: Nome do Modulo
  planned_for: A definir
  iteration: A definir
  priority: Medium
  severity: Normal
  work_item_id: A definir
  parent_work_item_id: A definir
  tags:
    - silic-2.0
    - user-story
---

# HU-XXX-000 - Titulo da Historia de Usuario

## Finalidade do artefato

Este documento e a fonte canonica da historia de usuario no ecossistema SILIC 2.0. O front matter acima deve ser mantido em formato YAML valido para permitir exportacao, indexacao, dashboards, automacao documental e sincronizacao futura com IBM Jazz / EWM.

## Contexto de negocio

Descrever o problema, oportunidade ou demanda de negocio que motiva a historia.

## Objetivo

Descrever o resultado de negocio e o valor esperado com a implementacao desta HU.

## Declaracao da historia de usuario

Como [perfil], quero [capacidade], para [beneficio de negocio].

## Personas e partes interessadas

| Perfil    | Papel na jornada | Interesse principal |
| --------- | ---------------- | ------------------- |
| A definir | A definir        | A definir           |

## Descricao funcional

Descrever o comportamento funcional esperado de forma objetiva e orientada a negocio.

## Fluxo operacional principal

1. Descrever passo 1.
2. Descrever passo 2.
3. Descrever passo 3.

## Regras de negocio

| ID    | Regra     |
| ----- | --------- |
| RN-01 | A definir |

## Criterios de aceitacao

| ID    | Criterio                                   |
| ----- | ------------------------------------------ |
| CA-01 | Dado que [...], quando [...], entao [...]. |

## Status de validacao

| Item                             | Situacao  |
| -------------------------------- | --------- |
| Prototipo funcional              | A definir |
| Validacao de negocio             | A definir |
| Validacao tecnica de integracao  | A definir |
| Validacao com dados reais        | A definir |
| Sincronizacao com IBM Jazz / EWM | A definir |

## Referencias do prototipo

| Item                  | Referencia |
| --------------------- | ---------- |
| Nome do prototipo     | A definir  |
| URL validada          | A definir  |
| Natureza da evidencia | A definir  |
| Escopo atual          | A definir  |
| Observacao            | A definir  |

## Referencias de repositorio

| Item                         | Referencia                           |
| ---------------------------- | ------------------------------------ |
| Repositorio de implementacao | A definir                            |
| URL do repositorio           | A definir                            |
| Repositorio de governanca    | osvaldojeronymo-silic-2.0            |
| Caminho canonico             | docs/user-stories/NOME-DO-ARQUIVO.md |
| Relacao com o ecossistema    | A definir                            |

## Mapeamento para IBM Jazz / EWM

| Campo EWM               | Valor     |
| ----------------------- | --------- |
| Work Item Type          | Story     |
| Summary                 | A definir |
| Owned By                | A definir |
| Status                  | A definir |
| Filed Against           | A definir |
| Planned For             | A definir |
| Iteration               | A definir |
| Priority                | Medium    |
| Severity                | Normal    |
| Team Area               | A definir |
| Project Area            | SILIC 2.0 |
| Work Item ID            | A definir |
| Parent Epic             | A definir |
| Tags                    | A definir |
| External Prototype Link | A definir |
| Repository Link         | A definir |
| Canonical Source        | A definir |

## Consideracoes para integracoes futuras

| Tema                            | Placeholder |
| ------------------------------- | ----------- |
| API principal                   | A definir   |
| Workflow corporativo            | A definir   |
| Identificador BPM               | A definir   |
| Identificador de auditoria      | A definir   |
| Contrato de exportacao PDF/DOCX | A definir   |
| Identificador IBM Jazz / EWM    | A definir   |

## Ganhos habilitados pelo metadado estruturado

- automacao de exportacoes;
- indexacao de HUs;
- dashboards de acompanhamento;
- documentacao automatica;
- integracao com IA;
- sincronizacao com IBM Jazz / EWM.

## Licoes aprendidas

- Registrar aprendizados de descoberta, validacao ou implementacao.

## Rastreabilidade

| Dimensao                 | Referencia                       |
| ------------------------ | -------------------------------- |
| User Story               | A definir                        |
| Modulo                   | A definir                        |
| Prototipo funcional      | A definir                        |
| Repositorio associado    | A definir                        |
| Fonte canonica           | A definir                        |
| Template base            | docs/user-stories/HU-TEMPLATE.md |
| Epic vinculada           | A definir                        |
| Feature vinculada        | A definir                        |
| Work Item IBM Jazz / EWM | A definir                        |
| Caso de teste funcional  | A definir                        |
| Evidencia de homologacao | A definir                        |

## Governanca documental

Este documento deve permanecer como fonte canonica. O front matter deve ser mantido valido e sincronizado com o conteudo funcional da HU.
