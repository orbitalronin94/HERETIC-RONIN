# HERETIC-RONIN

### MODELO LARGO. MÉTODO CORTO.

*La mosca no necesitaba pureza. Necesitaba sobrevivir.*

HERETIC-RONIN es un laboratorio experimental para estudiar cuánto aprendizaje puede extraerse de modelos pequeños mediante corpus amplios, entrenamiento eficiente, transferencia y evaluación comparativa.

Su principio es sencillo: **experimentar sin reverencia, medir sin indulgencia**. Un conjunto de datos grande no equivale automáticamente a un conjunto bueno; un checkpoint que reduce la pérdida no demuestra por sí solo más capacidad.

---

## Estado actual

| Elemento | Estado verificado |
|---|---|
| Estudiante experimental | 500.102.144 parámetros |
| Corpus Drosophila versionado | 50.000 filas candidatas |
| Estructura | 10 shards JSONL de 5.000 filas |
| Dominios actuales | Matemáticas, álgebra, lógica, programación, física, química, probabilidad, estadística, economía e ingeniería |
| Naturaleza del lote actual | Sintético y procedimental; no corpus gold |
| Objetivo de expansión | 500.000 ejemplos candidatos, sujetos a curación |
| Promoción de datos | Nunca automática por volumen |
| Evaluación | Holdout separado; nunca se incorpora al entrenamiento |

**Importante:** las 50.000 filas actuales se generaron mediante plantillas procedimentales. Los IDs distintos garantizan filas identificables, no diversidad semántica ni corrección independiente. El lote sirve como material experimental, pero no debe describirse como 50.000 ejemplos humanos verificados ni como 50.000 capacidades distintas. La propia ficha del lote documenta esta limitación.

## Biblioteca de datos

La fuente versionada del corpus está en `data/drosophila/`:

- `data/drosophila/parts/`: shards JSONL de entrenamiento.
- `data/drosophila/README_01301_51300.md`: ficha y limitaciones del lote sintético de 50.000 filas.

La biblioteca crecerá hacia **500.000 candidatos**, pero el contador bruto y el contador admitido deben mantenerse separados. Cada nuevo lote debe conservar, como mínimo:

1. Fuente y URL de origen, licencia y condiciones de redistribución.
2. Hash del material original y del shard procesado.
3. Dominio, idioma, fecha de adquisición y método de extracción.
4. Esquema validado, filas válidas y filas rechazadas.
5. Deduplicación exacta y aproximada frente a toda la biblioteca existente.
6. Filtros de calidad, contaminación, privacidad y seguridad.
7. Muestreo de revisión humana y resultados de auditoría.

### Estados de admisión

- **candidate:** descargado o generado; todavía no acreditado.
- **screened:** ha superado validaciones automáticas y controles de duplicados.
- **reviewed:** ha pasado revisión estratificada de contenido y procedencia.
- **admitted:** cumple licencia, trazabilidad, calidad y controles de contaminación.
- **rejected:** excluido con motivo registrado.

Solo los ejemplos `admitted` pueden entrar en el corpus de entrenamiento por defecto. Los candidatos no revisados no deben mezclarse silenciosamente con los admitidos.

## Objetivo de expansión: 50k → 500k

La expansión se realizará por lotes incrementales y reproducibles. La prioridad no es rellenar 450.000 huecos con variaciones de plantillas: es incorporar fuentes abiertas con licencias compatibles, contenido útil y diversidad real de tareas, dominios, idiomas y niveles de dificultad.

Orden de trabajo:

1. Inventariar fuentes y verificar licencias en la fuente primaria.
2. Adquirir lotes pequeños y registrar su procedencia antes de procesarlos.
3. Normalizar a un esquema JSONL común sin borrar metadatos.
4. Ejecutar validación estructural, deduplicación y filtros de calidad.
5. Auditar muestras estratificadas; rechazar fuentes que no superen los controles.
6. Integrar únicamente lotes admitidos y actualizar el manifiesto y este README.
7. Repetir hasta alcanzar 500.000 ejemplos **admitidos**, no simplemente descargados.

No se afirmará que se alcanzó el objetivo hasta que un inventario reproducible cuente los registros admitidos y publique hashes y auditoría.

## Entrenamiento y evaluación

Los experimentos se ejecutan mediante GitHub Actions. Los workflows y scripts versionados son la fuente de verdad; este README describe el estado y las reglas, no promete una receta fija de entrenamiento.

El experimento de 500M sobre los shards Drosophila de 50k está definido en [`drosophila-50k-500m-multiseed.yml`](.github/workflows/drosophila-50k-500m-multiseed.yml). El experimento de continuación sin tutor y comparación pareada se mantiene en su workflow específico. Cada resultado debe enlazar el run y sus artefactos; no se considerará exitoso hasta inspeccionar checkpoint, logs y reporte.

Reglas experimentales:

- Separar estrictamente entrenamiento, validación y holdout.
- Comparar antes/después con los mismos IDs, configuración y condiciones.
- Registrar semilla, pasos, configuración, hashes, tiempo y recursos.
- Informar resultados por dominio y cambios de predicción.
- No promocionar checkpoints ni corpus por pérdida de entrenamiento o tamaño.
- Conservar resultados negativos y fallos de ejecución.

## Arquitectura del estudiante

El experimento de 500M utiliza una arquitectura de **500.102.144 parámetros**. Es un estudiante experimental, no una afirmación de capacidad equivalente a un modelo de 500M entrenado a gran escala. La calidad se juzga por evaluaciones externas y controles reproducibles.

## Filosofía del laboratorio

RONIN-IA y HERETIC-RONIN exploran métodos distintos. HERETIC acepta datos heterogéneos, síntesis y recetas agresivas, pero no confunde velocidad con evidencia. La herejía consiste en probar caminos no convencionales; no en rebajar los criterios para declarar una victoria.

> La única herejía imperdonable sería dejar de medir porque el resultado nos gusta.

---

## Licencias

El código de este repositorio se distribuye bajo MIT. Los datasets, checkpoints, modelos docentes y materiales externos conservan sus propias licencias, atribuciones y restricciones. La licencia MIT del repositorio no sustituye ni amplía los derechos sobre esos materiales.
