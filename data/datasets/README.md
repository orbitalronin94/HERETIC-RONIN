# HERETIC-RONIN — biblioteca de datasets

Actualizado: 2026-11-27. Este documento distingue **admitido**, **candidato** y **cuarentena**. El tamaño descargado nunca equivale por sí solo a tamaño entrenable. La revisión manual de candidatos usa muestreo determinista estratificado por fuente, dominio, idioma y formato; los fragmentos nunca se imprimen en logs públicos.

## Resumen verificable

| Métrica | Valor |
|---|---:|
| Corpus base RONIN-IA admitido | 680.665.972 bytes |
| Cosmopedia v0.1 curada y admitida | 4.734 documentos · 22.927.899 bytes |
| Auditoría source-scoped combinada | 261.039 documentos examinados |
| Exclusiones exactas/near-duplicate | 68 extremos |
| Subconjunto resultante autorizado | 260.971 documentos |
| Total de bytes admitidos contabilizados | **703.593.871 bytes (671,0 MiB)** |
| Objetivo de biblioteca | 500.000.000.000 bytes (500 GB decimal) |
| G-0 global para nuevas admisiones | **BLOQUEADO**: falta inventario inmutable completo de todos los splits protegidos |
| Fuentes registradas | 114 (incluye DGT-Acquis y DGT-TM como discovery-only; JRC-Acquis queda bloqueado por conflicto de términos) |

Auditoría source-scoped: [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). Artefacto de auditoría: ID `13570263309`, SHA-256 `db826ced0bcd9158fee17d254faad203e7fe9e317f510e12fcf2cd448bb42dc9`.

La auditoría detectó 9 grupos/hits exactos y 68 pares SimHash. Los 68 índices excluidos están dentro del bloque base de 256.305 registros; los 4.734 documentos Cosmopedia permanecen en el subconjunto autorizado. No hubo coincidencias exactas con las 120 preguntas sintéticas de diagnóstico. Esto es una heurística de deduplicación y contaminación, no una prueba semántica ni un benchmark público.



**Bloqueo G-0 (revisión 2026-11-25).** La run [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447) es una auditoría *source-scoped*, no un G-0 completo. El script `scripts/audit_heretic_training_corpus.py` importa el artefacto train de RONIN-IA y solo los candidatos que se le suministran expresamente (en esa ejecución, Cosmopedia); no inventaría todos los splits validation/test/benchmark/holdout del corpus. Las 120 preguntas son un diagnóstico sintético, no el conjunto protegido completo. El `training_authorized=true` histórico solo se aplica a ese subconjunto exacto. **No se admite ninguna fuente nueva** hasta crear y auditar un manifiesto inmutable de todas las fuentes y todos sus splits protegidos.

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
- Auditoría source-scoped: [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447).

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
| Wikidata | 50.000 | 165.781.647 | Candidato CC0; falta muestra y auditoría source-scoped |
| Aya | 25.000 | 42.931.184 | Candidato Apache-2.0; falta revisión de privacidad/splits y auditoría source-scoped |
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
6. Ejecutar auditoría source-scoped y control de contaminación.
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

La última auditoría source-scoped del train combinado sigue siendo [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). Su alcance es el corpus train-only RONIN-IA y la tranche Cosmopedia v0.1 curada que se suministró expresamente; no autoriza ningún otro candidato.

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

El [run 42379525699](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42379525699) terminó después de conservar sus artefactos. El workflow marcó fallo porque no alcanzó su umbral de escala de 6.800.000.000 bytes; no fue una admisión ni una auditoría source-scoped.

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

Otros lotes incluyen FineWeb-Edu, OpenWebMath, Cosmopedia, Aya, LibriSpeech y VoxPopuli. FineWeb/OpenWebMath permanecen en cuarentena por derechos de las páginas subyacentes; Cosmopedia v2 por linaje mixto; Aya por contenido de terceros y metadatos de idioma incompletos en la muestra; el resto sigue pendiente de auditoría source-scoped. El artefacto de muestras es un muestreo determinista, **no una aprobación humana**.

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


## Nuevo candidato documental — Asamblea Nacional de Francia (2026-11-10)

Se registra el recurso oficial **`an-comptes-rendus`**, con los textos de debates de la XVII legislatura en XML y francés:

- La ficha del recurso describe actas de sesión con fechas, números de sesión, temas, oradores y textos.
- La página oficial del Hackathon 2026 identifica expresamente `an-comptes-rendus` y lo etiqueta como **Licence Ouverte / Open Licence**.
- El export actual de la ficha de debates está fechado **2026-11-06** y publica MD5 `a91c9d51574a8e89eb183a7bef74bf57`. Es una exportación mutable; aún no se ha descargado ni calculado SHA-256.
- La licencia enlazada por el portal es **Etalab Licence Ouverte v1.0**, no una licencia SPDX estándar. Se registra con el identificador local `LicenseRef-Etalab-Open-License-v1.0`. Permite adaptación y uso comercial con atribución, pero excluye datos personales salvo consentimiento, anonimización o base legal, y excluye derechos de terceros.
- Estado: candidato de descubrimiento. Filas y bytes **no medidos; 0 descargados y 0 admitidos**. Antes de staging hay que congelar el ZIP, verificar MD5/SHA-256, resolver datos personales y terceros, revisar muestras y ejecutar deduplicación/holdout/G-0.

