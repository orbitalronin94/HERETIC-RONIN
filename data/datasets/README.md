# HERETIC-RONIN — biblioteca de datasets

Actualizado: 2026-11-07. Este documento distingue **admitido**, **candidato** y **cuarentena**. El tamaño descargado nunca equivale por sí solo a tamaño entrenable.

## Resumen verificable

| Métrica | Valor |
|---|---:|
| Corpus base RONIN-IA admitido | 680.665.972 bytes |
| Cosmopedia v0.1 curada y admitida | 4.734 documentos · 22.927.899 bytes |
| Auditoría combinada | 261.039 documentos examinados |
| Exclusiones exactas/near-duplicate | 68 extremos |
| Subconjunto resultante autorizado | 260.971 documentos |
| Total de bytes admitidos contabilizados | **703.593.871 bytes (671,0 MiB)** |
| Objetivo de biblioteca | 500.000.000.000 bytes (500 GB decimal) |

Auditoría global: [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). Artefacto de auditoría: ID `13570263309`, SHA-256 `db826ced0bcd9158fee17d254faad203e7fe9e317f510e12fcf2cd448bb42dc9`.

La auditoría detectó 9 grupos/hits exactos y 68 pares SimHash. Los 68 índices excluidos están dentro del bloque base de 256.305 registros; los 4.734 documentos Cosmopedia permanecen en el subconjunto autorizado. No hubo coincidencias exactas con las 120 preguntas sintéticas de diagnóstico. Esto es una heurística de deduplicación y contaminación, no una prueba semántica ni un benchmark público.

## Datasets admitidos

| Fuente | Contenido | Filas admitidas | Bytes admitidos | Uso |
|---|---|---:|---:|---|
| RONIN-IA train-only (CoVoST2, ScienceVerse, Mathlib4, literatura española, NASA revisado, Papers propio) | Multilingüe, ciencia, matemáticas, traducción y texto | 256.237 tras deduplicación | 680.665.972 | Preentrenamiento experimental; Papers solo uso interno autorizado |
| Cosmopedia v0.1 `auto_math_text/train` | Prosa educativa y matemática sintética | 4.734 | 22.927.899 | Next-token pretraining experimental; no gold answers ni razonamiento verificado |

### Cosmopedia v0.1 — ficha de admisión

