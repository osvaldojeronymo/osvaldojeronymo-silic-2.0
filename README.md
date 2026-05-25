# SILIC 2.0 — Centro de Documentação e Governança

Repositório central para documentação, arquitetura, pesquisa e padrões de governança do ecossistema do módulo de imóveis de uso da Caixa Econômica Federal (CAIXA) no **SILIC 2.0**.

## Visão Geral

Este módulo de imóveis do SILIC 2.0 é um ecossistema integrado concebido para organizar iniciativas de gestão, operacionais e técnicas dos serviços relacionados aos imóveis de uso da CAIXA. Este repositório é a fonte única da verdade para:

- Direcionamento arquitetural
- Governança e padrões
- Artefatos de pesquisa
- Conhecimento institucional

## Descrição do Ecossistema

O ecossistema é organizado em repositórios e módulos coordenados que evoluem sob padrões compartilhados e princípios arquiteturais comuns.

### Repositórios

#### Núcleo do Sistema

| Tipo        | Função                       | Repositório                                                          | GitPages                                                             |
| ----------- | ---------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Portal      | Entrada principal do sistema | [Portal](https://github.com/osvaldojeronymo/silic-portal-imoveis)    | [Portal](https://osvaldojeronymo.github.io/silic-portal-imoveis/)    |
| Serviços    | Solicitação de serviços      | [Serviços](https://github.com/osvaldojeronymo/silic-request-service) | [Serviços](https://osvaldojeronymo.github.io/silic-request-service/) |
| Operacional | Tratamento de demandas       | [Operacional](https://github.com/osvaldojeronymo/silic-hands-on)     | [Operacional](https://osvaldojeronymo.github.io/silic-hands-on/)     |
| Gestão      | Fila de trabalho             | [Gestão](https://github.com/osvaldojeronymo/silic-input-doc)         | [Gestão](https://osvaldojeronymo.github.io/silic-input-doc/)         |

##### Ações Rápidas

| Tipo        | Função                | Repositório                                                                        | GitPages                                                                           |
| ----------- | --------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Ação Rápida | Processo Digital      | [Processo Digital](https://github.com/osvaldojeronymo/silic-digital-process)       | [Processo Digital](https://osvaldojeronymo.github.io/silic-digital-process/)       |
| Ação Rápida | Motivos de Devolução  | [Motivos de Devolução](https://github.com/osvaldojeronymo/silic-catalog-reasons/)  | [Motivos de Devolução](https://osvaldojeronymo.github.io/silic-catalog-reasons/)   |
| Ação Rápida | Assinador Digital     | [Assinador Digital](https://github.com/osvaldojeronymo/silic-digital-process/)     | [Assinador Digital](https://osvaldojeronymo.github.io/silic-digital-signer/)       |
| Ação Rápida | Gerador de Documentos | [Gerador de Documentos](https://github.com/osvaldojeronymo/silic-call-for-tenders) | [Gerador de Documentos](https://osvaldojeronymo.github.io/silic-call-for-tenders/) |

O SILIC 2.0 segue uma arquitetura modular e evolutiva, com responsabilidades bem definidas, interfaces padronizadas e tomada de decisão orientada por governança.

Veja:

- [`/architecture/ecosystem-map.md`](/architecture/ecosystem-map.md)
- [`/architecture/roadmap.md`](/architecture/roadmap.md)
- [`/diagrams/system-context-diagram.md`](/diagrams/system-context-diagram.md)

## Roteiro Futuro

O roteiro está documentado em [`/architecture/roadmap.md`](/architecture/roadmap.md) e deve ser revisado periodicamente para alinhar prioridades, dependências e marcos de execução.

## Módulos Operacionais

Os módulos operacionais são mantidos com escopo, interfaces e limites de serviço bem definidos.

- Módulo A — _A definir_
- Módulo B — _A definir_
- Módulo C — _A definir_

## Ações Rápidas

- Revisar a documentação de arquitetura: [`/architecture`](/architecture)
- Revisar os padrões de governança: [`/governance`](/governance)
- Contribuir com artefatos de pesquisa e descoberta: [`/research`](/research)
- Adicionar referências visuais e diagramas: [`/diagrams`](/diagrams)

## Estrutura da Documentação

```text
/docs
/architecture
/governance
/research
/assets
/diagrams
```
