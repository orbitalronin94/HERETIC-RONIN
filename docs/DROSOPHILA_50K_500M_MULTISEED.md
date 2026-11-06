# Experimento Drosophila 50k — HERETIC 500M, tres semillas

## Objetivo

Aislar el efecto de entrenar desde inicialización aleatoria el estudiante HERETIC de
500.102.144 parámetros con el lote procedimental Drosophila 01301–51300, sin instructor,
sin destilación y sin tocar checkpoints existentes.

## Datos

Se consumen directamente los diez JSONL de \`data/drosophila/parts/\`:
5.000 filas por fichero, 50.000 filas en total. El script falla ante JSON inválido,
filas ausentes, IDs repetidos o recuentos distintos de los esperados. Registra SHA-256
por shard y del corpus concatenado, duplicados exactos y duplicados de texto normalizado.

El lote se describe en \`data/drosophila/README_01301_51300.md\` como sintético/procedimental:
50 familias con 1.000 parametrizaciones cada una. El volumen no equivale a 50.000
capacidades independientes. Se trata como train_candidate, nunca como holdout ni gold.

## Diseño

- Arquitectura: 500.102.144 parámetros; byte tokenizer; contexto 128.
- Semillas independientes: 17, 42 y 137.
- Inicialización: pesos aleatorios nuevos en cada semilla; no se sobrescribe ni se
  modifica el checkpoint del experimento anterior.
- Tutor: ninguno.
- Entrenamiento: 100 pasos de optimizador por semilla (300 pasos totales), batch 1,
  FP32, CPU, AdamW, LR constante 1e-4.
- Ejecución: matriz de GitHub Actions; cada semilla publica checkpoint y métricas.
- Retención: artefactos de Actions durante 90 días.

**Definición explícita de ciclo:** en esta iteración, “100 ciclos” se implementa como
100 actualizaciones del optimizador por semilla, no 100 pasadas completas (epochs)
sobre las 50.000 filas. La muestra de ventanas next-token es aleatoria y reproducible.
Esto permite un smoke experiment medible en runners CPU; no debe describirse como
100 epochs ni como exposición exhaustiva a cada fila.

## Métricas y límites

Cada ejecución publica loss inicial/final, duración, throughput del loop, tamaño del
checkpoint, inventario de shards, hashes y conteos de duplicados. La loss de entrenamiento
no demuestra razonamiento ni generalización. No se calcula benchmark de capacidad en
esta PR; el corpus no se usa como evaluación.