- Fuente: [HuggingFaceTB/cosmopedia](https://huggingface.co/datasets/HuggingFaceTB/cosmopedia)
- Revisión: `0ae6ec63f91742bd2d1eaef4f02232c55d719385`
- Config/split: `auto_math_text/train`
- Licencia declarada en la ficha: Apache-2.0.
- SHA-256 del payload original: `050b03f64c3e9976d91ff86447761174f46121c0af899004172368f61255dcc6`.
- Curación: 5.000 entradas; 4.734 conservadas; 266 rechazadas (265 con caracteres de control/reemplazo y 1 por longitud).
- Revisión humana: 50 fragmentos deterministas estratificados.
- SHA-256 del JSONL curado: `f474a3d8bd7a18ab7cac222ae1f2906c52bdaa346a27ca0df728039ac1438f9a`.
- Auditoría global: [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447).

**Limitación de calidad y derechos:** el contenido es sintético y hereda una línea de semillas externas de AutoMathText. La revisión detectó explicaciones mayormente coherentes, pero también notación dañada y posibles errores matemáticos. La declaración Apache-2.0 de la ficha se registra como evidencia del publicador; no es una opinión legal ni una verificación independiente de cada semilla. Se admite solo como texto experimental de next-token, no como supervisión de respuestas correctas.

## Candidatos descargados — no admitidos

El lote de 100 bibliotecas del [run 42356179021](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42356179021) produjo:

- 531.963 filas candidatas.
- 1.670.605.627 bytes sin comprimir (~1,56 GiB).
- Artefacto ZIP: 749.837.093 bytes.
- **Bytes admitidos aportados por este lote: 0** hasta completar revisión y auditorías por fuente.

| Fuente/lote | Filas candidatas | Bytes de texto | Estado |
|---|---:|---:|---|
| FineWeb-Edu | 100.000 | 424.092.222 | Cuarentena: derechos de páginas Common Crawl no resueltos por ODC-By |
| OpenWebMath | 100.000 | 456.695.086 | Cuarentena: contenido de blogs/foros/Q&A; licencia del contenido subyacente no resuelta |
| Cosmopedia v0.1 raw | 50.000 | 234.364.804 | Solo el slice separado curado de 4.734 filas está admitido |
| Cosmopedia v2 | 50.000 | 278.500.947 | Cuarentena: lineage de semillas mixto |
| Wikidata | 50.000 | 165.781.647 | Candidato CC0; falta muestra y auditoría global |
| Aya | 25.000 | 42.931.184 | Candidato Apache-2.0; falta revisión de privacidad/splits y auditoría global |
| LibriSpeech train.clean.360 | 50.000 | 19.208.974 | Candidato CC-BY-4.0; texto solo, pendiente muestra y auditoría |
| VoxPopuli (6 idiomas) | 106.963 | En manifiesto | Candidato CC0; pendiente revisión por idioma y auditoría |

## Siguiente tanda de adquisición/revisión

Las PR [#21](https://github.com/orbitalronin94/HERETIC-RONIN/pull/21) y [#22](https://github.com/orbitalronin94/HERETIC-RONIN/pull/22) ya están mergeadas. El recolector incluye las fuentes siguientes, pero sus nuevas descargas siguen siendo candidatas hasta completar la auditoría:

- PubMed filtered: aceptar únicamente registros con URI exacta CC-BY-4.0 o CC0; el propio Common Pile advierte de posibles errores de metadatos.
- OpenThoughts3: Apache-2.0 declarado, pero prompts derivados de fuentes upstream requieren revisión de derechos.
- OpenR1-Math: Apache-2.0 declarado; los problemas proceden de NuminaMath 1.5, cuya procedencia debe resolverse.
- IFM Code/Math: Apache-2.0 declarado; falta trazabilidad completa de origen y validación de calidad/corrección.

Todos siguen como candidatos; sus bytes no se suman al total admitido. La siguiente admisión requiere revisión de muestra, procedencia/licencia, integridad SHA-256, deduplicación global, control de holdout y registro de la autorización exacta.

## Regla operativa

1. Descubrir fuente y fijar revisión inmutable.
2. Descargar solo split/config explícitos; preservar metadatos y atribución.
3. Validar esquema, calidad, privacidad y seguridad.
4. Revisar muestras estratificadas manualmente.
5. Deduplicar exacta y aproximadamente contra todo el corpus.
6. Ejecutar auditoría global y control de contaminación.
7. Contar bytes solo después de una admisión explícita en el registro.
8. Conectar el dataset al workflow de entrenamiento y verificarlo en sus logs/manifiestos antes de afirmar que el modelo lo consumió.

El piloto de 500 pasos [run 42358300901](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42358300901) comenzó antes de la admisión de Cosmopedia y utiliza el corpus base; no se le atribuye el nuevo dataset. Los artefactos de Actions son staging temporal, no almacenamiento permanente de cientos de GB.

## Nueva expansión documental — 2026-11-07 (candidatos)

Se amplía el siguiente lote con tres fuentes de mayor volumen y dominios complementarios. **Todavía no suman bytes admitidos**: la adquisición fija la revisión de Hub y genera muestras, pero cada fuente debe superar revisión de derechos, calidad, deduplicación global y holdout.

| Fuente | Volumen publicado | Slice inicial | Licencia/procedencia | Estado |
|---|---:|---:|---|---|
| [Spanish-PD-Books](https://huggingface.co/datasets/PleIAs/Spanish-PD-Books) | 52,1 GB; 302.640 libros; 13,9B palabras | 2 shards Parquet fijados (583 MB + 593 MB; máximo 5.000 textos) | El publicador afirma dominio público en la UE por autor fallecido hace más de 70 años; agregación BDH + Internet Archive | Candidato: verificar autor/fecha, procedencia y OCR por muestra |
| [CourtListener / docketx](https://huggingface.co/datasets/docketx/us-caselaw-fed-district) | 8,47 GB; ~1,31M opiniones | Hasta 100.000 opiniones | CC0 de empaquetado; opiniones judiciales estadounidenses de dominio público | Candidato: verificar tipo de opinión, calidad, metadatos y deduplicación |
| [OpenStax text](https://huggingface.co/datasets/crumb/openstax-text) | 3.354.565 filas; 159 MB; 76 libros | Hasta 50.000 textos | CC-BY-4.0 declarado por la ficha del dataset | Candidato: comprobar licencia por libro/edición y atribución embebida |

### Detalles de adquisición

- Spanish-PD-Books: shards `spanish_pd_1.parquet`, `spanish_pd_10.parquet`, `spanish_pd_100.parquet` y `spanish_pd_101.parquet`; se preservan `identifier`, `creator`, `title`, `publication_date` y `word_count`. La ficha muestra problemas de esquema en el visor; la adquisición aislada por shard evita mezclar esquemas incompatibles. El estado sigue siendo candidato hasta revisar derechos y OCR.
- CourtListener: solo `text` como payload, conservando identificador, jurisdicción, título, fuente, licencia, cita, tribunal y fecha.
- OpenStax: se conserva el texto con atribución original; la licencia general de OpenStax puede variar por libro/edición, así que la etiqueta CC-BY-4.0 de la colección no es suficiente para admitirla.

Los nuevos artefactos se separan por fuente para facilitar descarga e inspección sin depender de un único ZIP multi-GB. Referencias: [ficha Spanish-PD-Books](https://huggingface.co/datasets/PleIAs/Spanish-PD-Books), [ficha CourtListener](https://huggingface.co/datasets/docketx/us-caselaw-fed-district), [ficha OpenStax](https://huggingface.co/datasets/crumb/openstax-text).


## Expansión de gran escala — Common Corpus y bibliotecas históricas (candidatos)

| Fuente | Tamaño declarado | Muestra configurada | Condición de admisión |
|---|---:|---:|---|
| [PleIAs Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus) | 2,27 billones de tokens | Hasta 20.000 registros | Filtro exacto por licencia individual; conservar colección, tipo, idioma, autoría e identificador; excluir CC-BY-SA/NC/ND/desconocidas |
| [English-PD](https://huggingface.co/datasets/PleIAs/English-PD) | 362 GB; 736.214 títulos; 78,6B palabras | Dos shards: 497 MB + 447 MB | Verificar criterio pre-1884/dominio público, metadatos y OCR |
| [Spanish-PD-Newspapers](https://huggingface.co/datasets/PleIAs/Spanish-PD-Newspapers) | 48,6 GB; 247.491 textos; 2,7B palabras | Un shard de 69,6 MB | Verificar procedencia, fecha, dominio público y OCR |

Common Corpus reúne OpenCulture, OpenGovernment, OpenSource, OpenScience, OpenWeb y OpenSemantic. La ficha declara procedencia y licencia por documento; el workflow solo deja pasar una lista cerrada de etiquetas exactas (CC0, dominio público, CC-BY-4.0, MIT, Apache-2.0, Open Parliament Licence v3.0 y Licence Ouverte). No se acepta una etiqueta general de colección como sustituto de la licencia del registro. Referencia: [ficha Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus).

English-PD y Spanish-PD-Newspapers proceden de corpus patrimoniales agregados y OCR. Sus fichas declaran dominio público con criterio de autor fallecido hace más de 70 años; se mantienen candidatos hasta verificar muestras y metadatos de cada obra/periódico. English-PD declara títulos pre-1884 como medida adicional. Referencias: [English-PD](https://huggingface.co/datasets/PleIAs/English-PD), [Spanish-PD-Newspapers](https://huggingface.co/datasets/PleIAs/Spanish-PD-Newspapers).


## Nueva tanda multilingüe — candidatos, no admitidos

Se incorporan dos fuentes adicionales al recolector; ambas permanecen fuera del corpus activo hasta terminar descarga, revisión humana, deduplicación global y escaneo de holdout.

| Fuente | Alcance candidato | Licencia / filtro | Estado |
|---|---|---|---|
| [dataseek/ptbr-books-publicos](https://huggingface.co/datasets/dataseek/ptbr-books-publicos) | 28,2k filas de libros en portugués brasileño; límite de adquisición 10.000 | CC0-1.0 declarado por la ficha; verificar procedencia y situación de cada obra | Candidato; 0 bytes admitidos |
| [coral-nlp/german-commons](https://huggingface.co/datasets/coral-nlp/german-commons) — `cultural` | 10.000 filas como máximo de un corpus de 258 GB / 154,56B tokens globales | Filtro estricto: **todos** los valores de licencia por documento deben ser CC0-1.0 o CC-BY-4.0 exactos | Candidato; 0 bytes admitidos |

El recolector ahora rechaza filas German Commons con licencia desconocida, combinaciones mixtas, BY-SA, NC o ND; la licencia ODC-BY de la agregación no se usa para relicenciar los textos. Se conservan `id`, `source`, `subset`, `license`, `num_tokens` y `ocr_score`. En portugués se conservan nombre de fichero, tipo de libro, longitud y timestamp para comprobar pureza lingüística, OCR y procedencia.

**Fuente descartada deliberadamente:** Institutional Books / Harvard Library anuncia 983.004 libros y 242B tokens, pero su ficha remite a términos de acceso anticipado; Harvard limita su Public Domain Corpus a usos sin ánimo de lucro, educativos y de investigación. No lo incorporamos a la cola de entrenamiento general hasta que los términos permitan expresamente ese uso. No cuenta como material candidato ni admitido.


## Estado de adquisición — actualización 2026-11-07 14:20 CET

### Inventario admitido

- **260.971 documentos únicos**
- **703.593.871 bytes admitidos** (671,0 MiB)
- **0,1407 %** del objetivo de 500.000.000.000 bytes
- **Nuevas admisiones en esta ejecución: 0 documentos / 0 bytes**

El último global audit autorizado sigue siendo [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). Su alcance es el corpus train-only RONIN-IA y la tranche Cosmopedia v0.1 curada que se suministró expresamente; no autoriza ningún otro candidato.

### Lote candidato terminado — run 42357699240

[Run 42357699240](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42357699240) terminó con fallo del umbral de escala, después de publicar el artefacto para inspección:

| Métrica | Resultado |
|---|---:|
| Filas candidatas en manifiesto | 531.963 |
| Bytes JSONL candidatos | 1.670.605.627 |
| Objetivo de adquisición candidato | 6.800.000.000 bytes |
| Escala frente al corpus admitido anterior | 2,45× |
| Artefacto ZIP | 749.837.081 bytes |
| Artifact ID | `13573027505` |
| SHA-256 del artefacto | `e58188d5ca788df5f330905996a5592896f090fa1f19088ac7edae728f6eb1de` |
| Bytes nuevos admitidos | **0** |

[Descargar/ver artefacto en Actions](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42357699240/artifacts/13573027505). El manifiesto completo y los SHA-256 de cada JSONL están registrados en `data/sources/registry.json` bajo `candidate_acquisitions`.

| Fuente/configuración train | Filas candidatas | Bytes JSONL | Decisión actual |
|---|---:|---:|---|
| [FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) `sample-10BT` | 100.000 | 424.092.222 | Cuarentena: ODC-By cubre la base de datos; derechos de páginas Common Crawl siguen sin resolverse |
| [OpenWebMath](https://huggingface.co/datasets/open-web-math/open-web-math) | 100.000 | 456.695.086 | Cuarentena: derechos de las páginas subyacentes y términos Common Crawl |
| [Cosmopedia v0.1](https://huggingface.co/datasets/HuggingFaceTB/cosmopedia) `auto_math_text` raw | 50.000 | 234.364.804 | Candidato bruto; no sustituye ni amplía la tranche curada de 4.734 ya admitida y exige deduplicación |
| [Cosmopedia v2](https://huggingface.co/datasets/HuggingFaceTB/smollm-corpus) `cosmopedia-v2` | 50.000 | 278.500.947 | Cuarentena: linaje mixto y repetición de plantillas |
| [Aya](https://huggingface.co/datasets/CohereLabs/aya_dataset) `default` | 25.000 | 42.931.184 | Candidato: Apache-2.0 verificado en el Hub; faltan PII, linaje y revisión multilingüe |
| [Wikidata](https://huggingface.co/datasets/philippesaade/wikidata) | 50.000 | 165.781.647 | Candidato CC0; faltan calidad, procedencia, deduplicación y holdout |
| [LibriSpeech](https://huggingface.co/datasets/openslr/librispeech_asr) `train.clean.360` | 50.000 | 19.208.974 | Candidato CC-BY-4.0; texto solo y atribución pendiente de auditoría |
| [VoxPopuli](https://huggingface.co/datasets/facebook/voxpopuli) es/en/de/fr/it/pl | 106.963 | 49.030.763 | Candidato CC0; solo transcripciones gold de train, falta revisión por idioma |

Todos los shards anteriores tienen revisión inmutable, split y SHA-256 individual en el registro. **No superaron** la revisión humana, deduplicación cruzada, contaminación global de holdout ni gates finales de derechos/procedencia; no tienen `training_eligible` ni autorización para entrenamiento. Cosmopedia v0.1 raw comparte fuente/config con la tranche curada anterior: sus 234.364.804 bytes no se suman como material nuevo admitido.

### Fuentes que no produjeron un shard candidato válido

- **Schema sin columna `text` utilizable:** PubMed filtered, CCCC, Data Provenance Initiative, StackExchange, PressBooks, LibreTexts, DOAB, OERCommons y News. No se relaja el esquema ni se infiere licencia desde el agregador.
- **arXiv complete:** solo 6.650 filas utilizables, por debajo del mínimo configurado; se deja fuera del total candidato.
- **LibriSpeech `train.clean.100`:** 21.038 transcripciones utilizables, por debajo del mínimo configurado; solo `train.clean.360` produjo el shard de 50.000 filas.
- El umbral de 6,8 GB no se alcanzó. El fallo del workflow no convierte los archivos del artefacto en datos admitidos.

### Estado de los siguientes workflows y corrección de seguridad

- [Run 42366207131](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42366207131): seguía en streaming; se ejecuta sobre `86348b6c5d5215416c894abdda38ca8855abd06b`, anterior al filtro exacto. Cuando termine, su bundle seguirá en cuarentena.
- [PR #23](https://github.com/orbitalronin94/HERETIC-RONIN/pull/23) integrada en [commit 7f0e539](https://github.com/orbitalronin94/HERETIC-RONIN/commit/7f0e539069222682924588bf23d3fe124b9e2b1b): el filtro de licencia por registro ahora compara valores completos, rechaza ausencias/mezclas/ambigüedades y no acepta CC-BY-SA como CC-BY. [Run 42377093318](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42377093318): compilación y 8 pruebas unitarias correctas.
- [Run 42377212260](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42377212260): en cola por exclusión mutua; utilizará el nuevo filtro al comenzar.
- PR #18, catálogo de 100 bibliotecas: no integrado y no mergeable. El diff añade el catálogo pero no modifica el recolector para leerlo; además, sus etiquetas genéricas de licencia no sustituyen la verificación de cada payload. Sus 100 entradas no son descargas ni admisiones.

No se debe cancelar el workflow activo ni lanzar otra adquisición concurrente. La siguiente revisión debe inspeccionar el manifiesto/artifact del run 42366207131, y después auditar cada shard con el código exacto ya integrado. Hasta que todos los gates pasen, el contador admitido permanece en **260.971 documentos / 703.593.871 bytes**.
