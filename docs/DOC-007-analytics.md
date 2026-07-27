# DOC-007 - Analytics Executivo

## Objetivo

O módulo de Analytics não deve apenas desenhar gráficos. Ele deve ajudar o gestor a decidir.

## Comportamento esperado

Ao receber CSV ou XLSX, Daniel deve:

- identificar medida principal, como valor_total, receita, faturamento ou quantidade;
- identificar dimensões relevantes, como vendedor, produto, região, canal ou cliente;
- calcular KPIs básicos;
- gerar rankings;
- gerar evolução temporal quando houver coluna de data;
- apontar leitura executiva;
- sugerir ações práticas;
- permitir download dos resultados.

## Exemplo de resposta desejada

```text
Analisei a planilha enviada e transformei os dados em uma leitura executiva.

Leitura executiva:
- A base contém 30 registros e movimenta R$ 175.000,00.
- O maior destaque por vendedor é Ana Silva, com 27% do total.
- O último período mostra crescimento em relação ao primeiro.

Recomendações:
- Validar as práticas dos vendedores líderes e replicar nas equipes abaixo da média.
- Investigar regiões com baixa participação antes de definir cobrança.
- Criar acompanhamento semanal do indicador principal.
```

## Persistência

Dashboards gerados devem permanecer no histórico da conversa. Se o gestor enviar uma nova mensagem, a análise anterior não deve desaparecer.
