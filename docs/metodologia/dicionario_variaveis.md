# Dicionário de variáveis

Fonte principal: `basedosdados.br_mec_sisu.microdados`

## Variáveis originais utilizadas

- `ano`: ano de referência do SiSU.
- `id_municipio_candidato`: código IBGE do município de residência do candidato.
- `nome_curso`: nome do curso escolhido na inscrição.
- `turno`: turno associado ao curso escolhido.

## Variável derivada

- `total_inscricoes`: contagem agregada de inscrições para cada combinação de `ano`,
  `nome_curso` e `turno`.

## Observações analíticas

- A unidade analítica do pipeline é a inscrição agregada.
- O uso de `COUNT(1)` contabiliza registros da base filtrada, não pessoas únicas.
- Resultados sobre evasão ou permanência exigem integração com outras bases ou
  enquadramento analítico adicional.
