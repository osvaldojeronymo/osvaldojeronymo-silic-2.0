# Documentação

Este diretório contém modelos e referências transversais de documentação do SILIC 2.0.

## Conteúdo

| Categoria                 | Descrição                                            |
| ------------------------- | ---------------------------------------------------- |
| Documentação de processos | Materiais de referência para fluxos e procedimentos. |
| Guias operacionais        | Instruções práticas para execução e operação.        |
| Referências internas      | Documentos de apoio e alinhamento institucional.     |

## Situação

| Situação    | Detalhe                                                                      |
| ----------- | ---------------------------------------------------------------------------- |
| Em evolução | Adicionar documentos específicos de domínio à medida que forem formalizados. |

## Historias de usuario

As historias de usuario canonicas ficam em `docs/user-stories` e seguem um padrao de documento com metadado estruturado em front matter YAML. Esse formato foi adotado para habilitar exportacoes, indexacao, dashboards, geracao automatica de documentacao, integracao com IA e futura sincronizacao com IBM Jazz / EWM.

| Artefato                           | Tipo                | Modulo           | Status     | Observacao                                                              |
| ---------------------------------- | ------------------- | ---------------- | ---------- | ----------------------------------------------------------------------- |
| `docs/user-stories/HU-TEMPLATE.md` | Template padrao     | Generico         | Ativo      | Modelo base para novas HUs com metadado estruturado                     |
| `docs/user-stories/HU-PD-001.md`   | User Story canonica | Processo Digital | Homologado | Historia alinhada ao prototipo validado e preparada para mapeamento EWM |
