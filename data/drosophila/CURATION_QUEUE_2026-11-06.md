# Cola de curación generalista — biblioteca Drosophila

Fecha: 2026-11-06. **Drosophila es el nombre del corpus experimental, no una restricción temática a la mosca biológica.** La biblioteca admite conocimiento general y multidominio: matemáticas, lógica, programación, ciencias naturales, ingeniería, economía, humanidades, idiomas y conocimiento técnico.

Esta cola sustituye la interpretación biológica errónea de la revisión anterior. La biología de *Drosophila melanogaster* puede ser un dominio más, pero no define el corpus.

## Estado y reglas
- Corpus sintético versionado actual: 50.000 filas en 10 shards JSONL. Es candidato experimental, no 50.000 documentos gold ni 50.000 capacidades independientes.
- Biblioteca objetivo: 500 GB decimales de bytes efectivamente admitidos, no tamaño remoto anunciado.
- Solo seleccionar registros marcados explícitamente para `train`; nunca validation, test ni holdout.
- Elegibilidad source-scoped no equivale a superar G-0 global: faltan controles globales de near-duplicates, contaminación de holdout y asignación de bibliotecas.
- Los documentos propios con autorización de uso interno no adquieren por ello derechos de redistribución pública o comercial.
- No se hará un fork ciego ni se copiarán repositorios completos. Se fijarán revisiones inmutables, licencias por activo y splits.

## Importación desde RONIN-IA — inventario inicial

| Fuente | Partición train declarada | Derechos/alcance | Situación del payload |
|---|---:|---|---|
| CoVoST 2 translation-only | 270.244 segmentos | CC0-1.0; solo texto de traducción; no audio ni frases originales de Common Voice | `train.jsonl.gz` presente |
| ScienceVerse CC-BY | 7.103 documentos | CC BY 4.0 / CC0 por documento; atribución; train source-scoped | Payload por corpus presente; filtrar `training_eligible=true`; 262 held excluidos |
| Mathlib4 | 8.498 documentos | Apache-2.0; train source-scoped | Solo manifiesto en Git; recuperar artefacto auditado |
| Literatura española | 608 documentos | Licencia y procedencia por fuente; train source-scoped | Solo manifiesto en Git; recuperar artefacto auditado |
| NASA NTRS file-reviewed | 2 documentos en manifiesto actual | Train explícito y alcance file-reviewed; no usar el conjunto public-use completo | `documents.train.jsonl` y `train.txt` presentes |
| Papers propios | 9 documentos | Autorización explícita para entrenamiento interno; no inferir redistribución externa/comercial | Payload Markdown presente |

**No sumar estas cifras como importación completada.** Son conteos de manifiestos; antes de integrar hay que recuperar payloads faltantes, validar hashes, filtrar elegibilidad por documento, deduplicar contra Drosophila y holdout y conservar licencia, autoría y procedencia. ScienceVerse declara `global_g0=FAIL`; siguen pendientes near-duplicates globales y contaminación de holdout. Si estos controles no pasan, los datos quedan en staging.

El bootstrap actual copia el directorio `admitted` completo a un artefacto temporal; no es una importación filtrada al lector de entrenamiento.

## Candidatos GitHub para revisión

