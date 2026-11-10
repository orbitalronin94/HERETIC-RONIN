# HERETIC-RONIN — biblioteca de datasets

Actualizado: 2026-11-10. Este documento distingue **admitido**, **candidato** y **cuarentena**. El tamaño descargado nunca equivale por sí solo a tamaño entrenable.

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

**Exclusión de share-alike (2026-11-07):** los 5.000 registros CC-BY-SA-4.0 de Stack Exchange registrados en el run 42295370306 quedan en estado *held/excluded*. Share-alike no está aprobado para este uso: no se readquieren, no se entrenan y aportan **0 bytes admitidos**.

## Siguiente tanda de adquisición/revisión

Las PR [#21](https://github.com/orbitalronin94/HERETIC-RONIN/pull/21) y [#22](https://github.com/orbitalronin94/HERETIC-RONIN/pull/22) ya están mergeadas. El recolector incluye las fuentes siguientes, pero sus nuevas descargas siguen siendo candidatas hasta completar la auditoría:

- PubMed filtered: aceptar únicamente registros con URI exacta CC-BY-4.0 o CC0; el propio Common Pile advierte de posibles errores de metadatos.
- OpenThoughts3: Apache-2.0 declarado, pero prompts derivados de fuentes upstream requieren revisión de derechos.
- OpenR1-Math: Apache-2.0 declarado; los problemas proceden de NuminaMath 1.5, cuya procedencia debe resolverse.
- IFM Code/Math: Apache-2.0 declarado; falta trazabilidad completa de origen y validación de calidad/corrección.

Todos siguen como candidatos; sus bytes no se suman al total admitido. La siguiente admisión requiere revisión de muestra, procedencia/licencia, integridad SHA-256, deduplicación global, control de holdout y registro de la autorización exacta.

### Descubrimiento nuevo — discursos del Parlamento Europeo (solo candidato)

La API oficial [Open Data API v2](https://data.europarl.europa.eu/en/developer-corner/opendata-api) ofrece /speeches; el tipo PLENARY_DEBATE_SPEECH permite acotar discursos y include-output=xml_fragment solicita el fragmento textual. La especificación de la API declara CC-BY-4.0 y las [reglas de Open Data del Parlamento](https://data.europarl.europa.eu/en/discover/rules-on-the-european-parliaments-open-data) adoptan CC-BY-4.0 para sus datos abiertos. **No se ha descargado nada (0 bytes):** el endpoint es mutable y el catálogo distingue recursos bajo aviso legal. Antes de adquirir, hay que fijar snapshot/hash, confirmar licencia por recurso, excluir terceros y revisar privacidad/metadatos.

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

### Nueva fuente primaria descubierta — PMC Open Access Subset (candidata)

Se ha registrado [PMC Open Access Subset](https://pmc.ncbi.nlm.nih.gov/tools/openftlist/) como candidato biomédico de alto valor, **sin descargar ni contar bytes**. NCBI/NLM ofrece recuperación automatizada autorizada mediante [OAI-PMH](https://pmc.ncbi.nlm.nih.gov/tools/oai/) y [Cloud Service](https://pmc.ncbi.nlm.nih.gov/tools/cloud/); el scraping sistemático de la web principal está prohibido. La licencia varía por artículo y NLM no posee los derechos de autor. Referencias oficiales: [PMC Open Access Subset](https://pmc.ncbi.nlm.nih.gov/tools/openftlist/), [PMC OAI-PMH](https://pmc.ncbi.nlm.nih.gov/tools/oai/), [PMC Cloud Service](https://pmc.ncbi.nlm.nih.gov/tools/cloud/) y [PMC Copyright Notice](https://pmc.ncbi.nlm.nih.gov/about/copyright/).

El piloto propuesto acepta únicamente URI exactas **CC-BY-4.0 o CC0-1.0**. Se rechazan BY-SA, BY-ND, NC, otras versiones, licencias personalizadas, ausentes o ambiguas; los filtros de búsqueda CC BY/CC0 son solo descubrimiento y cada XML debe validarse individualmente. El OAI-PMH limita el tráfico a 3 solicitudes/s y pide no usar solicitudes concurrentes; los lotes de más de 100 solicitudes deben ejecutarse fuera de horas punta de EE. UU. Referencias: [guía de búsqueda PMC por licencia](https://pmc.ncbi.nlm.nih.gov/about/userguide/) y [límites y formatos OAI-PMH](https://pmc.ncbi.nlm.nih.gov/tools/oai/).

Antes de adquirir: fijar fecha de inventario, lista completa de PMCIDs y su SHA-256; conservar DOI, autores, journal, versión, licencia y atribución; excluir material de terceros, figuras, suplementos, retirados, PII y datos clínicos identificables; y ejecutar deduplicación/holdout global y revisión humana. Estado en el registro: `priority_candidate_official_license_filtered_pilot_not_acquired`; **0 filas / 0 bytes admitidos**.

### Estado de los siguientes workflows y corrección de seguridad

- [Run 42366207131](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42366207131): seguía en streaming; se ejecuta sobre `86348b6c5d5215416c894abdda38ca8855abd06b`, anterior al filtro exacto. Cuando termine, su bundle seguirá en cuarentena.
- [PR #23](https://github.com/orbitalronin94/HERETIC-RONIN/pull/23) integrada en [commit 7f0e539](https://github.com/orbitalronin94/HERETIC-RONIN/commit/7f0e539069222682924588bf23d3fe124b9e2b1b): el filtro de licencia por registro ahora compara valores completos, rechaza ausencias/mezclas/ambigüedades y no acepta CC-BY-SA como CC-BY. [Run 42377093318](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42377093318): compilación y 8 pruebas unitarias correctas.
- [Run 42377212260](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42377212260): en cola por exclusión mutua; utilizará el nuevo filtro al comenzar.
- PR #18, catálogo de 100 bibliotecas: no integrado y no mergeable. El diff añade el catálogo pero no modifica el recolector para leerlo; además, sus etiquetas genéricas de licencia no sustituyen la verificación de cada payload. Sus 100 entradas no son descargas ni admisiones.

No se debe cancelar el workflow activo ni lanzar otra adquisición concurrente. La siguiente revisión debe inspeccionar el manifiesto/artifact del run 42366207131, y después auditar cada shard con el código exacto ya integrado. Hasta que todos los gates pasen, el contador admitido permanece en **260.971 documentos / 703.593.871 bytes**.


## Adquisición candidate-only — run 42379525699 (revisión 2026-11-08)

El [run 42379525699](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42379525699) terminó después de conservar sus artefactos. El workflow marcó fallo porque no alcanzó su umbral de escala de 6.800.000.000 bytes; no fue una admisión ni una auditoría global.

| Métrica | Resultado |
|---|---:|
| Filas completadas en el manifiesto | 780.527 |
| Bytes JSONL completados en el manifiesto | 4.505.001.697 |
| ZIP candidato | 1.860.559.190 bytes |
| SHA-256 del ZIP (digest de GitHub Actions) | `4580efd18cbc11ed2c94947236a3a814b32345fc540a5df6e1550bce01266018` |
| SHA-256 del manifiesto | `083b0fa38ffd57ec9d78f05d4d2d767d2c30d88f28a1acc2b120744b79b4c39f` |
| SHA-256 de muestras estratificadas | `24d7fb0a000a0fa5c2d462db6ba661650982a13c5e8dab08cc91e6c07d69a89c` |
| Fuentes completadas / fallidas | 25 / 12 |
| Nuevas admisiones | **0 documentos / 0 bytes** |

**Cuarentena obligatoria del lote completo.** El manifiesto cuenta solo los shards que superaron el mínimo de filas, pero el workflow subió también archivos parciales creados por fuentes que fallaron después de escribir. Se verificaron 117.712.976 bytes expandidos de shards parciales de Spanish-PD-Books cuyo manifiesto declara cero filas y cero bytes. El ZIP incluye por tanto material no reconciliado; ni su tamaño comprimido ni esos parciales se cuentan como admitidos. No se ejecutaron deduplicación cruzada, G-0, contaminación global ni revisión humana de derechos.

### Candidatos de mayor volumen (todos no admitidos)

| Fuente | Filas | Bytes JSONL | Motivo de retención |
|---|---:|---:|---|
| OpenThoughts3 | 15.000 | 935.959.550 | Linaje de preguntas de Stack Exchange y otras fuentes upstream sin autorización individual acreditada |
| PubMed filtered | 20.000 | 494.056.484 | Verificar licencia en el artículo original, autores y derechos de terceros |
| DOAB | 50.000 | 359.365.617 | Comprobar licencia del libro y contenido de terceros, incluidas figuras |
| PressBooks | 33.736 | 302.342.385 | CC-BY por registro candidato; falta revisión de libro, autoría y material de terceros |
| Wikidata | 50.000 | 166.881.647 | CC0 declarado; pendiente auditoría de calidad, duplicados y contaminación |
| IFM Code-Reasoning | 12.000 | 169.084.387 | Procedencia y linaje del contenido incompletos |
| Common Corpus | 20.000 | 185.442.381 | Metadatos exactos de licencia; requiere comprobación de derechos por fuente |
| PT-BR Books Públicos | 10.000 | 128.837.168 | CC0 declarado; verificar obras, procedencia, OCR e idioma |

Otros lotes incluyen FineWeb-Edu, OpenWebMath, Cosmopedia, Aya, LibriSpeech y VoxPopuli. FineWeb/OpenWebMath permanecen en cuarentena por derechos de las páginas subyacentes; Cosmopedia v2 por linaje mixto; Aya por contenido de terceros y metadatos de idioma incompletos en la muestra; el resto sigue pendiente de auditoría global. El artefacto de muestras es un muestreo determinista, **no una aprobación humana**.

### Corrección del recolector

La próxima versión:
- escribe cada shard en `.partial` y solo lo publica tras superar el mínimo de filas;
- elimina temporales cuando falla una fuente;
- serializa fechas como ISO-8601 (el fallo de CourtListener se debió a un objeto `datetime`);
- conserva el split y todos los `metadata_fields` declarados;
- deja el umbral de escala como informativo: una adquisición parcial no debe aparecer como fallo técnico si los artefactos y manifiestos son válidos.

El inventario admitido no cambia: **260.971 documentos y 703.593.871 bytes**, 0,1407 % de 500 GB. No se suman candidatos ni parciales.


## Adquisición fragmentada y recuperación de interrupciones — 2026-11-09

La [run 42488804804](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42488804804) agotó el límite de seis horas durante el streaming secuencial (llegó a la configuración VoxPopuli de polaco). El workflow anterior solo publicaba artefactos al final, por lo que no dejó artefactos recuperables. **Admisiones de esa ejecución: 0 documentos / 0 bytes.**

El log del run registra 17 slices completos antes de la interrupción: **629.527 filas candidatas y 2.436.847.391 bytes JSONL escritos en el runner**. No se generó artefacto ni manifiesto final, por lo que esos archivos fueron efímeros y no son un lote recuperable. Tres slices se descartaron por quedar bajo su mínimo: LibreTexts (20.532/25.000), arXiv paper_text (6.650/50.000) y LibriSpeech train.clean.100 (21.038/25.000). No hay medición verificable de bytes remotos ni de un ZIP final para esa ejecución.

La adquisición se divide ahora en cuatro tranches deterministas de la lista de fuentes. La ejecución programada diaria procesa una tranche distinta según el día del año; cada fuente completada actualiza atómicamente el manifiesto y el artefacto de la tranche se intenta publicar incluso si el streaming posterior se interrumpe. Los registros siguen marcados como candidatos no admitidos; esto no supera revisión humana, derechos/procedencia, deduplicación cruzada ni G-0.

El inventario admitido permanece sin cambios: **260.971 documentos / 703.593.871 bytes**, equivalente al **0,1407 %** de 500 GB.

## Nuevo candidato multilingüe — EUR-Lex / CELLAR (2026-11-09)

Se incorpora a la cola de descubrimiento **EUR-Lex / CELLAR**, repositorio oficial de publicaciones de la Oficina de Publicaciones de la UE, para explorar actos jurídicos del Diario Oficial y terminología jurídica en las lenguas oficiales. CELLAR ofrece acceso público a metadatos y publicaciones mediante SPARQL y una API REST; la consulta y cada expresión deben congelarse con identificadores y hashes propios.

El aviso legal de EUR-Lex permite reutilizar documentos jurídicos para fines comerciales y no comerciales salvo condiciones específicas. No es una licencia universal: algunos documentos tienen condiciones especiales, y las obras de terceros o los datos de personas identificables pueden requerir autorización. Los metadatos son CC0-1.0; el contenido editorial, resúmenes y textos consolidados propiedad de la UE se indican bajo CC-BY-4.0. Se mantendrán como clases distintas y se excluirán los documentos con términos especiales o derechos no resueltos.

**Estado:** candidato de descubrimiento; 0 descargas, 0 filas candidatas y 0 bytes admitidos. Antes de staging se fijarán consulta SPARQL, timestamp, CELEX/ELI/CELLAR IDs, expresión por idioma, formato y SHA-256. No se habilita para train ni se altera el inventario admitido.

Fuentes primarias: [aviso legal EUR-Lex](https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en), [CELLAR](https://op.europa.eu/en/web/cellar), [knowledge graph/SPARQL](https://op.europa.eu/en/web/cellar/cellar-data/metadata/knowledge-graph) y [documentación CELLAR](https://op.europa.eu/en/web/cellar/documentation). El registro detallado y los controles están en `data/sources/registry.json`.


## Adquisición candidate-only — run 42737780473 (2026-11-10)

La [run 42737780473](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42737780473) completó la tranche determinista **2/4**. El estado `success` significa que terminó la adquisición y publicó el artefacto; no significa admisión ni autorización de entrenamiento.

| Fuente / configuración | Revisión inmutable | Filas | Bytes JSONL | SHA-256 del shard |
|---|---|---:|---:|---|
| HuggingFaceTB/cosmopedia · auto_math_text | `0ae6ec63f91742bd2d1eaef4f02232c55d719385` | 50.000 | 236.364.804 | `665be7e612ba8b38f7d3b125a886284d008f44f555f0fef37c8d1592719d06cf` |
| common-pile/pressbooks_filtered | `1a1d3b50d77f834370f8eb4c0d174668dd1676bb` | 33.736 | 302.949.633 | `ffcd8219132f154b6405259639b94987eaa05bb54fb0aca7bc562c433d967d74` |
| common-pile/oercommons_filtered | `506b6159dadcbc0dc67611cea024eedb04232fb2` | 3.828 | 28.787.310 | `5a10422434eca490390762263f3fd9c066fa7a1d75de088d2caa2fa3d2b12396` |
| facebook/voxpopuli · es | `42f01879c780b4a2e90ec0b4f616c2ece526e4f1` | 20.000 | 10.095.818 | `49e7df3161b06f307136d78502238c449dfb00015b0eccf78abd97392e589dc1` |
| facebook/voxpopuli · it | `42f01879c780b4a2e90ec0b4f616c2ece526e4f1` | 12.885 | 6.667.111 | `2c959d383306ead1d6d94c572c4315be93802e5bb314a7294d77ff492190b217` |
| common-pile/pubmed_filtered | `c156f0569a92d8f2edc33cebe1f72f7d3e1cae84` | 20.000 | 494.416.484 | `da8c11cfac2c6326e41119d3bd34e2d905b5987ffe84a7065bb8d56839e27e40` |
| IFM/Math-Reasoning · math-dialogue | `e249295774c3a66943e1483dbf53e0c811bc41dd` | 12.000 | 65.051.630 | `a82a4b22791bf751fa59f87b71c8eeb0b87f0d1cbdf86c2c519eea842120e5bd` |
| **Total candidato** | | **152.449** | **1.144.332.790** | |

El artefacto `heretic-open-source-candidates-42737780473-group-2` (ID `13737479716`) ocupa **397.069.719 bytes**; digest SHA-256 publicado por GitHub Actions: `22428d0ae88ac63b8fc0a6887126390f3372d485beea795f0afeb11a3b38f2c9`. Incluye el manifiesto y el directorio de staging; el SHA-256 propio del manifiesto no se ha recalculado en esta revisión y los hashes de shards proceden del manifiesto/log, no de una segunda extracción independiente. No hay medición fiable de bytes remotos ni de tamaño comprimido de las fuentes upstream.

**Slices fallidos y descartados:**
- Spanish-PD-Books: 954 filas utilizables frente al mínimo de 1.000; parcial descartado.
- Spanish-PD-Newspapers: falta `default/train/0041.parquet` en la revisión fijada; no se publicó shard.
- German Commons political: 0 filas utilizables frente al mínimo de 500; parcial descartado.

**Gates pendientes:** near-dedup entre fuentes, contaminación global de validation/test/benchmarks/holdout, G-0, revisión humana, privacidad/secretos/malware y derechos de upstream/terceros. La muestra automática fue de seis filas por fuente: no es aprobación humana ni cubre estratos independientes de dominio, idioma y formato. El filtro de adquisición actual solo rechaza patrones de email/teléfono; no equivale a un escáner completo de PII o secretos.

**Admisión del lote: 0 filas / 0 bytes.** No se marca `training_eligible`, no se modifica el corpus admitido y no se autoriza entrenamiento. El inventario sigue en **260.971 documentos / 703.593.871 bytes**, **0,1407 %** del objetivo decimal de 500 GB.

### Riesgo de almacenamiento del lote

El workflow sube `staging/open-source-candidates/` completo al artefacto de Actions, incluidos los shards brutos y material de muestra. Como el repositorio es público, los artefactos públicos no constituyen una cuarentena privada: GitHub documenta que los endpoints de artefactos de recursos públicos pueden utilizarse sin autenticación. El paso `review_candidate_samples.py` también imprime extractos brutos en los logs públicos de Actions. El artefacto y esos logs no son una cuarentena privada. No se ha borrado el artefacto ni se ha cancelado ningún workflow; antes de publicar nuevos payloads hay que separar manifiestos públicos de datos en cuarentena privada o limitar la publicación a fuentes cuyo derecho de redistribución esté acreditado.

## Nuevas fuentes investigadas — 2026-11-10 (solo descubrimiento)

- **Common Voice Scripted Speech v27.0:** 295 locales; metadata fijada en `common-voice/cv-dataset@65ca2460d5e686ea03902a932bbca09b322dc4b0`. Mozilla Data Collective lista los datasets como CC0-1.0, pero la línea de prompts incluye aportaciones de usuarios y texto importado; no se aceptará nada con procedencia Wikipedia/terceros o desconocida sin verificar derechos. Solo texto, sin audio ni metadatos demográficos/de hablante. Acceso MDC pendiente; 0 descargas y 0 bytes admitidos.
- **Tatoeba:** frases de texto bajo CC-BY-2.0-FR por defecto, con subconjunto CC0; exige atribuir al autor de cada frase. No hay snapshot inmutable ni descarga en esta ejecución. Traducciones no verificadas profesionalmente, posibles aportaciones copiadas y contenido ofensivo: requiere atribución por fila, filtro de derechos y partición por componentes de traducción. Audio excluido.
- **World Bank Open Knowledge Repository:** licencia mixta por obra. Solo se estudiarán ítems con CC-BY-4.0 o CC-BY-3.0-IGO exactas; NC/ND, términos desconocidos y componentes de terceros quedan fuera. Requiere atribución completa y avisos adicionales para traducciones/adaptaciones.
- **Parlamento Europeo:** se confirmó que las reglas institucionales de Open Data adoptan CC-BY-4.0, pero el candidato de discursos sigue pendiente de licencia a nivel de recurso, terceros y privacidad de metadatos de ponentes.

Los tres primeros registros nuevos permanecen como `candidate_discovery_only`, con `count_toward_admitted_bytes=false` y `training_authorized=false`. No se ha descargado ni admitido material de ellos.


### Corrección de publicación de candidatos — PR #30

La [PR #30](https://github.com/orbitalronin94/HERETIC-RONIN/pull/30) se integró en el commit [ca3fb47](https://github.com/orbitalronin94/HERETIC-RONIN/commit/ca3fb4714bbf94eb0cfe16b384ac04ef05cae3d6), validado por la [run 42830396419](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42830396419): compilación y suite de seguridad correctas, sin descargar datasets. En repositorios públicos, las futuras ejecuciones suben solo `OPEN-SOURCE-MANIFEST.json`; shards y muestras completos solo se publican si el repositorio es privado. El script de muestras deja de imprimir extractos en los logs y muestra únicamente recuentos. El trigger de push de adquisición queda limitado a `main`; los PR ejecutan solo validación.

La exposición histórica no desaparece: el artefacto [13737479716](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42737780473/artifacts/13737479716) figura con expiración **2027-02-08** en los metadatos de GitHub; los extractos también están en el log del job, pero su fecha exacta de retención no se ha verificado. No se han borrado artefactos ni cancelado workflows. La adquisición que ya se había disparado desde la rama antes de restringir el trigger ([run 42830186561](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42830186561)) continúa bajo la política de manifiesto público solamente; el push de `main` ([run 42830458157](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42830458157)) espera la exclusión mutua.


## Nuevo descubrimiento — Parlamento de Austria (2026-11-10)

Se incorpora a la cola de descubrimiento, **sin descarga ni admisión**, el dataset oficial de protocolos estenográficos del Nationalrat y Bundesrat:

- La página específica indica que los textos completos están disponibles en HTML desde la XX legislatura y que los discursos individuales están estructurados desde la XXVI.
- La misma ficha limita expresamente la condición de *freie Werke* a los protocolos estenográficos del Nationalrat y Bundesrat. Las listas de resultados y metadatos de la API están bajo CC BY 4.0; esa licencia no se extiende a otros materiales del portal.
- API de filtros documentada: `POST https://www.parlament.gv.at/Filter/api/filter/data/211?js=eval&showAll=true`.
- Idioma inicial: alemán. Tamaño, filas y bytes: **no medidos; 0 descargados y 0 admitidos**.
- Bloqueos antes de staging: congelar cuerpo exacto de consulta, respuesta, timestamp, IDs de sesión y SHA-256 por documento; revisar datos personales, citas/material de terceros, calidad y codificación; deduplicar contra todo el corpus y holdouts; superar G-0.
- No se ha asignado SPDX al texto: la fuente lo describe como obra libre bajo su régimen nacional; CC BY 4.0 se registra solo para metadatos/listas API.

Fuentes primarias: [ficha de protocolos](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/stenographische-protkolle/index.html) · [condiciones generales y catálogo](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/).
