# Diagrama de Contexto do Sistema

Este documento representa visualmente como os módulos do ecossistema SILIC 2.0 se conectam com base nas evidências reais encontradas no código-fonte disponível.

```mermaid
flowchart LR
    Portal[Portal Principal\nsilic-portal-imoveis]

    Solicitacao[Gestão de Imóveis SAP\nsilic-request-service]
    Gestao[Gestão e Perfis Operacionais\nsilic-input-doc]
    Operacao[Tratamento Operacional\nsilic-hands-on]
    Processo[Processo Digital\nsilic-digital-process]
    Assinador[Assinador Digital\nsilic-digital-signer]
    Motivos[Motivos de Devolução\nsilic-catalog-reasons]
    Documentos[Gerador de Documentos\nsilic-call-for-tenders]

    Portal --> Solicitacao
    Portal --> Gestao
    Portal --> Operacao
    Portal --> Processo
    Portal --> Assinador
    Portal --> Motivos
    Portal --> Documentos

    Solicitacao -. voltarAoPortal .-> Portal
    Gestao -. voltarAoPortal .-> Portal
    Operacao -. voltarAoPortal .-> Portal
    Processo -. voltarAoPortal .-> Portal
    Assinador -. retorno configurado .-> Portal
    Documentos -. link para portal .-> Portal

    Nota1[Sem evidência forte, até aqui, de integrações runtime módulo a módulo]
    Nota1 -.- Gestao
    Nota1 -.- Operacao
```

## Leitura do Diagrama

- O padrão dominante confirmado no código é `portal -> módulos satélite`, por navegação direta entre URLs publicadas.
- Vários módulos também implementam caminho explícito de retorno ao portal.
- O nó de `silic-request-service` foi relabelado para o papel realmente sustentado pelo código: um protótipo legado de gestão de imóveis com dados SAP e locadores.
- O diagrama não afirma integrações técnicas diretas entre os módulos satélite, porque elas ainda não foram comprovadas no código revisado.

## Uso Recomendado

- Utilizar este diagrama como referência visual de alto nível.
- Usar `architecture/fluxo-negocio-desejado.md` quando a discussão for sobre jornada alvo de negócio, e não sobre arquitetura comprovada.
- Manter diagramas derivados separados para distinguir fluxo desejado de negócio e arquitetura comprovada em código.
- Refinar este diagrama quando surgirem contratos, APIs e eventos formalizados entre os módulos.