| Repositorio | Dominio | Licencia declarada | Decisión inicial |
|---|---|---|---|
| [UltraData-OpenBMB/UltraData-Math](https://github.com/UltraData-OpenBMB/UltraData-Math) | Matemáticas | Apache-2.0 declarado en el repositorio | Candidato prioritario; verificar licencia del payload, revisión inmutable, shards y linaje antes de descargar |
| [amazon-science/street-reasoning](https://github.com/amazon-science/street-reasoning) | Razonamiento multidominio | Apache-2.0 para el repositorio | Código/generador no autorizan automáticamente los datasets upstream; revisar derechos por tarea y split |
| [Zhenwen-NLP/MathChat](https://github.com/Zhenwen-NLP/MathChat) | Matemáticas / diálogo | Apache-2.0 en el repo | No entrenar por defecto: README indica dependencia de ejemplos del test de GSM8K; aislar por riesgo de contaminación |
| [GovDataHub/open-data-index](https://github.com/GovDataHub/open-data-index) | Catálogo público: clima, energía y economía | Licencias por dataset en el catálogo | Índice de descubrimiento, no dataset de texto; verificar fuente primaria por activo |

Las licencias del código de un repositorio no cubren automáticamente sus datos de terceros. Los catálogos agregadores tampoco sustituyen la licencia del activo original.

## Procedimiento obligatorio
1. Fijar URL, commit/release, archivo, tamaño y SHA-256.
2. Leer licencia del activo y fuentes upstream; bloquear NC, ND, share-alike no aprobado, research-only o licencia no declarada.
3. Descargar solo train; aislar validation/test/holdout.
4. Preservar autor, cita, URL, DOI, SPDX/licencia, revisión, archivo original, hash y condiciones.
5. Validar esquema, codificación, calidad, PII, secretos y seguridad.
6. Deduplicar exacta y aproximadamente contra biblioteca y holdouts.
7. Auditar muestra estratificada por dominio, idioma, fuente y formato.
8. Normalizar sin borrar estructura ni contexto; preservar dirección source/target en traducciones.
9. Emitir manifiesto con conteos por estado y bytes comprimidos/descomprimidos.
10. Integrar al entrenamiento solo cuando el pipeline consuma el lote validado y la evaluación pareada no muestre regresión.

## Estados
- `discovery`: fuente localizada, licencia/payload sin verificar.
- `candidate`: revisión y archivos identificados; no entrenable.
- `staged_train`: payload recuperado y manifiesto source-scoped validado; faltan gates globales.
- `admitted_train`: todos los gates superados; entrenable.
- `held` / `rejected`: excluido con motivo.

**Estado de esta cola:** corrección conceptual y priorización documental. No declara importaciones nuevas ni bytes adicionales admitidos.


## Ampliación de fuentes externas — 2026-11-06

Se amplía la búsqueda más allá de RONIN-IA. Estos candidatos son multidominio; ninguno se cuenta todavía como bytes admitidos:

| Fuente | Escala declarada | Licencia declarada | Estado y cautela |
|---|---:|---|---|
| [OpenThoughts3-1.2M](https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M) | 1,2 M filas; ~59,8 GB expandidos | Apache-2.0 en la ficha | Prioridad alta: matemáticas, código y ciencia. La ficha no enumera todos los orígenes de preguntas; auditar linaje y contaminación antes de importar. |
| [Aya Dataset](https://huggingface.co/datasets/CohereLabs/aya_dataset) | 204 k pares; 65 idiomas | Apache-2.0 en la ficha | Prioridad alta para español y multilingüismo. Revisar splits, atribución y separar datos demográficos de anotadores/PII. |
| [Dolma](https://huggingface.co/datasets/allenai/dolma) | Muestra v1.6 ~16,4 GB comprimidos; corpus completo multi-TB | ODC-BY-1.0 | Generalista: web, ciencia, código, libros y enciclopedia. La licencia de base de datos no sustituye los términos de las fuentes originales. |
| [FineWeb](https://huggingface.co/datasets/HuggingFaceFW/fineweb) | sample-350BT ~388 GB | ODC-BY-1.0 | Útil para ampliar preentrenamiento general; preservar URL/fecha/atribución y no asumir que cada página web tiene licencia abierta. |
| [DCLM Baseline](https://huggingface.co/datasets/mlfoundations/dclm-baseline-1.0) | ~7,2 TB | CC-BY-4.0 declarada | Selección acotada por shards; revisar procedencia, restricciones de uso de investigación y atribución. |

**Orden de adquisición recomendado:** OpenThoughts3 (tranche de train pequeña y auditable) → Aya (multilingüe) → shards de Dolma/FineWeb/DCLM. No descargar terabytes completos sin medir coste, solapamiento y utilidad marginal. Para los tres corpus web, la licencia de la base de datos no debe presentarse como licencia individual de cada documento.

La cifra objetivo de 500 GB sigue siendo una meta de almacenamiento, no una autorización para aceptar contenido de derechos inciertos.

## Auditoría de derechos y nueva adquisición — 2026-11-06

### Aya Dataset — candidato multilingüe verificable

La ficha oficial de CohereLabs declara Apache-2.0 y permite cualquier propósito. Se añade una adquisición limitada a 5.000 ejemplos de la configuración `default`, partición `train`, extrayendo únicamente `inputs` y `targets`. La configuración `demographics` y el campo `user_id` quedan fuera. El script exige que la revisión inmutable de Hugging Face publique la etiqueta `license:apache-2.0`; si falta, aborta. La licencia del conjunto no sustituye la revisión de PII, re-anotaciones, procedencia, duplicados ni contaminación del holdout.

### Open Textbook Library — catálogo para curación por libro

Se incorpora como catálogo de descubrimiento, no como dataset con licencia común. Se priorizarán títulos con licencia CC-BY verificable en la ficha y en la fuente editorial. Se excluirán CC-NC, CC-ND y derechos de terceros no aclarados. Se conservarán autoría, edición, atribución, URL y hash.

### Common Pile — no aceptar la licencia agregada como garantía

La colección reúne fuentes de dominio público y licencias abiertas, pero cada componente mantiene sus propios términos. Además, el propio proyecto advierte que la detección automática puede asignar licencias incorrectas. Se exige revisión por fuente y documento; no se importa el agregado en bloque.

### Fuentes expresamente bloqueadas

OpenStax se bloquea: su licencia oficial es CC BY-NC-SA y sus condiciones para proyectos de IA requieren una solicitud específica. No se descargará ni entrenará con ese contenido sin autorización escrita que cubra el uso previsto.

**Estado:** Aya se adquiere como candidato, nunca como admitted. Ningún byte nuevo se cuenta como admitido hasta completar auditoría global, revisión humana, deduplicación exacta/aproximada y contaminación de holdout.


## Nueva expansión de bibliotecas — lote adicional (2026-11-06)

Se amplía el workflow de adquisición con tres fuentes nuevas, siempre como **candidatas no admitidas**:

- **Wikidata (CC0-1.0):** 5.000 registros de IDs, etiquetas y descripciones multilingües. No se incorporan textos de Wikipedia ni imágenes enlazadas.
- **PubMed / Common Pile filtrado:** hasta 5.000 artículos, pero solo si el campo por registro `metadata.license` contiene CC-BY-4.0 o CC0-1.0. Se conservan licencia, URL, autores y procedencia. BY-SA, NC, ND y desconocidas quedan fuera.
- **Stack Exchange / Common Pile:** excluido de la adquisición y de train porque CC-BY-SA-4.0 es share-alike y no está aprobado para este uso. Los 5.000 registros candidatos registrados en el run 42295370306 quedan held/excluded; aportan 0 bytes admitidos y no se readquieren sin aprobación explícita y revisión legal.

El script ahora aplica filtros de licencia por documento antes de guardar, y conserva la procedencia de cada registro. Las advertencias del proyecto Common Pile sobre posibles errores de clasificación de licencias se mantienen expresamente: estos lotes no son material entrenable hasta completar auditoría independiente.

### Grandes bibliotecas en cola, no descargadas

- **The Stack v1.1:** 6 TB de código, 193 licencias permisivas, pero cada archivo conserva su licencia original y atribución. Requiere acceso, selección por SPDX y revisión de opt-outs.
- **The Stack v2:** 67,5 TB; bloqueado hasta obtener el acuerdo de descarga masiva con Software Heritage e INRIA y cumplir sus principios de entrenamiento.

El lote anterior de adquisición (run 42294489267) descargó 25.000 filas y 105.792.783 bytes. Su manifiesto marca `training_authorized: false`; no se suma a corpus admitido.


### Bibliotecas de texto académico y manuales abiertos

Se añade una segunda pareja de catálogos de libros:

- **PressBooks filtered:** hasta 5.000 capítulos con licencia por registro CC-BY-4.0 exacta.
- **LibreTexts filtered:** hasta 5.000 secciones de libros con licencia por registro CC-BY-4.0 exacta.

Se excluyen CC-BY-SA, GFDL, NC, ND, dominio público no verificado y licencias desconocidas. Se conserva autoría, título, URL del libro y URL de la sección. La advertencia de Common Pile sobre errores de metadatos sigue vigente; estos lotes requieren revisión humana y auditoría independiente antes de admisión.


### Investigación científica de arXiv — selección por licencia de cada paper

Se incorpora `secemp9/arxiv-complete` como candidato para un piloto de 5.000 papers del config `paper_text`. La licencia del conjunto es mixta: su propia LICENSE aclara que CC0 solo cubre la capa organizativa y metadatos, no los artículos. La mayoría de papers usa una licencia arXiv no exclusiva o no tiene licencia registrada; quedan fuera. Solo se aceptan filas cuya licencia individual sea CC-BY-4.0 o CC0-1.0. Se conservarán ID, título, resumen, categoría y licencia. También se filtrarán retractaciones, plantillas TeX y textos mal resueltos.

### Exclusión territorial de Project Gutenberg

Aunque Common Pile filtra títulos marcados como dominio público según metadatos de Project Gutenberg, el propio proyecto advierte que su evaluación se basa en la ley estadounidense y que fuera de EE. UU. hay que comprobar la ley local. Por tanto, no incorporamos en bloque sus 20 GB: solo consideraremos obras cuya situación de dominio público esté verificada individualmente para la UE/España (incluida la regla de vida del autor más 70 años), o con permiso/licencia explícita válida.


### Cuarta expansión: libros académicos, OER y web con licencia CC verificada

Se añaden cuatro adquisiciones limitadas a 5.000 registros cada una, filtrando por licencia individual **CC-BY-4.0 exacta**:

- **DOAB:** libros académicos revisados por pares; la fuente declara una whitelist manual de avisos de licencia en el propio libro.
- **OERCommons:** materiales educativos, ejercicios y recursos docentes.
- **News filtered:** artículos con autor, editor/fuente y URL conservados.
- **CCCC (Creative Commons Common Crawl):** 260 GB y 51 millones de documentos declarados; Common Pile verificó manualmente dominios donde la licencia CC cubre todo el texto del dominio. Se conserva la cautela por errores residuales.

También quedan registrados para una segunda fase:

- **peS2o:** 188,2 GB de papers científicos filtrados por calidad; no se importa aún porque sus códigos `CCBY`/`CCBYSA` necesitan mapearse a la licencia exacta por documento.
- **Data Provenance Initiative filtered:** 3 GB con fuentes y licencias anotadas manualmente; pendiente de cerrar una allowlist de licencias y conservar `license_url` y `dataset_id`.

La regla no cambia: candidatos externos no suman bytes admitidos ni pueden alimentar el entrenamiento hasta superar derechos, calidad, deduplicación y contaminación del holdout.


### Resultado medido de adquisición — run 42295370306

<https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42295370306>

- 50.000 filas descargadas en 10 fuentes.
- 317.069.186 bytes en total.
- Artifact: `13541581972`.
- Manifiesto: `candidate_not_admitted`; `training_authorized=false`.

Comprobación del contenido por licencia:
- PubMed: 4.415 filas CC-BY-4.0 y 585 CC0.
- Stack Exchange: 5.000 filas CC-BY-SA-4.0 exactas, ahora reclasificadas como held/excluded por share-alike no aprobado; 0 bytes admitidos.
- PressBooks: 5.000 filas CC-BY-4.0 exactas.
- LibreTexts: 5.000 filas CC-BY-4.0 exactas.
- Wikidata: 5.000 filas CC0-1.0.
- Aya: 5.000 filas Apache-2.0.

El lote no se incorpora al entrenamiento actual ni se suma a bytes admitidos. Sigue pendiente deduplicación cruzada, revisión humana, PII, atribución, verificación legal y contaminación del holdout.


### Data Provenance Initiative — supervisión con licencias rastreables

Se añade `common-pile/data_provenance_initiative_filtered` como candidato de 3 GB / 3,51 millones de filas. La iniciativa declara anotación manual de origen y licencia, exclusión de texto generado por modelos y selección de fuentes públicas reconocidas. El nuevo importador solo acepta cadenas explícitas de licencias MIT, Apache 2.0, BSD, CC-BY-4.0 o CC0 y conserva `license_url`, `dataset_id`, idioma y procedencia. Se excluyen licencias no reconocidas y se revisan por separado contaminación de benchmarks, PII y calidad.


### Quinta expansión — Data Provenance Initiative (2026-11-06)

Se incorpora al importador un piloto acotado de hasta 5.000 registros de `common-pile/data_provenance_initiative_filtered` (3,51 M de registros anunciados; ~3,4 GB UTF-8). El proyecto DPI declara anotación manual de fuente/licencia por documento y excluye, según su metodología, texto generado por modelos y fuentes no abiertas. Su propia ficha advierte explícitamente de errores de metadatos y posible license laundering.

El filtro se aplica a `metadata.license` (que puede ser una lista), no a la licencia agregada del dataset. Solo pasan nombres de licencia de allowlist MIT, Apache-2.0, BSD-2-Clause/3-Clause, CC-BY-4.0 y CC0-1.0. Se conserva `license_url`, `dataset_id`, idioma, URL de origen y procedencia. Licencias NC, ND, share-alike, desconocidas o ausentes se rechazan. La revisión exacta de Hugging Face se fija en el manifiesto al adquirir.

**Estado:** adquisición candidata, no admitida. El dataset card y la muestra oficial confirman que el campo por registro está en `metadata.license`; no sustituyen auditoría independiente. No sumar bytes ni entrenar hasta validar el mapeo de licencias, revisar muestras por fuente, PII/calidad, deduplicar contra todo el corpus y comprobar contaminación de holdout.


## Expansión multilingüe de transcripciones — 2026-11-07

Se añade una nueva tranche de bibliotecas de texto obtenidas de transcripciones, sin descargar ni conservar audio:

- **VoxPopuli (CC0-1.0):** seis configuraciones de idioma (español, inglés, alemán, francés, italiano y polaco), hasta 10.000 transcripciones *gold* de `train` por idioma. Se proyectan las columnas `normalized_text`, `is_gold_transcript` y `language`; se excluyen audio, identificadores de hablante, género, acento y splits validation/test. El corpus completo declara 1.255.237 filas y 18 idiomas, pero la adquisición de esta tanda está limitada a 60.000 filas. [Ficha y licencia](https://huggingface.co/datasets/facebook/voxpopuli) · [Repositorio oficial y licencia CC0 de los datos](https://github.com/facebookresearch/voxpopuli).
- **LibriSpeech ASR (CC-BY-4.0):** hasta 25.000 transcripciones de `train.clean.100` y 25.000 de `train.clean.360`. Solo se proyecta la columna `text`; quedan fuera audio, IDs de hablante/capítulo y cualquier split de validación o test. Se conserva la atribución a Panayotov et al. y OpenSLR. [Ficha del dataset](https://huggingface.co/datasets/openslr/librispeech_asr) · [Licencia y splits oficiales](https://openslr.org/12/).

**Límite de esta tranche:** hasta 110.000 registros candidatos (60.000 VoxPopuli + 50.000 LibriSpeech). La descarga fija el commit SHA de cada fuente y publica SHA-256 por archivo/configuración. Los filtros de transcripción gold y de columnas se aplican antes de serializar. Son candidatos, no datos admitidos: deben superar deduplicación cruzada, auditoría de holdout, revisión humana por idioma y comprobación final de atribución/calidad. No se habilita su uso en el entrenamiento ni se suman bytes admitidos automáticamente.

Fuentes oficiales consultadas: VoxPopuli documenta CC0 para los datos y 18 idiomas con transcripción; OpenSLR declara CC BY 4.0 para LibriSpeech. La biblioteca mantiene las licencias y procedencias por fuente, sin asumir que el permiso de una fuente cubre otras.


## Tranche ampliada de corpus efectivo — 2026-11-07

La adquisición candidata se amplía con límites superiores por fuente para obtener material sustancial sin tratar el tamaño remoto como resultado:

| Fuente | Máximo candidato | Filtro | Valor esperado |
|---|---:|---|---|
| arXiv Complete paper_text | 20.000 artículos | Licencia por artículo CC-BY-4.0 o CC0; excluir licencia arXiv no exclusiva, NULL, NC, ND y BY-SA | Ciencia, matemáticas, física, informática e ingeniería |
| DOAB | 20.000 textos | CC-BY-4.0 exacto en metadatos por documento | Libros académicos revisados por pares y humanidades |
| Pressbooks | 15.000 capítulos | CC-BY-4.0 exacto por documento | Libros de texto y educación |
| LibreTexts | 15.000 secciones | CC-BY-4.0 exacto por documento | Matemáticas, ciencias e ingeniería |
| PubMed filtered | 10.000 artículos | CC-BY-4.0 o CC0 por registro | Biomedicina y ciencias de la vida |

El script fija la revisión de Hub y SHA-256 de cada salida, conserva metadatos de licencia/procedencia y mantiene todos los registros como candidate_not_admitted. La adquisición no habilita entrenamiento. Los máximos suman hasta 80.000 registros adicionales en esta tranche, no 80.000 documentos admitidos ni una estimación de bytes garantizada.

**Corrección de bloqueo:** los runs iniciales de adquisición fallaban antes de descargar datos porque las nuevas entradas de LibriSpeech/VoxPopuli contenían el literal Python true. Se corrige a True. CCCC se retira temporalmente del lote ejecutable porque el esquema público observado no muestra un campo de licencia por registro; no se permite inferir una licencia individual a partir de la colección sin una auditoría específica. El workflow se limita a pushes en main y dispone de seis horas para evitar múltiples ejecuciones por cada commit de ramas experimentales.


## Cierre de auditoría de fuentes train-scoped (2026-11-07)

La auditoría global del artefacto train-only terminó con éxito en [run 42288107561](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42288107561): 256.305 documentos elegibles para el escáner, cero coincidencias exactas con las 120 preguntas diagnósticas sintéticas, 9 hits exactos y 68 extremos de near-duplicate excluidos por el plan determinista. El corpus efectivo que el entrenamiento consumió en [run 42338551408](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42338551408) quedó en 256.237 documentos y 680.665.972 bytes. Distribución tras deduplicación: CoVoST2 240.022; Mathlib4 8.497; ScienceVerse 7.102; literatura española 606; NASA 1; Papers 9. La auditoría es heurística (SimHash) y su holdout de 120 preguntas es sintético; no sustituye benchmark externo ni revisión legal sobre derechos más amplios. Se mantiene Papers bajo autorización interna únicamente.


## Descubrimiento oficial — discursos del Parlamento Europeo (2026-11-07)

- Fuente primaria: [European Parliament Open Data API v2](https://data.europarl.europa.eu/en/developer-corner/opendata-api), endpoint /speeches.
- Alcance potencial: actividad PLENARY_DEBATE_SPEECH; la API documenta include-output=xml_fragment para incluir el texto y un filtro de idioma para las 24 lenguas oficiales de la UE.
- Derechos: la especificación de la API declara CC-BY-4.0; las [reglas oficiales de Open Data](https://data.europarl.europa.eu/en/discover/rules-on-the-european-parliaments-open-data) adoptadas el 16-12-2024 establecen CC-BY-4.0 para datos abiertos del Parlamento. No se extiende esta autorización a terceros ni a recursos sujetos al aviso legal del portal.
- **Estado:** descubrimiento/candidato, 0 descargas y 0 bytes admitidos. El endpoint es mutable; antes de staging hay que fijar consulta, schema, timestamp y SHA-256, confirmar licencia por recurso, excluir contenido de terceros y revisar PII/metadatos de oradores. Solo después se diseñará el importador train-only.


## Descubrimientos nuevos — 2026-11-08 (candidatos, no admitidos)

### German Commons: seleccionar splits reales, no `train` genérico

La ficha de [German Commons](https://huggingface.co/datasets/coral-nlp/german-commons) enumera splits por fuente con licencias diferentes. Se priorizan tres tranches separadas:

| Configuración / split | Fuente | Licencia declarada | Límite inicial |
|---|---|---|---:|
| `cultural/germanpd` | Literatura alemana de dominio público | CC0-1.0 | 5.000 |
| `political/btdrucksachen` | Publicaciones del Bundestag | CC0-1.0 | 5.000 |
| `political/germanpoliticalspeeches` | Discursos políticos alemanes | CC-BY-4.0 | 5.000 |

La ejecución anterior pidió `cultural/train`, split inexistente. La nueva adquisición usa las claves exactas y exige que **cada** registro contenga solo la URI de licencia permitida. Se conserva ID, fuente, subset, licencia, número de tokens y OCR score. Ninguna tranche es admitida hasta comprobar derechos upstream, calidad, privacidad, deduplicación y G-0.

### BOE — legislación consolidada española

La [API oficial de datos abiertos del BOE](https://www.boe.es/datosabiertos/api/api.php) ofrece legislación consolidada. Las [condiciones de reutilización vigentes desde el 28-06-2024](https://www.boe.es/informacion/aviso_legal/index.php) permiten reproducción, distribución, adaptación y extracción para fines comerciales y no comerciales, con atribución, fecha de actualización y otras obligaciones. La Biblioteca Jurídica Digital usa CC BY-NC-ND 4.0 y queda expresamente excluida; también se excluyen documentos con condiciones especiales y elementos de terceros.

No se ha descargado contenido todavía. Cada documento futuro deberá congelarse con identificador/CVE, fecha de publicación y consolidación, URL, condiciones aplicables y SHA-256. Los textos consolidados deberán conservar el aviso de que tienen carácter informativo y no se presentarán como versión oficial auténtica.

### Parlamento Europeo

La API v2 declara CC-BY-4.0 en su especificación. Sigue como candidata hasta verificar el alcance por recurso, exclusiones de terceros y privacidad; no se contabiliza ningún byte.

## Descubrimiento nuevo — EUR-Lex / CELLAR (2026-11-09)

Se registra **EUR-Lex / CELLAR** como candidato de alto valor para legislación y terminología jurídica multilingüe de la UE. No se ha descargado ningún payload y no se contabiliza ningún byte.

- **Acceso oficial:** [EUR-Lex](https://eur-lex.europa.eu/) y [CELLAR](https://op.europa.eu/en/web/cellar). CELLAR permite recuperar metadatos y documentos mediante su interfaz pública [SPARQL](https://publications.europa.eu/webapi/rdf/sparql) y su API REST; la documentación oficial describe las consultas y los enlaces de descarga. [Knowledge graph y SPARQL](https://op.europa.eu/en/web/cellar/cellar-data/metadata/knowledge-graph) · [documentación](https://op.europa.eu/en/web/cellar/documentation).
- **Derechos:** el [aviso legal de EUR-Lex](https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en) indica que, salvo especificación contraria, los documentos jurídicos publicados en EUR-Lex pueden reutilizarse con fines comerciales y no comerciales. Algunos documentos tienen condiciones especiales (por ejemplo, normas internacionales de contabilidad); el contenido de terceros y datos de personas identificables pueden requerir autorización adicional. Los metadatos se dedican a dominio público CC0-1.0; el contenido editorial, los resúmenes y los textos consolidados propiedad de la UE se licencian CC-BY-4.0. **No existe una licencia única aplicable indiscriminadamente a todo EUR-Lex.**
- **Alcance inicial propuesto:** actos jurídicos del Diario Oficial de la UE producidos por instituciones de la UE. Separar metadatos, actos, resúmenes y textos consolidados. Excluir documentos con condiciones especiales, material de terceros y recursos con derechos o privacidad no resueltos.
- **Reproducibilidad:** fijar consulta SPARQL, timestamp, IDs CELEX/ELI/CELLAR de work/expression/manifestation/item, idioma y formato; guardar SHA-256 por expresión y payload. No tratar un endpoint mutable como revisión inmutable.
- **Estado:** `candidate_discovery_only_pending_document_level_terms`; 0 descargas, 0 documentos admitidos, 0 bytes admitidos. G-0, deduplicación global, privacidad y revisión estratificada siguen siendo obligatorios.
