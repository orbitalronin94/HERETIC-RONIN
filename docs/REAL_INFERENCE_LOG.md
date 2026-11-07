# HERETIC-RONIN — Registro de inferencias reales

Este documento conserva las respuestas generadas **por los pesos reales** de HERETIC-RONIN. Es una bitácora experimental, no una colección de respuestas escritas por una persona ni una evaluación de calidad.

## Criterios de registro

- Cada entrada debe proceder de una ejecución de GitHub Actions que haya cargado un checkpoint real y completado la generación.
- Se conserva literalmente el prompt y la continuación producida, sin corregir ortografía ni completar frases.
- Se anotan checkpoint, número de parámetros, método de decodificación, run y fecha cuando esos datos están disponibles.
- Una ejecución fallida o sin artefacto de inferencia no se presenta como respuesta del modelo.
- Las respuestas son continuaciones greedy de un modelo de predicción del siguiente byte; no debe confundirse esto con una conversación de un modelo instruction-tuned.

## Tanda 1 — «¿Quién eres?»

- Fecha: 2026-11-06
- Run: [42292725259](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42292725259)
- Checkpoint: step 600
- Parámetros: 500.102.144
- Decodificación: greedy
- Estado: generación completada y artefacto subido.

**Prompt**
```text
¿Quién eres?
```

**Continuación literal**
```text
a.
R: El erererera.
R: El entrera.
```

## Tanda 2 — Continuación sobre fotosíntesis

- Fecha: 2026-11-06
- Run: [42292201200](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42292201200)
- Checkpoint: step 600
- Parámetros: 500.102.144
- Decodificación: greedy
- Estado: generación completada y artefacto subido.

**Prompt**
```text
La fotosíntesis es el proceso mediante el cual
```

**Continuación literal**
```text
a ententa ententa ententa ententa ententa.
```

## Historial de ejecuciones sin respuesta archivada

- Run [42292516789](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42292516789): la generación falló antes de producir un resultado válido. No se cuenta como tanda ni se inventa una respuesta.

---

## Nuevas inferencias

Las siguientes tandas se añadirán automáticamente al completar con éxito los workflows de inferencia compatibles. El bot archivará el prompt, la continuación literal, los metadatos del checkpoint y el enlace al run. Cada run se registrará una sola vez.