Fuentes oficiales: [ficha Débats](https://data.assemblee-nationale.fr/travaux-parlementaires/debats) · [recursos Hackathon 2026](https://hackathon2026.assemblee-nationale.fr/) · [texto de Licence Ouverte v1.0](https://data.assemblee-nationale.fr/content/download/28755/file/Licence_Ouverte.pdf).


## Descubrimientos jurídicos y administrativos multilingües — 2026-11-11

### España — API de legislación consolidada del BOE

La API oficial ofrece legislación consolidada, sumarios BOE/BORME y tablas auxiliares. Se registra únicamente el endpoint de **legislación consolidada**, no los sumarios BORME ni la Biblioteca Jurídica Digital.

- Las condiciones de reutilización aprobadas por resolución de 27-06-2024 permiten uso comercial/no comercial, reproducción, distribución, adaptación y obras derivadas con atribución.
- La licencia es un conjunto de condiciones propio, no una entrada SPDX; se registra como LicenseRef-BOE-Reuse-2024.
- La página legal excluye obras de la Biblioteca Jurídica Digital —CC BY-NC-ND 4.0 salvo indicación distinta— y elementos de terceros; algunos documentos pueden tener condiciones especiales.
- Cada texto consolidado debe presentarse como informativo, no como publicación oficial. Deben conservarse la atribución BOE y la fecha de actualización.
- Estado: candidato de descubrimiento; 0 descargas, 0 filas medidas y 0 bytes admitidos. La API es mutable y requiere snapshot, XSD, IDs y SHA-256 antes de staging.

Fuentes oficiales: [API de datos abiertos](https://www.boe.es/datosabiertos/api/api.php) · [condiciones de reutilización](https://www.boe.es/informacion/aviso_legal/index.php) · [FAQ de legislación consolidada](https://www.boe.es/datosabiertos/faq/consolidada.php).

### Francia — API Légifrance / DILA

La API estable, abierta el 04-04-2023, somete los datos a Licence Ouverte / Etalab 2.0 y a las CGU de PISTE y de la propia API. Las CGU API indican que se permite uso comercial, pero requieren registro, OAuth y respeto a los límites de uso.

- Se registra como LicenseRef-Etalab-Open-License-2.0, no como SPDX estándar.
- La primera selección futura se limitaría a textos legislativos, códigos y reglamentos bajo responsabilidad de DILA.
- Jurisprudencia y decisiones judiciales quedan excluidas inicialmente por riesgos de datos personales, terceros y pseudonimización.
- La API advierte que sus datos no son jurídicamente oponibles y que puede haber errores o falta de actualización.
- Estado: candidato de descubrimiento; 0 descargas, 0 filas medidas y 0 bytes admitidos. Falta acceso PISTE autorizado, snapshot inmutable y G-0.

Fuentes oficiales: [Open data y API](https://www.legifrance.gouv.fr/contenu/pied-de-page/open-data-et-api) · [CGU de la API (15-12-2022)](https://www.legifrance.gouv.fr/contenu/Media/files/pied-de-page/cgu-legifrance-api-vf-15-12-2022_0.pdf) · [Licence Ouverte 2.0](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf).

### Fuentes investigadas y bloqueadas

- **Deutscher Bundestag:** ofrece Plenarprotokolle y Drucksachen en XML/JSON para procesamiento, pero la página oficial consultada no acredita una licencia explícita del payload. Bloqueado; no se infiere permiso comercial de la etiqueta “Open Data”.
- **GovInfo (EE. UU.):** 17 U.S.C. §105 cubre obras del Gobierno federal preparadas por empleados en sus funciones, pero GovInfo advierte que publicaciones oficiales pueden contener material de terceros protegido. Además, esa regla estadounidense no resuelve por sí sola el alcance territorial en España/UE. Bloqueado hasta revisión territorial y clearance por documento.

Fuentes: [Bundestag Open Data](https://www.bundestag.de/services/opendata) · [GovInfo copyright policy](https://www.govinfo.gov/about/policies) · [17 U.S.C. §105](https://www.copyright.gov/title17/92chap1.html).

## Adquisición parcial más reciente — run 42976034496 (2026-11-11)

[Run de GitHub Actions](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42976034496) — grupo 0/4; terminó cancelado al alcanzar el límite de 360 minutos.

| Fuente | Filas candidatas en runner | Bytes JSONL | SHA-256 del shard |
|---|---:|---:|---|
| FineWeb-Edu, revisión 87f09149ef4734204d70ed1d046ddc9ca3f2b8f9 | 100.000 | 428.092.222 | 021a35da979813fa7cf2b270a7bbc77c0673420e9ed21bc948e4a269e7bc0d77 |
| Aya, revisión f9ea04583f02a8f86404ff6c58bf75fe637df8a2 | 25.000 | 46.109.328 | 9a8633c336389bd555e71d26646a908f2834416025d3e1b0bd7e20d00216da43 |
| VoxPopuli alemán, revisión 42f01879c780b4a2e90ec0b4f616c2ece526e4f1 | 20.000 | 9.857.291 | 269d88fd53e7841f9f7f1cdd9136bd496b28c5ed70032f071cf316a9f21e2c9c |
| **Total** | **145.000** | **484.058.841** | — |

- 71.526 filas fueron rechazadas por los filtros de adquisición aplicados; dos slices fallaron y descartaron sus archivos parciales: arXiv obtuvo 6.650 filas utilizables frente a un mínimo de 50.000; LibriSpeech train.clean.100 obtuvo 21.038 frente a 25.000.
- El manifiesto informa 145.000 filas y 484.058.841 bytes JSONL, pero son resultados escritos en el runner efímero. El repositorio es público y el workflow subió únicamente el manifiesto: **payload retenido = 0 bytes**.
- Artefacto manifiesto: [13856681975](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42976034496/artifacts/13856681975), 2.190 bytes; SHA-256 del ZIP 94863a5c62a333e2bb7fe94389e332ba0d237f7d8211264e23cc739815694587; SHA-256 del JSON interno b9fd726daa029e64edb8dcf1642c36d71a950506b2e1bba1d6a7ad5a1ef9c8d8.
- Los hashes de shards están declarados en el manifiesto, pero no pudieron recalcularse contra los payloads porque no se conservaron.
- Near-dedup global, contaminación de holdout, G-0, auditoría humana estratificada, PII/secretos y malware: pendientes o no completados. No es admisión.

El run 42925046806 (grupo 1/4) produjo 352.000 filas / 1.463.172.254 bytes JSONL y un artefacto de manifiesto de 3.923 bytes. Reprodujo exactamente las revisiones, conteos, bytes y hashes de run 42841334250; es una repetición, no crecimiento acumulado. Ambos dejaron 0 bytes admitidos y 0 bytes de payload retenido.

**Balance global sin cambios:** 260.971 documentos y 703.593.871 bytes admitidos; 0 nuevas admisiones. Progreso sobre 500 GB: 0,141 %.


## Descubrimientos nórdicos — 2026-11-11

### Noruega — Stortinget Open Data API

La fuente primaria del Stortinget ofrece datos del procedimiento parlamentario —preguntas, asuntos, reuniones, votaciones, audiencias y publicaciones— en XML/JSON. Sus condiciones remiten a la versión vigente de la Norsk lisens for offentlige data; el enlace oficial conduce a NLOD 2.0.

- NLOD 2.0 permite copiar, modificar, combinar, redistribuir y usar comercialmente, con atribución y sin presentar los datos de forma engañosa.
- La licencia excluye datos personales sin base jurídica, información confidencial, derechos de terceros que el licenciante no pueda conceder y otras IP como marcas.
- Se registra como LicenseRef-NLOD-2.0; no se presupone un identificador SPDX.
- La API limita las llamadas a 100 por minuto y solo muestra la versión vigente del servicio/documentación.
- Estado: candidato de descubrimiento; 0 descargas, 0 filas medidas y 0 bytes admitidos. Primera selección limitada a preguntas, asuntos, agendas, votaciones y publicaciones oficiales; excluidos endpoints de personas/biografías/fotos, listas de oradores, aportaciones a audiencias y contenido de terceros.

Fuentes oficiales: [Stortinget Open Data](https://data.stortinget.no/) · [condiciones de uso](https://data.stortinget.no/om-datatjenesten/bruksvilkar/) · [API y XML](https://data.stortinget.no/dokumentasjon-og-hjelp/) · [NLOD 2.0](https://data.norge.no/nlod/no/2.0).

### Dinamarca — Folketinget Open Data (bloqueado para actas)

El catálogo OData v3 ofrece XML/JSON y contiene actas de debates en XML. Las condiciones generales conceden uso comercial y adaptación de los datos del catálogo; sin embargo, las actas tienen cláusulas especiales:

- Los borradores pueden revisarse varias veces sin que cada cambio quede marcado; debe conservarse y comunicarse si el acta es provisional o definitiva.
- Para las actas se concede expresamente un derecho de reproducción, se reserva al titular originario el derecho exclusivo de publicar colecciones de sus propias intervenciones y se limita la modificación a lo necesario para el uso permitido.
- Los PDFs, imágenes y otros documentos enlazados no forman parte en general de los datos abiertos; las obras de terceros incluidas en anexos conservan sus propios derechos.
- Estas cláusulas necesitan interpretación jurídica antes de extraer, normalizar, tokenizar, agregar o entrenar con los textos.

Estado: bloqueado, sin descarga ni staging. No se interpreta la licencia general como autorización automática para transformar las actas en un corpus de entrenamiento.

Fuentes oficiales: [Open Data y condiciones](https://www.ft.dk/dokumenter/aabne_data) · [portal OData](https://oda.ft.dk).



## Adquisición de candidatos — 2026-11-12 (run 88, grupo 5/8)

[Run 43176267906](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43176267906) terminó con éxito en el commit `a75fb8d35d099efa04353918ee7b73ad2a65cc75`. El éxito significa que terminó la adquisición, no que se haya admitido material.

- Filas candidatas escritas por el runner: **170.000**.
- Bytes JSONL escritos en el runner: **462.861.425**.
- Filas filtradas/rechazadas por el recolector: **283.379**.
- Fuentes completadas: 4; fallos no fatales: 1.
- Bytes remotos anunciados/descargados y bytes comprimidos originales: **no medidos**.
- Payload durable retenido: **0 bytes**; staging durable: **0 filas / 0 bytes**.
- Admisión nueva: **0 filas / 0 bytes**.

| Fuente | Revisión inmutable | Config/split | Filas | Bytes JSONL efímeros | SHA-256 reportado por el runner |
|---|---|---|---:|---:|---|
| philippesaade/wikidata | `3c43a705de25f60268a1ef343098d3c3464706c7` | default/train | 50.000 | 167.781.647 | `ad779639abb79cc5454040301c245ca688bcc86772bb88283b3022be3b7e1e5d` |
| openslr/librispeech_asr | `71cacbfb7e2354c4226d01e70d77d5fca3d04ba1` | all/train.clean.360 | 50.000 | 21.708.974 | `5222e62edd4d73053f6ede7a76214a9ef81de8e92fd3f0eb9d3de2d3baf1c47e` |
| common-pile/data_provenance_initiative_filtered | `8f5afcf585e4618ff12f5b6d49cb5242faf5afbd` | default/train | 50.000 | 87.100.950 | `35199be7ec9e6126b3e484c0c9aaf52ffc6d0598a41727359b0f0ea0a5f236c3` |
| PleIAs/common_corpus | `307910e4c5d040d6f318e6edf2a2b97849155771` | default/train | 20.000 | 186.269.854 | `d53b2571fe117cb93113e99c2683c7d4fa3db6c47629d4130803636d46e68b99` |
| coral-nlp/german-commons | `d12379bba6ecdc525958ebe6e182f9cb905a06e2` | political/btdrucksachen | 0 | 0 | — |

Los hashes de shards son los calculados y registrados por el script en el manifiesto; **no se pudieron recalcular contra los shards** porque el runner fue efímero y el repositorio público solo conserva el manifiesto. El hash del artefacto y el del JSON interno sí se verificaron después de descargarlo:

- Artefacto [13923729490](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43176267906/artifacts/13923729490): ZIP de 2.721 bytes; SHA-256 `87b93844e6b74ee1eb23468d86055e588e0c142510cf26ee905d3342fccf3626`.
- `OPEN-SOURCE-MANIFEST.json`: 8.771 bytes; SHA-256 `3f1fa4f320b866dcb85ef7910b7d78646f7bcf97ae36daf4108836c479ea1a83`.

**Controles pendientes:** la adquisición usó train-only, deduplicación exacta dentro de cada fuente, filtro de longitud y patrones básicos de email/teléfono. No ejecutó near-dedup global, comparación contra todos los holdouts, G-0, revisión humana real, escaneo integral de PII, secretos o malware. Se generaron seis muestras de reservoir por fuente, pero solo se publicaron sus recuentos; no hay muestras disponibles para revisión humana. Los filtros por licencia se aplicaron en origen donde estaban configurados, pero no sustituyen la verificación independiente de cada upstream y componente de terceros.

- Wikidata: etiqueta oficial CC0-1.0 verificada; pendientes privacidad, calidad y deduplicación global.
- LibriSpeech: etiqueta CC-BY-4.0 verificada; pendiente revisión de procedencia de los textos transcritos y calidad.
- Data Provenance Initiative: allowlist por registro aplicada; siguen pendientes errores de metadatos, posibles casos de license laundering y derechos upstream.
- PleIAs Common Corpus: allowlist exacta de nombres aplicada; no hubo etiqueta oficial de licencia del Hub y falta revisar cada obra/origen y sus componentes.
- German Commons `btdrucksachen`: cero filas utilizables; shard parcial descartado.

Este lote queda **held / ephemeral / not retained**, no staged durable y no training-eligible. No se suman sus 462.861.425 bytes al total admitido.

## Nuevos descubrimientos jurídicos — 2026-11-12

### ILO Research Repository — candidato discovery-only

La política oficial de la OIT establece CC BY 4.0 por defecto para publicaciones producidas desde el 3 de mayo de 2023, salvo indicación distinta; la página de copyright de cada obra controla. Excluye componentes de terceros. Los trabajos anteriores no quedan cubiertos automáticamente; las fotografías son mayoritariamente CC BY-NC-ND y el audio/vídeo suele ser CC BY-ND. El portal de investigación declara 18.392 activos, pero esa cifra es dinámica y no equivale a documentos elegibles. No se ha identificado aún un contrato de export/API reproducible. [Derechos OIT](https://www.ilo.org/rights-and-permissions) · [Research Repository](https://researchrepository.ilo.org/esploro/).

### Australia — Federal Register of Legislation — candidato discovery-only

La página oficial declara CC BY 4.0 para el contenido del registro salvo el Commonwealth Coat of Arms y los elementos expresamente exceptuados; permite adaptación y uso comercial con atribución. Exige indicar la fecha completa de descarga y si se modificó el contenido. Los derechos de terceros quedan fuera. Hay excepciones por instrumento: F2014L01500 declara CC BY-NC 4.0 y debe excluirse. [Términos oficiales](https://www.legislation.gov.au/terms-of-use) · [OPC — Federal Register](https://www.opc.gov.au/FRL).

### Canadá — Justice Laws bulk XML — bloqueado

El catálogo de Open Government Portal etiqueta el paquete bulk XML con OGL Canada 2.0. Sin embargo, el Reproduction of Federal Law Order SI/97-5 permite expresamente reproducir legislación federal sin permiso, pero no dice expresamente que permita adaptarla. La relación entre la licencia del catálogo y el payload, y el alcance para transformaciones de entrenamiento, no está resuelta. No descargar hasta aclararlo. [Dataset XML](https://open.canada.ca/data/en/dataset/2f4bb174-b2e7-4fb2-a7a1-a313507acbc6) · [OGL Canada](https://open.canada.ca/en/open-government-licence-canada) · [SI/97-5](https://laws-lois.justice.gc.ca/PDF/SI-97-5.pdf).


## Adquisición fallida de artefacto — 2026-11-11 (run 87, grupo 6/8)

[Run 43090663647](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43090663647) generó candidatos, pero terminó en **failure** porque `actions/upload-artifact@v7` devolvió HTML donde esperaba JSON y agotó cinco reintentos. No hubo artefacto ni manifiesto durable.

| Fuente | Revisión | Config/split | Filas | Bytes JSONL efímeros | SHA-256 reportado en el log |
|---|---|---|---:|---:|---|
| common-pile/pressbooks_filtered | `1a1d3b50d77f834370f8eb4c0d174668dd1676bb` | default/train | 33.736 | 302.949.633 | `ffcd8219132f154b6405259639b94987eaa05bb54fb0aca7bc562c433d967d74` |
| facebook/voxpopuli | `42f01879c780b4a2e90ec0b4f616c2ece526e4f1` | es/train | 20.000 | 10.095.818 | `49e7df3161b06f307136d78502238c449dfb00015b0eccf78abd97392e589dc1` |
| common-pile/pubmed_filtered | `c156f0569a92d8f2edc33cebe1f72f7d3e1cae84` | default/train | 20.000 | 494.416.484 | `da8c11cfac2c6326e41119d3bd34e2d905b5987ffe84a7065bb8d56839e27e40` |

Total: **73.736 filas / 807.461.935 bytes JSONL** en el runner. El recolector filtró 99.635 filas. Fallos parciales descartados: PleIAs Spanish-PD-Books (954 filas utilizables frente a un mínimo de 1.000) y German Commons `germanpoliticalspeeches` (0 frente a 500). Los bytes remotos/comprimidos no se midieron.

Los hashes de shards proceden del log; no se pueden recalcular porque los archivos se perdieron con el runner efímero. El artefacto de manifiesto tampoco se creó. Payload durable retenido: **0 bytes**; staging durable: **0 bytes**; admisión: **0 filas / 0 bytes**. Las muestras solo se resumieron en logs; no hubo revisión humana. El fallo no habilita reintentos de admisión ni permite contar los bytes efímeros.

## Actualización de curación — 2026-11-13 (runs 92–93)

**Admisiones nuevas: 0.** El total acumulado sigue en **703.593.871 bytes** y 260.971 documentos según la última auditoría source-scoped verificada (run [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447)). Progreso hacia 500.000.000.000 bytes: **0,140719 %**. Ningún byte de los lotes siguientes se suma al total.

- [Run 92](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43298985874), grupo 7/8: 35.000 filas y 945.924.928 bytes JSONL producidos en el runner. VoxPopuli inglés: 20.000 filas, 9.695.378 bytes, SHA-256 `16d055db8451e1f247907265f38b5835d00f766e1cf9193438c93792d29a159f`. OpenThoughts3: 15.000 filas, 936.229.550 bytes, SHA-256 `c23a18348f6478acac2ed0549df655a1c3f433d6f6763d93e9892e877f3228a9`. LibreTexts (20.532/25.000) y PleIAs Spanish-PD-Books (978/1.000) se descartaron por debajo del mínimo. Artifact de manifiesto [13983600253](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43298985874/artifacts/13983600253), 1.938 bytes, SHA-256 `adc350c45bf60c66e1e35f62dcbc0fb449aad312ddc2e8bcf1d72983f9c98ebd`; JSON interno 5.372 bytes, SHA-256 `c4d9055db2c098b1f05c6333c60df18636f74e125d65e7ea7ba57881c6296645`.
- [Run 93](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43383222519), grupo 6/8: 73.736 filas y 807.461.935 bytes JSONL producidos en el runner. PressBooks: 33.736 filas / 302.949.633 bytes; VoxPopuli español: 20.000 / 10.095.818; PubMed: 20.000 / 494.416.484. PleIAs Spanish-PD-Books (954/1.000) y German Commons speeches (0/500) se descartaron. Los tres shards correctos tienen exactamente los mismos SHA-256, conteos y bytes que run 87; run 93 es una repetición, con **0 filas y 0 bytes candidatos únicos nuevos**. Artifact de manifiesto [14018112522](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43383222519/artifacts/14018112522), 2.292 bytes, SHA-256 `79b3e47ad7467370f611b979bd7294a1022f6f114eca6ce4b59d075218965129`; JSON interno 7.287 bytes, SHA-256 `59e692299981eca4403fa3836b7f1c4e38469315286e41620f0fd35055710d77`.

En ambos runs: bytes remotos y comprimidos no medidos; 0 bytes retenidos, 0 staged y 0 admitidos. Los hashes de shards proceden del manifiesto y no se pudieron recalcular sin recuperar los payloads. La deduplicación aproximada global, contaminación de holdout, revisión humana, privacidad/secretos/malware y G-0 siguen pendientes.

### Fuentes descubiertas

- **Eurostat** — candidata discovery-only. Reutilización comercial de datos estadísticos, metadatos, publicaciones y herramientas con atribución, pero con excepciones para datos de terceros, co-publicaciones, determinados países y datos comerciales específicos. El API SDMX/JSON-stat/TSV no conserva versiones históricas: cada adquisición futura tendrá que fijar consulta, dataflow, DSD, codelists, timestamp y SHA-256. La web oficial anunció mantenimiento de servicios/API el 13/11/2026 de 14:00 a 23:00 CET; no se descargó nada.
- **OECD written content** — candidata discovery-only, limitada inicialmente a obras publicadas desde 2024-07-01 con CC-BY-4.0 confirmada en la página de copyright de cada obra. Se excluyen excepciones, co-publicaciones y material de terceros; el catálogo y la política no bastan para admitir un documento.
- **OpenThoughts3** queda en estado held y desactivado en el recolector: el tag Apache-2.0 del dataset agregado no resuelve los derechos de todas las preguntas upstream. No se volverá a descargar hasta tener un allowlist por fila y revisión de licencias/procedencia.

### Correcciones operativas

La rotación anterior `day_of_year + slot` repetía grupos y no repartía uniformemente las ocho tranches. Se cambia a `((day_of_year - 1) * 4 + slot) % 8`, que cubre los ocho grupos exactamente una vez por cada ciclo de 48 horas. La adquisición ya no se dispara por `push`; los PR ejecutan validación solamente.

El repositorio es público. El workflow exige el secreto Actions `HERETIC_STAGING_PASSPHRASE` antes de descargar payloads; si falta, publica un manifiesto `blocked_storage_gate` de cero bytes y no descarga. Si existe, cifra el paquete con GPG AES-256 e integridad antes de publicar el artefacto público; los payloads en claro se borran del runner. Los artefactos tienen retención de 90 días. No se ha creado ni modificado ningún secreto.


**Fortaleza del secreto de staging:** en repositorios públicos el workflow solo descarga si `HERETIC_STAGING_PASSPHRASE` tiene al menos 32 caracteres; GPG usa AES-256, SHA-512 S2K y control de integridad. Sin ese mínimo, el lote se bloquea antes de descargar.


## Actualización de curación — 2026-11-14 (run 102)

**Admisiones nuevas: 0.** La última ejecución programada [43568604566](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43568604566) terminó correctamente en el paso de preflight, pero el gate de almacenamiento bloqueó la descarga antes de contactar fuentes: el repositorio es público y HERETIC_STAGING_PASSPHRASE estaba ausente o era demasiado corto.

- Grupo: 5/8. Filas candidatas: **0**; bytes remotos/descargados/comprimidos: **no medidos**; JSONL generado: **0 bytes**; staging durable: **0 filas / 0 bytes**; payload retenido: **0 bytes**; admisión: **0 filas / 0 bytes**.
- Artefacto de manifiesto [14103293875](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43568604566/artifacts/14103293875): ZIP 653 bytes, SHA-256 88c9315417f8f9cb6531c0ed8df6b7b9bb79d240bae86163c94bef75753fb5da. JSON interno 871 bytes, SHA-256 0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7. El manifiesto declara blocked_storage_gate, payload_downloaded=false y training_authorized=false.
- **EuroVoc 4.24**: candidato discovery-only, 24 lenguas oficiales de la UE más albanés, macedonio y serbio. Las distribuciones archivadas de 2020 constan como CC0-1.0, pero la licencia de la distribución actual 4.24 debe confirmarse en su ficha exacta; no se ha descargado.
- **HUDOC / TEDH**: bloqueado por términos no comerciales. La reproducción de textos se limita a uso privado o información/educación relacionada con el Tribunal, sin cobro; cualquier otro uso, especialmente comercial, exige permiso previo escrito. No se ha descargado.

Total acumulado sin cambios: **703.593.871 bytes / 260.971 documentos**, progreso **0,140719 %** de 500 GB. El éxito del workflow solo confirma que el bloqueo se registró correctamente; no es una adquisición ni una admisión.


## Revisión de derechos — EEA Datahub y FAO (2026-11-14)

- EEA Datahub: dos registros WISE (Nutrients 2025 y WEI+ 2023) muestran CC-BY 4.0 con EEA como titular en sus metadatos. Siguen como candidatos: falta trazar derechos de los datos nacionales/upstream, fijar distribuciones y hashes, auditar calidad y superar G-0. No se adquirió ningún payload.
- FAO Publications: bloqueado por los términos por defecto no comerciales y la exigencia de permiso para reproducciones/adaptaciones. No descargado.
- Resultado: **0 admisiones nuevas / 0 bytes**. Ninguno de los dos registros es training_eligible.


- [Run 101](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43496984977), grupo 3/8: el preflight bloqueó antes de descargar por falta de HERETIC_STAGING_PASSPHRASE (mínimo 32 caracteres). 0 filas, 0 bytes remotos/descargados/comprimidos medidos, 0 staged y 0 admitidos. Artefacto [14071464119](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43496984977/artifacts/14071464119): ZIP 653 bytes, SHA-256 cddd161c01910852db6083f15ed157b2b4c6e2ad38308fa5ddc070b9767205b6; JSON interno 871 bytes, SHA-256 2829acd2e3d3d88cd5d58aa573fff9cfc9c9067d45dc1035e09e1c190c488b26. Hash del ZIP recalculado localmente y coincidente con GitHub; no hubo payload ni shards.


## Revisión de curación — 2026-11-15

**Admisiones nuevas: 0.** Se añadieron dos fuentes a discovery-only, sin descarga:

- legislation.gov.uk: OGL-UK-3.0 para el texto legislativo cubierto por el aviso del sitio; excluir excepciones, datos personales y derechos de terceros. El material derivado de EUR-Lex se separa y no se cuenta aquí. Preservar atribuciones de Westlaw/British History Online, versiones/fechas y XML exacto.
- Registro público del Consejo de la UE: Decision (EU) 2017/1842 cubre documentos públicos producidos/held por el Consejo para reutilización comercial y no comercial, con atribución y sin distorsión; quedan pendientes condiciones por documento, adaptación/training, privacidad, derechos de terceros y seguridad.

Ambas entradas tienen `training_authorized=false`, `count_toward_admitted_bytes=false`, sin filas ni bytes medidos.

[Run 43687908071](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43687908071), grupo 1/8, quedó bloqueado en preflight por falta de `HERETIC_STAGING_PASSPHRASE` de al menos 32 caracteres. No contactó las fuentes ni descargó payload. Manifiesto [14150964444](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43687908071/artifacts/14150964444): ZIP SHA-256 `a2bea5f0df4fdf616328872d3774265066685b7afea70ade5ef5db260dfc516d`; JSON interno SHA-256 `5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437`.

Total acumulado verificado sin cambios: **703.593.871 bytes / 260.971 documentos**, **0,140719 %** de 500 GB. No se suman candidatos, artefactos ni bytes efímeros.


## Curación 2026-11-15 — European Parliament Think Tank / EPRS

- Añadido **European Parliament Think Tank / EPRS** como candidato discovery-only, limitado a publicaciones cuya propia página indique expresamente CC-BY-4.0 y titularidad de la Unión Europea. Hay ejemplos verificables en publicaciones de 2025 y 2026 sobre derechos de autor/IA y retención de datos. El aviso legal general del Parlamento no se trata como una licencia CC-BY universal: cada obra debe revisarse, y figuras, tablas, citas y anexos de terceros se excluyen salvo autorización independiente.
- Se preservarán código EPRS, autoría, fecha, DOI/ISBN, idioma, página de copyright, PDF/HTML exacto y SHA-256. Sin descarga ni bytes medidos en esta ejecución.
- El candidato permanece `training_authorized=false` y `count_toward_admitted_bytes=false`; faltan revisión de cada obra, terceros, privacidad, muestras y G-0.


## Curación — 2026-11-16

### Open Research Europe — candidato discovery-only

La plataforma cubre ciencias naturales, ingeniería y tecnología, medicina, agricultura/veterinaria, ciencias sociales y humanidades. Sus artículos se publican bajo CC BY; la versión exacta de la licencia puede cambiar y se muestra bajo el resumen. Se registrará como `CC-BY-4.0` únicamente cuando la página individual indique expresamente esa versión. El copyright permanece con el autor o su institución. Los datos asociados pueden estar bajo CC0/CC BY, pero son activos separados. [Política editorial](https://ore.eu/editorial-policies/) · [Cómo publica](https://ore.eu/how-publishing-works) · [Guía de artículos](https://ore.eu/article-guidelines).

**Estado:** no descargado, filas y bytes desconocidos. Exigir DOI y versión inmutable, copyright page, autores, revisión por pares completada y aprobada, historial de versiones, revisión de terceros, privacidad/consentimiento, integridad, calidad, muestra humana, deduplicación global y G-0. Excluir material retracted/withdrawn, revisión pendiente o no aprobada, editorial notes sin resolver y suplementos/figuras de terceros sin licencia propia. `training_authorized=false`; `count_toward_admitted_bytes=false`.

### Run 117 — 2026-11-16

[Run 43821600133](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43821600133), grupo 5/8: el preflight bloqueó antes de descargar porque el secreto `HERETIC_STAGING_PASSPHRASE` no estaba presente o tenía menos de 32 caracteres. 0 filas; bytes remotos/comprimidos no medidos; 0 bytes descargados, JSONL, staged, retenidos o admitidos. Manifiesto [artifact 14204298738](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43821600133/artifacts/14204298738), 653 bytes. SHA-256 informado por metadatos de GitHub: `48650002b2d9f35b79cfb96df40186235259ce507596d35681489879abd7ca0f`; no se descargó el ZIP para recalcularlo en esta ejecución. El manifiesto no tiene hash interno verificado. El éxito del run solo acredita que el bloqueo se registró correctamente.

Total admitido sin cambios: **703.593.871 bytes / 260.971 documentos**; **0,140719 %** de 500 GB. Nuevas admisiones: **0 documentos / 0 bytes**.


## CORDIS — 2026-11-16, candidato discovery-only

**Alcance limitado:** noticias y *Thematic Packs* editoriales demostrablemente propiedad de la UE, con aviso de reutilización CC-BY-4.0 aplicable al elemento. La política del sitio se basa en la Decisión 2011/833/UE; esta no cubre documentos con derechos de terceros, acceso privilegiado, datos confidenciales, patentes/marcas ni ciertos proyectos de investigación no publicados. Los materiales de beneficiarios de programas de la UE se rigen por las condiciones de la subvención, no por la licencia editorial general. [Aviso legal](https://cordis.europa.eu/about/legal) · [Decisión](https://eur-lex.europa.eu/eli/dec/2011/833/oj/eng).

La interfaz ofrece seis idiomas (ES/DE/EN/FR/IT/PL), pero la disponibilidad de cada artículo debe verificarse; conservar el idioma original y excluir traducciones automáticas hasta revisar los términos de eTranslation. Excluir datos de contacto de participantes y elementos multimedia/de terceros sin permiso independiente. No descargado: filas y bytes desconocidos; `training_authorized=false`; `count_toward_admitted_bytes=false`. G-0, privacidad, revisión humana y deduplicación global pendientes.


## Curación y descubrimiento — 2026-11-17

### PLOS — candidato discovery-only

Se incorpora PLOS únicamente como candidato para artículos de investigación cuya propia página identifique expresamente **CC-BY-4.0**. La política actual de PLOS permite reutilización comercial y minería de artículos bajo CC BY 4.0 u otras licencias comparables, pero el registro adopta una allowlist más estricta: solo CC-BY-4.0 exacta por artículo. Los autores conservan el copyright y la atribución debe identificar autor y fuente. Las figuras, tablas, imágenes, mapas, audio/vídeo, protocolos, código, citas y datasets de terceros pueden tener derechos separados y no heredan automáticamente la licencia del artículo. [Licencias y copyright](https://journals.plos.org/plosone/s/licenses-and-copyright) · [Text and Data Mining](https://api.plos.org/text-and-data-mining.html).

La adquisición futura deberá usar el Solr Search API/JATS XML documentado, con un máximo de 100 filas por petición, 10 peticiones por minuto, 300 por hora y 7.200 por día; no se permite sustituirlo por scraping masivo de HTML/PDF. Cada DOI/version y payload exacto se fijará con URL, autores, copyright holder, fecha, aviso de licencia, timestamp UTC, bytes y SHA-256. Se excluyen artículos con derechos ambiguos, componentes de terceros no autorizados, datos clínicos/personales no despejados, retracted/withdrawn/removed y versiones superadas. El candidato queda training_authorized=false, count_toward_admitted_bytes=false; no se descargó.

### Runs 120 y 121 — preflight de almacenamiento

- [Run 120](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43970081452), grupo 7/8: blocked_storage_gate; 0 filas, 0 bytes JSONL/descargados/staged/admitidos. Solo manifiesto de 871 bytes dentro de ZIP de 653 bytes. Artifact [14276384265](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43970081452/artifacts/14276384265): ZIP SHA-256 5ccaf40cebdf09513fe878878c686cd2c3e51307e81877c75db01e48ed52899b; JSON SHA-256 3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992.
- [Run 121](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44045933438), grupo 1/8: mismo bloqueo antes de descargar; 0 filas y 0 bytes de payload. Solo manifiesto de 871 bytes dentro de ZIP de 653 bytes. Artifact [14312065087](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44045933438/artifacts/14312065087): ZIP SHA-256 bd558141f5e6d4f3375aaba4fea21c00a0b70733c9bfeea2d0711c70c1a6e046; JSON SHA-256 5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437.

Ambos ZIP y JSON se descargaron y sus hashes se recalcularon independientemente; los hashes ZIP coinciden con el digest de GitHub. El manifiesto de cada run confirma payload_downloaded=false, training_authorized=false y total_rows=0. Los bytes remotos y comprimidos no se midieron porque no hubo petición de payload. Los jobs de instalación/adquisición se omitieron por el gate; el workflow terminó correctamente al registrar el bloqueo.

**Balance:** 0 admisiones nuevas. Total acumulado sin cambios: **703.593.871 bytes / 260.971 documentos**, **0,140719 %** de 500 GB, según la auditoría source-scoped [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). No se suman candidatos, manifiestos ni tamaños de artefacto.


## Curación y adquisición — 2026-11-18

### WIPO Publications — candidata, no admitida

Se incorpora como candidata únicamente la publicación individual cuya propia página de copyright declare **CC-BY-4.0** y confirme que WIPO es titular. La política general de acceso abierto de WIPO establece CC BY 4.0 para muchas publicaciones nuevas, pero contempla excepciones; la licencia del portal no sustituye el aviso de cada obra. Ejemplos con aviso individual explícito: *WIPO IP Facts and Figures 2024* (DOI 10.34667/tind.57723), *World Intellectual Property Report 2024* (DOI 10.34667/tind.49284) y *A Primer on Technology Transfer in the Field of Biotechnology* (2025; DOI 10.34667/tind.50126). Se excluyen emblemas, logotipos, figuras/fotografías y demás material de terceros sin autorización independiente. No se ha descargado contenido: 0 filas y 0 bytes. Estado: `training_authorized=false`, pendiente de snapshot por DOI/ISBN, derechos por elemento, privacidad, calidad, deduplicación global y G-0.

### WIPO Lex — bloqueada

No se incorpora como fuente entrenable. Sus términos actuales limitan los textos jurídicos y traducciones a fines académicos, de investigación y no comerciales; los juicios de PI no pueden adaptarse, modificarse ni utilizarse comercialmente. Además, prohíben consultas automatizadas, adquisición/descarga masiva y scraping. No se ha consultado ni descargado ningún payload. Solo podría reconsiderarse tras permiso escrito que cubra el uso previsto y autorización de todos los titulares pertinentes.

### Últimas ejecuciones programadas — runs 123 y 124

Ambos runs terminaron correctamente porque registraron un bloqueo previo a cualquier descarga. El repositorio es público y `HERETIC_STAGING_PASSPHRASE` estaba ausente o por debajo de 32 caracteres.

| Run | Grupo | Filas | Bytes JSONL | Staged | Admitidos | Manifiesto ZIP |
|---|---:|---:|---:|---:|---:|---:|
| [123](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44177892230) | 3/8 | 0 | 0 | 0 | 0 | [14370333374](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44177892230/artifacts/14370333374) |
| [124](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44262175192) | 5/8 | 0 | 0 | 0 | 0 | [14409340141](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44262175192/artifacts/14409340141) |

En ambos: 871 bytes de JSON dentro de un ZIP de 653 bytes; bytes remotos y comprimidos no medidos, pues no se inició la descarga. Los dos artefactos se descargaron y verificaron:

- Run 123: ZIP SHA-256 `f6099c982aa2fe7a1ab0500f6fac06279223a46b59757849a8fdc7aed01cc4a8`; JSON SHA-256 `2829acd2e3d3d88cd5d58aa573fff9cfc9c9067d45dc1035e09e1c190c488b26`.
- Run 124: ZIP SHA-256 `0f4c06392971fb32a751e5878d6737deed43aa98196b002ff637ccf58ae7a650`; JSON SHA-256 `0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7`.

Los manifiestos declaran `blocked_storage_gate`, `payload_downloaded=false`, `total_rows=0` y `training_authorized=false`. No existen hashes de shards porque no hubo shards.

**Inventario admitido sin cambios:** 260.971 documentos y 703.593.871 bytes; progreso **0,140719 %** de 500 GB. No se suman candidatos, manifiestos ni tamaños de artefactos.


## Curación de biblioteca — actualización verificada 2026-11-19

### Canada Justice Laws — candidata discovery-only, no admitida

Se reevalúa la entrada existente de **Canada Justice Laws: consolidated federal laws bulk XML**. La ficha oficial del Open Government Portal identifica el recurso concreto “Consolidated federal Acts and regulations – Bulk XML” y le asigna **Open Government Licence – Canada**; la misma ficha enlaza el repositorio oficial `justicecanada/laws-lois-xml`. En el commit inmutable `855cdfc65207a6906c414e09a77d7f93267c5356` (2026-11-16), el archivo `LICENSE.md` del repositorio vuelve a declarar Open Government Licence – Canada. La versión 2.0 permite copiar, modificar, traducir, adaptar y distribuir, también con fines comerciales, con atribución; excluye información personal, derechos de terceros no licenciables, símbolos oficiales y otros derechos de propiedad intelectual. [Ficha oficial del recurso](https://open.canada.ca/data/dataset/2f4bb174-b2e7-4fb2-a7a1-a313507acbc6) · [OGL Canada](https://open.canada.ca/en/open-government-licence-canada) · [LICENSE.md fijado](https://raw.githubusercontent.com/justicecanada/laws-lois-xml/855cdfc65207a6906c414e09a77d7f93267c5356/LICENSE.md).

La **Reproduction of Federal Law Order SI/97-5** permite además reproducir enactments y consolidaciones sin permiso, exige exactitud y prohíbe presentar reproducciones como versiones oficiales. La base para adaptación no se infiere de esa orden: procede de la OGL que el portal asigna al recurso y que figura en el repositorio de payload. [Orden oficial](https://laws-lois.justice.gc.ca/eng/regulations/SI-97-5/page-1.html).

- Revisión fijada: `justicecanada/laws-lois-xml@855cdfc65207a6906c414e09a77d7f93267c5356`; el commit indica legislación vigente al 2026-10-29.
- Alcance futuro: solo XML de Acts y Regulations en inglés/francés. Excluir DTD, XSLT, tablas de búsqueda, código, PDFs, símbolos, material de terceros y cualquier elemento con aviso distinto.
- Preservar ID, cita, título, idioma, fecha de consolidación/actualización y versión. Validar exactitud y no presentar copias como oficiales.
- PII, seguridad XML/XXE, integridad por archivo, calidad, muestra estratificada, deduplicación global y G-0 siguen pendientes.
- No se ha descargado payload: filas desconocidas; bytes remotos, descargados, comprimidos, expandidos, staged y admitidos no medidos/0 según corresponda. `training_authorized=false`; `count_toward_admitted_bytes=false`.

### Runs programados 128 y 129 — bloqueo de almacenamiento

Ambos runs terminaron correctamente solo porque registraron el bloqueo antes de contactar con las fuentes. En el repositorio público falta `HERETIC_STAGING_PASSPHRASE` de al menos 32 caracteres.

| Run | Grupo | Filas | Bytes de payload descargados | Staged | Admitidos | Artefacto |
|---|---:|---:|---:|---:|---:|---|
| [128](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44394965672) | 7/8 | 0 | 0 | 0 | 0 | [14467584999](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44394965672/artifacts/14467584999) |
| [129](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44482327436) | 1/8 | 0 | 0 | 0 | 0 | [14508428839](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44482327436/artifacts/14508428839) |

Cada ZIP contiene solo un manifiesto JSON de 871 bytes; el ZIP ocupa 653 bytes. Los bytes remotos anunciados/descargados y comprimidos no se midieron porque no hubo solicitudes de payload.

- Run 128: ZIP SHA-256 `cf794e0a569b259284d56b744943cc484a70fa30526fa2e1c4d384bfd316b41b`; JSON SHA-256 `3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992`.
- Run 129: ZIP SHA-256 `2b04d8064fb1dbff181e736ef47e4ac1c1732a9550367234e8c7b72569c2882f`; JSON SHA-256 `5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437`.

Los ZIP se descargaron y sus hashes se recalcularon independientemente; coinciden con los digests de GitHub. Ambos manifiestos declaran `blocked_storage_gate`, `payload_downloaded=false`, `total_rows=0` y `training_authorized=false`. No existen hashes de shards.

**Balance:** 0 admisiones nuevas. El total admitido permanece en **703.593.871 bytes / 260.971 documentos**, **0,140719 %** de 500 GB, según la última auditoría source-scoped [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). No se suman candidatos, manifiestos ni tamaños de artefacto.


## Nueva candidata multidisciplinar — Open Book Publishers (2026-11-19)

**Estado: discovery-only; cero documentos y bytes admitidos.**

Open Book Publishers es una editorial académica independiente, sin ánimo de lucro y dirigida por académicos. Declara más de 450 títulos, revisión por pares y múltiples disciplinas. Sus autores conservan el copyright y eligen la licencia de cada libro; por ello no existe una licencia general que permita tratar todo el catálogo como CC BY. [Política de autores y revisión](https://www.openbookpublishers.com/publish-with-us/information-for-authors) · [Catálogo](https://www.openbookpublishers.com/books).

La allowlist futura se limita a obras cuya propia página de título/copyright declare **CC BY 4.0 exacta**. Ejemplos de alcance, no admisiones:

- *Ovid, Amores (Book 1)*, William Turpin, DOI [10.11647/OBP.0067](https://doi.org/10.11647/OBP.0067): ficha individual CC BY 4.0, idioma inglés, ISBN XML.
- *Denis Diderot, Rameau's Nephew / Le Neveu de Rameau*, Marian Hobson, Kate E. Tunstall y Caroline Warman, DOI [10.11647/OBP.0098](https://doi.org/10.11647/OBP.0098): ficha individual CC BY 4.0, inglés/francés, ISBN XML.
- *Engaging Researchers with Data Management: The Cookbook*, ocho autores, DOI [10.11647/OBP.0185](https://doi.org/10.11647/OBP.0185): el front matter alojado por la editorial declara CC BY 4.0 y ofrece ISBN XML.

No se infiere una licencia de la ficha bibliográfica: los registros MARC de OBP se publican bajo CC BY-SA 4.0 y no son contenido entrenable; los metadatos Thoth CC0 son solo para descubrimiento. Los libros con NC, ND, SA, condiciones ambiguas, fair-use excerpts, derechos de capítulo separados o componentes de terceros quedan fuera. Figuras, fotografías, mapas, audio, vídeo, portadas y suplementos se excluyen salvo permiso independiente. La muestra *B C, Before Computers* contiene material identificado como fair use; no se debe adquirir íntegramente bajo la licencia del libro.

La revisión de cada obra deberá fijar DOI/edición, autores, copyright, licencia exacta, lengua, ISBN, asset XML/HTML/EPUB, timestamp y SHA-256. Siguen pendientes integridad, calidad, privacidad/PII, seguridad, muestra estratificada, deduplicación global y G-0. `training_authorized=false`; `count_toward_admitted_bytes=false`.
 
## Candidato multidominio — World Bank Data Catalog (2026-11-20)

**Estado: discovery-only; cero payload descargado y cero bytes admitidos.** Se registra el catálogo oficial como fuente de datos estructurados de agricultura, clima, economía, educación, energía, medioambiente, finanzas, salud, infraestructura, pobreza y gobernanza. El catálogo incluye miles de datasets; la licencia por defecto de los datasets del Banco Mundial es CC BY 4.0, salvo indicación distinta. No se hereda esa licencia a los datasets de terceros ni a los recursos con términos específicos.

La allowlist futura exige que tanto la ficha del dataset como los metadatos de cada recurso identifiquen exactamente **CC-BY-4.0**, y que el titular sea el propio Banco Mundial. Se excluyen ODbL/share-alike, Microdata Research License, NC/ND, licencias externas o custom, material restringido, microdatos y cualquier dataset de terceros sin clearance independiente. Deben fijarse dataset ID, versión, resource ID/versión, URL y SHA-256 por activo; el API documenta metadatos y endpoints de historial/versionado. Se conservará la atribución exigida por el Banco Mundial y el enlace a los términos vigentes. El idioma se medirá por recurso: no se presume que el catálogo sea multilingüe.

Fuentes primarias: [licencias del Data Catalog](https://datacatalog.worldbank.org/public-licenses) · [términos de datasets](https://www.worldbank.org/ext/en/legal/terms-conditions/datasets) · [API](https://ddh-openapi.worldbank.org/docs/index.html) · [guía de uso](https://datacatalog.worldbank.org/getting-started) · [FAQ](https://datacatalog.worldbank.org/faq).

La adquisición sigue bloqueada por almacenamiento: [run 133](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44613415575), grupo 3/8, y [run 134](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44696596900), grupo 5/8, finalizaron correctamente el preflight pero no descargaron payload. Ambos manifiestos declaran blocked_storage_gate, 0 filas, 0 bytes y training_authorized=false. Artefactos: [14573297654](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44613415575/artifacts/14573297654), SHA-256 ZIP 4a9803b324b2e9fd722f2eb6b27bdd4b76a06d810caaeb41de3329c3d0e184bd; [14610009546](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44696596900/artifacts/14610009546), SHA-256 ZIP b3cbb40c3a95d8da9ba45f779f2a8d27d7f50b85f1736ec099acfa202d8b2306. Los hashes internos de manifiesto y bytes exactos figuran en data/sources/registry.json.

No se ejecutaron revisión de muestras, escáneres de payload, deduplicación global ni G-0 porque no hubo payload. El candidato conserva training_authorized=false y count_toward_admitted_bytes=false. El inventario admitido no cambia: **260.971 documentos / 703.593.871 bytes**, **0,140719 %** del objetivo de 500 GB, según la auditoría source-scoped [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447).



## Curación candidate-only — 2026-11-21

### OECD Data Explorer — series de datos con derechos OECD acreditados

Se añade **OECD Data Explorer** como candidata discovery-only multidominio. Las condiciones oficiales de la OCDE permiten extraer, descargar, copiar, adaptar, distribuir, compartir e incorporar datos para cualquier finalidad, incluso comercial, salvo cuando existan restricciones adicionales o derechos de terceros. La propia OCDE advierte que no garantiza controlar todos los derechos de todos los datos. Por ello, solo se considerarán series cuya metadata y pestaña *source* acrediten derechos de OECD sobre todas las observaciones incluidas y ausencia de restricciones adicionales; la inclusión en el portal no basta. Se conserva la cita y atribución exigidas por serie. Esta autorización condicional no es una licencia CC/SPDX: no se asigna identificador SPDX.

La adquisición futura deberá fijar agencia, dataflow y versiones explícitas, DSD, codelists, restricciones/ValidFrom, consulta y dimensiones exactas, formato, timestamp UTC, longitud y SHA-256. La API SDMX admite CSV/JSON/XML. Se respetará el límite publicado de **60 descargas por hora**, sin VPN ni fuentes anonimizadas, usando cache y consultas de contentconstraint. Se excluirán series mixtas o de terceros sin autorización independiente, restricciones especiales, datos confidenciales/personales y cualquier registro con derechos inciertos. El candidato queda training_authorized=false, sin payload, filas ni bytes admitidos.

Fuentes oficiales: [condiciones de uso de OECD, §3 Data](https://www.oecd.org/en/about/terms-conditions.html) · [API SDMX](https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html) · [buenas prácticas y límites de API](https://www.oecd.org/en/data/insights/data-explainers/2024/11/Api-best-practices-and-recommendations.html) · [catálogo SDMX](https://sdmx.oecd.org/public/rest/dataflow/all).

### Adquisiciones programadas — runs 137 y 138

- [Run 137](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44813247702), grupo 7/8: preflight correcto, adquisición bloqueada por falta de HERETIC_STAGING_PASSPHRASE (mínimo 32 caracteres). Manifiesto [artifact 14667188891](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44813247702/artifacts/14667188891): ZIP 653 bytes, SHA-256 a93086b9570d214b0036a5cfb9c7b2a8c5711a041ced85b175ed8a46c88f71ff; JSON interno 871 bytes, SHA-256 3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992.
- [Run 138](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44881057593), grupo 1/8: mismo bloqueo antes de descargar. Manifiesto [artifact 14697991415](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44881057593/artifacts/14697991415): ZIP 653 bytes, SHA-256 5941156dc57a7e31ad2dab81621f7344a9a6748e45ace8c73040f434d75db0f7; JSON interno 871 bytes, SHA-256 5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437.
- Ambos manifiestos declaran blocked_storage_gate, training_authorized=false, 0 filas, 0 bytes de payload y 0 shards. El job de validación fue omitido en estos eventos programados; el éxito solo acredita que el bloqueo se registró correctamente.
- Admisiones nuevas: **0 documentos / 0 bytes**. No se midieron bytes remotos ni descargados; los 653 bytes ZIP y 871 bytes JSON son solo el artefacto/manifiesto, nunca datos de entrenamiento.

El inventario admitido permanece en **260.971 documentos / 703.593.871 bytes**, **0,140719 %** del objetivo decimal de 500 GB, según la auditoría source-scoped [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). G-0, deduplicación global, holdout y revisión de payload no se ejecutaron porque no hubo payload. No se ha entrenado ni modificado ningún checkpoint.


## Candidata multidominio — Statistics Canada Open Licence (2026-11-21)

Se añade Statistics Canada como candidata discovery-only para estadísticas agregadas multidominio y bilingües. La licencia oficial concede derechos mundiales, gratuitos y no exclusivos para usar, reproducir, publicar, distribuir o vender la información cubierta y productos derivados; pero solo cubre resultados no confidenciales en los que Statistics Canada sea titular o licenciatario de todos los derechos de propiedad intelectual. Los derechos de terceros permanecen en sus titulares. No se asigna SPDX porque es una licencia específica de la institución.

El alcance inicial se limita a tablas estadísticas agregadas no confidenciales con titularidad despejada. Se excluyen microdatos y PUMF aunque aparezcan en la definición amplia de Information, datos de personas/hogares/empresas, celdas pequeñas con riesgo de divulgación, material de terceros y contenido conjunto no despejado. Se prohíbe cualquier enlace o combinación orientada a reidentificar personas, empresas u organizaciones. Se conserva la atribución exacta y el aviso de adaptación; no se usan logotipos ni símbolos oficiales.

La WDS ofrece datos y metadatos diarios mediante JSON y SDMX; hay descargas completas CSV/SDMX y Delta Files diarios. Los metadatos incluyen títulos EN/FR. Para cada activo se fijarán PID, tabla/vector, releaseTime/issueDate, metadatos, code sets, petición exacta, formato, timestamp UTC, longitud y SHA-256. El manual publica un límite de 25 solicitudes por segundo por IP; se aplicará un ritmo conservador y caché. No se ha descargado payload: **0 filas y 0 bytes admitidos**, training_authorized=false.

Fuentes oficiales: [Open Licence](https://www.statcan.gc.ca/en/terms-conditions/open-licence) · [FAQ de la licencia](https://www.statcan.gc.ca/en/terms-conditions/open-licence-faq) · [Web Data Service](https://www.statcan.gc.ca/en/developers/wds) · [guía WDS](https://www.statcan.gc.ca/en/developers/wds/user-guide) · [portal de desarrolladores](https://www.statcan.gc.ca/en/developers).

El inventario admitido no cambia: **260.971 documentos / 703.593.871 bytes**, **0,140719 %** de 500 GB, según la auditoría source-scoped [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). La nueva fuente no se suma al contador hasta completar revisión por producto, privacidad, seguridad, deduplicación y G-0.


## Candidata multidominio — ILOSTAT, estadísticas agregadas y diccionarios EN/FR/ES (2026-11-22)

ILOSTAT queda registrada como candidata discovery-only. La política oficial de ILO cubre bajo **CC BY 4.0** las bases de datos, datasets y metadatos referenciales publicados o puestos a disposición desde el 3 de mayo de 2023, salvo indicación distinta. La misma política excluye microdatos enviados u obtenidos de constituyentes y socios cuando estén restringidos al uso exclusivo de ILO. No se asigna esta licencia a los datos upstream de terceros: cada tabla requiere revisión de su procedencia y de los campos `source`, `collection` y `note_source`.

El alcance potencial se limita a tablas estadísticas agregadas y diccionarios públicos. Se excluyen microdatos, registros de encuestas, datos confidenciales, celdas reidentificables y cualquier tabla cuyo origen o condiciones no acrediten los derechos de ILO. El portal de descarga documenta CSV comprimidos, metadatos y diccionarios; las tablas de contenido y diccionarios están disponibles en inglés, francés y español. Las cifras aproximadas de 500 tablas por indicador y 700 por área de referencia son descripciones dinámicas del portal, no filas elegibles ni bytes admitidos.

Cada activo deberá fijarse mediante su ruta exacta, fila de `table_of_contents`, `last.update`, colección, fuente, diccionarios, timestamp UTC, longitud comprimida/expandida y SHA-256. La revisión de calidad incluirá integridad gzip, esquema CSV, semántica de valores ausentes, idioma, privacidad, seguridad y muestras estratificadas. La fuente no está conectada al colector Hugging Face actual: requiere un descargador acotado dedicado.

**Estado:** 0 payload descargado, 0 filas y 0 bytes admitidos; `training_authorized=false`. No se ha asignado SPDX fuera del alcance estrecho CC-BY-4.0. Fuentes: [política de derechos ILO](https://www.ilo.org/rights-and-permissions) · [bulk download ILOSTAT](https://ilostat.ilo.org/data/bulk/) · [metodología de recopilación](https://ilostat.ilo.org/about/data-collection-and-production/).

### Adquisiciones programadas — runs 149 y 150

- [Run 149](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45063468144), grupo 7/8, commit `ad3a9a649ab1f21654195b65830759ddec4d977f`: storage gate bloqueado antes de descargar. [Artifact 14770830618](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45063468144/artifacts/14770830618), ZIP de 653 bytes, SHA-256 `16fb4e6c8fae488456ed0faa8fee8e3e83cc502820c451c31dcc5e89c8525568`; JSON interno de 871 bytes, SHA-256 `3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992`.
- [Run 150](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45135391130), grupo 1/8, mismo commit: mismo bloqueo. [Artifact 14800025470](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45135391130/artifacts/14800025470), ZIP de 653 bytes, SHA-256 `26c72180952574f3919dfa467fe2921ae97e47ef626c36fbfd24083470697bce`; JSON interno de 871 bytes, SHA-256 `5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437`.
- Ambos manifiestos declaran `blocked_storage_gate`, 0 filas, 0 bytes de payload y 0 shards. Los jobs de adquisición terminaron correctamente al registrar el bloqueo; los pasos de instalación/descarga/revisión se omitieron. Los hashes ZIP y JSON se recalcularon tras descargar los artefactos.
- Admisiones nuevas: **0 documentos / 0 bytes**. Los 653 bytes ZIP y 871 bytes JSON son solo contenedores/manifiestos, nunca corpus.

El inventario admitido permanece en **260.971 documentos / 703.593.871 bytes**, **0,140719 %** del objetivo decimal de 500 GB. G-0, deduplicación global, holdout y revisión de payload no se ejecutaron porque no hubo payload. No se ha entrenado ni modificado ningún checkpoint.

## Fuentes investigadas y no adquiribles — 2026-11-22

- **UNESCO Institute for Statistics (UIS) Data Browser:** excluido porque sus términos oficiales declaran CC BY-SA 4.0. El proyecto no ha aprobado share-alike; no se descarga ni se incorpora contenido. Además, cualquier futura reconsideración exigiría revisar la procedencia de los indicadores y sus fuentes upstream.
- **UN Comtrade:** bloqueado. La política permite uso de IA dentro del uso interno definido como uso por personal de una unidad institucional en beneficio de esa unidad, pero prohíbe la redistribución externa de datos originales sin permiso de UNSD. No se ha acreditado elegibilidad institucional ni una licencia de distribución para el uso previsto. No se descarga ni se admite contenido.

Ambas fuentes figuran en `data/sources/registry.json` como no adquiribles, con `training_authorized=false` y cero bytes. Evidencia: [UIS terms](https://databrowser.uis.unesco.org/terms-and-conditions) · [UN Comtrade use policy](https://uncomtrade.org/docs/policy-on-comtrade-data-use/) · [UN Comtrade redistribution](https://uncomtrade.org/docs/re-dissemination-of-data/).


## Hansard — informes diarios con aviso OPL explícito (2026-11-23)

Se añade una fuente discovery-only para informes diarios Commons/Lords cuyo propio PDF incluya el aviso exacto de reproducción bajo **Open Parliament Licence v3.0 (OPL-UK-3.0)**. La muestra oficial Commons de 2026-11-03 incluye el aviso en la página 1. La licencia permite adaptación y uso comercial con atribución, pero excluye datos personales y derechos de terceros. Los discursos contienen nombres de parlamentarios y referencias a particulares; no se descargará payload hasta que una revisión de privacidad pueda excluir/redactar de forma fiable los datos personales y un control por documento despeje los elementos de terceros.

El archivo Historic Hansard no queda cubierto por inferencia: su página de archivo declara que el material permanece bajo Parliamentary Copyright. Solo se podría reconsiderar un documento histórico si su propio PDF incluye el aviso OPL aplicable.

- Fuente y endpoint: [Hansard](https://hansard.parliament.uk/) · `/pdf/{Commons|Lords}/YYYY-MM-DD`.
- Evidencia de alcance: [PDF Commons 2026-11-03](https://hansard.parliament.uk/pdf/Commons/2026-11-03) · [Open Parliament Licence](https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/) · [SPDX OPL-UK-3.0](https://spdx.org/licenses/OPL-UK-3.0.html) · [Historic Hansard copyright notice](https://api.parliament.uk/historic-hansard/index.html).
- Fijación: cámara, fecha, volumen, número, URL, timestamp UTC, páginas, bytes exactos y SHA-256 del PDF; hash independiente del texto extraído.
- Exclusiones: datos personales, referencias identificables a particulares, material de terceros, imágenes, escudos, marcas, audio/vídeo y adjuntos.
- No hay colector dedicado ni payload adquirido. `acquisition_enabled=false`, `training_authorized=false`, 0 filas y 0 bytes admitidos. G-0 y la deduplicación global siguen pendientes para cualquier futura adquisición.


## Descubrimientos nuevos — Europeana y New Zealand Legislation (2026-11-24)

### Europeana — metadatos culturales multilingües, CC0

Se registra como candidata **solo para metadatos**. Europeana publica todos los metadatos disponibles en europeana.eu bajo CC0 1.0, pero los objetos digitales, imágenes, audio, vídeo, transcripciones y contenidos enlazados conservan los derechos indicados por cada registro/proveedor. No se infiere que CC0 de metadatos relicencie el objeto. La metadata incluye valores en varios idiomas; deben preservarse los xml:lang por campo y la procedencia de traducciones/enriquecimientos. Se excluye toda descarga de edm:object, edm:isShownBy, edm:preview, europeana:object, enclosure y URLs de proveedores. Los metadatos también requieren filtro de privacidad, ya que pueden describir personas vivas o incluir información sensible.

- [Términos de uso](https://www.europeana.eu/en/rights/terms-of-use) · [Guía de uso de metadatos](https://www.europeana.eu/en/rights/usage-guidelines-for-metadata) · [API key](https://pro.europeana.eu/page/get-api) · [multilingüismo](https://pro.europeana.eu/index.php/page/data-multilinguality) · [Europeana Data Model](https://pro.europeana.eu/index.php/page/edm-documentation).
- La API requiere una clave confidencial; no se ha solicitado ni configurado una clave de proyecto. No hay colector ni snapshot adquirido.

### New Zealand Legislation — legislación oficial sin copyright (s. 27)

Se registra como candidata para Bills, Acts, regulations y bylaws cubiertos por la sección 27 de la Copyright Act 1994. Los términos oficiales de la API confirman que el Crown no reclama copyright sobre la compilación de datos legislativos. Esto no despeja obras de terceros incorporadas por referencia. Se excluyen del piloto la legislación secundaria publicada por agencias (calidad/integridad advertidas por PCO), material de terceros, emblemas y ayudas del sitio. La API v0 beta requiere una clave confidencial, tiene límites de 10.000 solicitudes por clave/día y 2.000 por IP cada cinco minutos. Cada obra y versión debe fijarse mediante work_id, version_id, fecha, estado, formato XML y SHA-256.

- [Copyright](https://www.legislation.govt.nz/copyright/) · [API terms](https://www.legislation.govt.nz/learn-more/legislation-data/api-terms-of-use/) · [Developer API](https://www.legislation.govt.nz/developer-api) · [Copyright Act 1994, s.27](https://www.legislation.govt.nz/act/public/1994/143/en/latest/sections/DLM345939/) · [anuncio de la API, 2026-02-11](https://www.legislation.govt.nz/learn-more/news/earlier-news-posts/earlier-2026-news-posts/legislation-api-now-available-plus-a-reminder-that-rss-feeds-will-change).
- No se ha solicitado ni configurado la clave API. No hay colector ni payload adquirido.

Ambas fuentes quedan discovery-only, acquisition_enabled=false, training_authorized=false, 0 filas y 0 bytes admitidos. Requieren claves separadas, colectores dedicados, revisión de privacidad y procedencia, deduplicación y G-0.

### Adquisiciones programadas — runs 153 y 154 (2026-11-24)

- [Run 153](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45295413549), grupo 4/8, artifact [14876935300](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45295413549/artifacts/14876935300): storage gate bloqueado antes de descargar; ZIP 653 bytes, SHA-256 7660bc0aa3a07c8f214f52048d1cbb543ee3e586d613e9c7006f58feeb83be83; JSON 871 bytes, SHA-256 3410f1b55d99d02fe29be723a56d8fefb20a81e0c517fe1cc6e7aa0eedcfd8ec.
- [Run 154](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45373420083), grupo 5/8, artifact [14909198800](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45373420083/artifacts/14909198800): mismo bloqueo; ZIP 653 bytes, SHA-256 5682d2f797a45ac60aa0b5ef62ece713aee192e45bd0b35b1b3d45dc893af5b1; JSON 871 bytes, SHA-256 0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7.
- Ambos manifiestos se descargaron y verificaron; registran blocked_storage_gate, 0 filas, 0 shards, 0 bytes de payload y training_authorized=false. Los 653 bytes ZIP y 871 bytes JSON son manifiestos, no corpus.
- **Admisiones nuevas: 0 documentos / 0 bytes.** Inventario global sin cambios: 260.971 documentos y 703.593.871 bytes admitidos.


## Descubrimientos nuevos — 2026-11-25: MASSIVE 1.1 y Universal Dependencies 2.19

### AmazonScience MASSIVE 1.1 — candidato de texto multilingüe CC BY 4.0

La versión 1.1 añade catalán a las 51 lenguas anteriores: 52 idiomas, más de un millón de utterances paralelas, 18 dominios, 60 intents y 55 tipos de slot. El NOTICE específico de Amazon declara CC BY 4.0 para el dataset y confirma que el texto fuente de SLURP es CC BY 4.0. La parte de audio de SLURP es CC BY-NC 4.0 y queda excluida. Se fija el README/NOTICE en el commit `f966f21846043aabef9b0f974fa7970027f43738` y SLURP en `8eb16545762be97ace75334109d73824217311f1`; el tarball 1.1 aún no se ha descargado ni hasheado.

- [MASSIVE 1.1 oficial](https://github.com/alexa/massive/blob/f966f21846043aabef9b0f974fa7970027f43738/README.md) · [NOTICE de datos](https://github.com/alexa/massive/blob/f966f21846043aabef9b0f974fa7970027f43738/NOTICE.md) · [tarball 1.1](https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz) · [licencia textual SLURP](https://github.com/pswietojanski/slurp/blob/8eb16545762be97ace75334109d73824217311f1/LICENSE.txt).
- Solo se considerará `partition=train`; dev/test y el material de evaluación MMNLU-22 quedan fuera. Se eliminarán `worker_id` y todos los identificadores anidados en `judgments`; se conservarán únicamente métricas agregadas para filtrar gramática, ortografía, intent y slots.
- Estado: discovery-only, `acquisition_enabled=false`, `training_authorized=false`; 0 filas y 0 bytes descargados/admitidos. Pendientes LICENSE del tarball, hash, calidad por idioma, privacidad, near-dedup y G-0 completo.

### Universal Dependencies 2.19 — candidato multilingüe con licencias mixtas por treebank

El release oficial del 15-11-2026 contiene 402 treebanks en 226 idiomas y se distribuye mediante LINDAT/CLARIAH-CZ, handle `11234/1-6316`. No existe una licencia única para la colección: UD exige revisar `LICENSE.txt` y el campo `License:` del README de cada treebank. Solo se consideran licencias exactas CC BY 4.0 o CC0 1.0, y únicamente cuando también estén despejados los derechos del texto subyacente. BY-SA, NC, ND, GPL y licencias ausentes/contradictorias quedan fuera.

- [Release 2.19](https://universaldependencies.org/download.html) · [política oficial de licencias](https://universaldependencies.org/contributing/licensing.html) · [snapshot LINDAT](https://hdl.handle.net/11234/1-6316).
- Riesgos ya identificados: Spanish AnCora declara CC BY 4.0 en metadatos pero su descripción remite a una licencia GNU heredada; queda excluido. English GUMReddit indica que el texto subyacente no está incluido; no se descargará ni fusionará texto externo. Solo se considerarían ficheros `*-train.conllu`; ningún dev/test/test-only.
- Estado: discovery-only, `acquisition_enabled=false`, `training_authorized=false`; 0 payload y 0 bytes admitidos. Pendientes manifiesto y hash del release, auditoría por treebank, derechos del texto, muestras, calidad, privacidad, deduplicación global y G-0.

### Common Voice v27.0 — aclaración de términos MDC

Los términos oficiales vigentes desde 2025-10-31 disponen que los datasets se ofrecen exclusivamente a través de Mozilla Data Collective y piden no publicar, distribuir ni replicar/mirror el dataset en otras plataformas. Además, sigue pendiente la procedencia de cada prompt (se excluyen Wikipedia y fuentes no despejadas). Se mantiene `acquisition_enabled=false` hasta disponer de una ruta compatible con MDC que no re-hospede el payload.

- [Common Voice Legal Terms](https://commonvoice.mozilla.org/oc/terms) · [datasets MDC](https://commonvoice.mozilla.org/en/datasets).

**Balance de las tres fuentes:** 0 descargas, 0 filas medidas y 0 bytes admitidos; no se suman a la biblioteca.

## Adquisiciones programadas — runs 157 y 158 (2026-11-25)

- [Run 157](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45503206072), grupo 7/8, artifact [14971249604](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45503206072/artifacts/14971249604): ZIP 653 bytes, SHA-256 `99c089bad3165b290c5d47d3677581cbe73ef1a7474579525d6c7ff272090dc5`; manifiesto JSON 871 bytes, SHA-256 `3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992`.
- [Run 158](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45581135551), grupo 1/8, artifact [15005629437](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45581135551/artifacts/15005629437): ZIP 653 bytes, SHA-256 `63475b22bd76851a587b41c254468d7bde1eced8e9f6bdf78cec11c21a8ae7d4`; manifiesto JSON 871 bytes, SHA-256 `5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437`.
- Ambos terminaron `success` porque el preflight completó correctamente, pero el storage gate bloqueó antes de contactar fuentes o descargar payload: 0 filas, 0 bytes remotos/descargados medidos, 0 staged y 0 admitidos. Motivo: falta `HERETIC_STAGING_PASSPHRASE` de al menos 32 caracteres. Los ZIP contienen solo manifiestos, no corpus.
- **Admisiones nuevas: 0 documentos / 0 bytes.** Inventario admitido sin cambios: **260.971 documentos / 703.593.871 bytes**, **0,140719 %** de 500 GB.


## Descubrimientos y preflights — 2026-11-26

| Fuente | Alcance revisado | Estado | Motivo / siguiente gate |
|---|---|---|---|
| United Nations Parallel Corpus v1.0 | Documentos oficiales 1990–2014, seis idiomas; atribución UN obligatoria | Candidata discovery-only | Fijar y hashear cada parte; excluir por completo test/dev 2015; calidad, privacidad y G-0 global |
| MOT v1.11 | CC BY 4.0; 54 archivos de sitio anunciados por 8.342.562.863 bytes en total | Candidata discovery-only | Solo texto de artículos de autoría exclusiva VOA; excluir AFP/AP/Reuters y medios; hashes por asset, revisión humana y G-0 |
| JRC DCEP | Corpus multilingüe del Parlamento Europeo | Bloqueado | La cesión oficial de derechos es para fines de investigación |
| LR-Sum | Resúmenes en 39/40 idiomas declarados según revisión | Bloqueado | La ficha lo describe como principalmente destinado a investigación; linaje VOA/terceros sin auditoría por registro |

**Runs recientes:** [162](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45708741819), artifact [15066562283](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45708741819/artifacts/15066562283), ZIP SHA-256 `73d43b33e273ceb588503f9a9e1366da21b7311d5da79a3368416afcb42a8df1`, manifiesto SHA-256 `2829acd2e3d3d88cd5d58aa573fff9cfc9c9067d45dc1035e09e1c190c488b26`; [163](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45785916162), artifact [15100551941](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45785916162/artifacts/15100551941), ZIP SHA-256 `1cecaa91ba593acfdee3925a060a21eb2a0bb5818c239b72fb55728960a2e1b4`, manifiesto SHA-256 `0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7`. Cada ZIP mide 653 bytes y contiene un JSON de 871 bytes; ambos manifiestos indican `blocked_storage_gate`, cero filas, cero payload y `training_authorized=false`.

**Admisiones nuevas: 0 documentos / 0 bytes.** El inventario sigue en 260.971 documentos y 703.593.871 bytes admitidos. G-0 global continúa bloqueado; no se ha ejecutado deduplicación ni contaminación sobre nuevos payloads porque no hubo descargas.

## Descubrimientos y preflights — 2026-11-27

### Parallel Global Voices — candidato multilingüe

- La ficha de CLARIN informa 174.629 documentos, 302.617 pares de documentos y 8.356.943 alineamientos de segmentos en 756 pares de lenguas; son recuentos publicados, no bytes medidos. El crawl de ILSP se realizó en 2015-2016 y cubre más de 40 idiomas.
- Derechos por capas: Global Voices aplica CC BY a su contenido salvo aviso distinto; el pie del sitio identifica CC BY 3.0. ILSP declara los alineamientos generados bajo CC BY 4.0. No hay un único SPDX para el conjunto. Se exigirá página original, autor/byline, licencia exacta y atribución por artículo; se excluyen media y contenido de terceros.
- Privacidad: revisión reforzada de historias sobre activistas, víctimas, menores y personas privadas; excluir opt-outs, retractaciones y bylines retirados por seguridad. Solo texto y alineamientos, nunca imágenes/audio/vídeo.
- Estado: discovery-only, acquisition_enabled=false, training_authorized=false; 0 descargas y 0 bytes admitidos.

### ParlaMint.ana 5.0 — candidato multilingüe de debates parlamentarios

- CLARIN.SI item [11356/2005](https://www.clarin.si/repository/xmlui/handle/11356/2005), emitido 2025-07-08, marca sus archivos bajo CC BY 4.0. El registro informa 8.132.022 utterances, 1.231.045.523 palabras, 1.402.488.391 tokens y 29 lenguas; son cifras del catálogo, no bytes adquiridos.
- El tag Git v5.0 se resuelve al commit 978f9051793367fc2192eedc80c1e71ac8ec7ea5, pero ese repositorio contiene muestras, esquemas y scripts, no el corpus completo. La revisión de datos debe fijarse por archivos de CLARIN.SI y SHA-256 por país.
- Riesgos: los metadatos incluyen nombres, género, afiliación, orientación política, año de nacimiento y comités. Se excluyen TSV de hablantes, perfiles, etiquetas de tema/sentimiento y la versión traducida al inglés 11356/2006. Se exige despejar derechos de las transcripciones por parlamento/jurisdicción y revisar privacidad del texto.
- Estado: discovery-only, acquisition_enabled=false, training_authorized=false; 0 descargas y 0 bytes admitidos.

### Preflights recientes

- [Run 165](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45900766740), grupo 7/8, artifact [15156090956](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45900766740/artifacts/15156090956): ZIP 653 bytes, SHA-256 0ca28a1224eb8f57adf481528e9dab3a93ba3850bb41eb2b31e49132dc623902; JSON 871 bytes, SHA-256 3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992.
- [Run 166](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45969736101), grupo 1/8, artifact [15184268031](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45969736101/artifacts/15184268031): ZIP 653 bytes, SHA-256 5cde9471e155fc56cf5c59cfb10c6b6922aaccc625e79d7bc8a8a90e91de9f12; JSON 871 bytes, SHA-256 5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437.
- Ambos ZIP se descargaron y sus SHA-256 se recalcularon; coinciden con el digest de GitHub. Los JSON internos confirman blocked_storage_gate, sources=[], 0 filas, 0 bytes y training_authorized=false. El job omitió instalación y descarga porque falta HERETIC_STAGING_PASSPHRASE de al menos 32 caracteres.
- Bytes remotos/descargados/comprimidos/expandidos de corpus: no medidos/0/0/0; staging durable: 0; bytes admitidos: 0. Los 653 bytes ZIP y 871 bytes JSON son solo manifiestos.

**G-0 global sigue bloqueado**: el inventario de splits protegidos continúa incompleto. No se ejecutó deduplicación global ni contaminación de holdout sobre nuevos payloads porque no hubo descargas. Inventario histórico sin cambios: **260.971 documentos / 703.593.871 bytes**, **0,140719 %** de 500 GB.


## Federal Register (GovInfo) — candidata discovery-only (2026-11-27)

- Alcance: XML de issues oficiales en el repositorio GovInfo, años 2000 en adelante; fuente multidominio (regulación, administración, salud, ambiente, energía, transporte, finanzas, trabajo, educación y otros ámbitos federales).
- Reutilización: [1 CFR 2.6](https://www.ecfr.gov/current/title-1/chapter-I/subchapter-A/part-2/section-2.6) permite reproducir/republicar sin restricción cualquier material que aparezca en ediciones regulares o especiales del Federal Register; [NARA/OFR](https://www.archives.gov/federal-register/the-federal-register/about.html) lo confirma. No se asigna SPDX. La sección 17 USC §105 se conserva como contexto para obras federales cualificadas, no como licencia general para terceros.
- Payload: [GovInfo FR bulk XML](https://www.govinfo.gov/bulkdata/FR). La guía GPO [fijada al commit 83a85170ce0bdd0cf218f6290bd739df8748e2ea](https://github.com/usgpo/bulk-data/blob/83a85170ce0bdd0cf218f6290bd739df8748e2ea/FR-XML_User-Guide.md) indica que el XML comienza en 2000, no es el formato legal oficial online y puede contener anomalías de tablas/marcado; solo PDF/Text tienen estatus oficial online. Se exige cotejo de muestras con PDF/Text.
- La Library of Congress advierte que algunos ítems pueden reimprimir obras protegidas de terceros. Se excluyen segmentos, gráficos, adjuntos y obras externas sin derechos despejados; también comentarios/dockets externos, user aids, sellos y logos. Privacidad document/segment-level obligatoria.
- Inmutabilidad: congelar listado anual, issue date, volumen/número, package/document IDs, URL, headers, timestamp UTC, longitud y SHA-256 por XML; registrar también revisión de schema/XSL.
- Estado: discovery-only, `acquisition_enabled=false`, `training_authorized=false`; 0 filas medidas, 0 bytes descargados y 0 bytes admitidos. Pendientes colector dedicado, almacenamiento seguro, revisión humana, calidad, deduplicación y G-0 global.

### Acciones de 2026-11-27

- [Run 46009185876](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/46009185876): auditoría source-scoped del artefacto RONIN-IA; terminó correctamente, pero no enumera todos los splits protegidos y no constituye G-0 global.
- [Run 46009185814](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/46009185814): curación y auditoría source-scoped de Cosmopedia; terminó correctamente. Su artefacto no supone por sí solo admisión nueva.
- [Último preflight programado #166](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45969736101): storage gate bloqueado antes de descarga; manifiesto de 871 bytes, 0 filas, 0 payload y 0 admisiones. ZIP artifact [15184268031](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45969736101/artifacts/15184268031), SHA-256 `5cde9471e155fc56cf5c59cfb10c6b6922aaccc625e79d7bc8a8a90e91de9f12`; JSON interno SHA-256 `5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437`.


## Recursos paralelos multilingües de la Comisión Europea (2026-11-27)

### DGT-Acquis — candidata discovery-only

- Fuente oficial: https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en
- Corpus del Diario Oficial desde mediados de 2004 hasta finales de 2011, hasta 23 idiomas. La página publica 4.900.254 segmentos para da1-pc (unos 3 GB comprimidos), 3.537.872 ficheros para da1-ft (unos 5 GB) y 3.537.876 para da1-fx (unos 9 GB). Son estadísticas del editor; no son descargas ni bytes admitidos.
- La Comisión declara titularidad exclusiva del dataset y cesión no exclusiva, mundial y gratuita para todo uso compatible con la Decisión 2011/833/EU. No hay SPDX estándar; mantener `spdx_license_identifier=null` y conservar atribución, URL, última actualización y titularidad de la Comisión.
- Alcance propuesto: da1-ft para contexto de documento completo; da1-pc solo como representación/alineación tras deduplicar. Excluir TIFF, software, marcas/logos y documentos con derechos de terceros, confidenciales o restricciones especiales. Resolver cada NumDoc contra EUR-Lex.
- Estado: discovery-only; acquisition_enabled=false; training_authorized=false; 0 descargas y 0 bytes admitidos.

### DGT-TM — candidata discovery-only

- Fuente oficial: https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-translation-memory_en
- Memoria TMX en 24 idiomas, UTF-16LE; extracción con inglés como pivote. La página declara titularidad de la Comisión y cesión mundial para todo uso bajo Decisión 2011/833/EU, con atribución y obligación de no distorsionar. La colección incluye documentos no pertenecientes al Acquis; cada NumDoc debe verificarse individualmente.
- La página indica preprocesamiento que puede cambiar el contenido y alineación automática desde releases 2011. Se requiere auditoría por release, par de idiomas, dominio y longitud; excluir software TMXtract y documentos de terceros.
- Estado: discovery-only; acquisition_enabled=false; training_authorized=false; no se ha descargado ningún ZIP.

### JRC-Acquis v3.0 — bloqueado por conflicto de términos

- La página actual JRC-Acquis afirma cesión mundial para todo uso bajo Decisión 2011/833/EU, pero enlaza la página de licencia histórica, actualizada en 2011, que dice que el corpus puede usarse/distribuirse para investigación y describe distribución no comercial.
- Hasta obtener aclaración escrita de JRC/OP, no descargar, no staging y no training_eligible. El corpus anuncia 22 idiomas, 463.792 textos, 4.350.447 documentos alineados y 243.187.303 enlaces; cifras del editor, no inventario admitido.
- URLs: https://joint-research-centre.ec.europa.eu/language-technology-resources/jrc-acquis_en ; https://wt-public.emm4u.eu/Acquis/JRC-Acquis.3.0/doc/licence.html ; https://eur-lex.europa.eu/eli/dec/2011/833/oj/eng

Para DGT-Acquis/DGT-TM, los snapshots deben fijar cada ZIP/idioma, lista de archivos, NumDoc/CELEX, headers, fecha UTC, bytes y SHA-256. Deduplicar por CELEX/NumDoc y texto normalizado entre ambos recursos, JRC-Acquis, EUR-Lex y todos los splits protegidos. G-0 global sigue siendo obligatorio.
