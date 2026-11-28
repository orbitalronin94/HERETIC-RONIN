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


## Descubrimiento y seguridad de staging — 2026-11-10

### Nuevas fuentes candidatas (sin descarga ni admisión)

1. **Common Voice Scripted Speech v27.0 (texto únicamente).** Release con corte 2026-09-11 y 295 locales. Fijar metadata en `common-voice/cv-dataset@65ca2460d5e686ea03902a932bbca09b322dc4b0` (release JSON blob Git SHA `e401c4a8e923cad5c8baacb6120c095b1e1bd561`). MDC lista CC0-1.0, pero no basta el license badge: unir `train.tsv` con `validated_sentences.tsv`, preservar `source`/dominio/ID y excluir prompts Wikipedia, terceros o procedencia desconocida. Nada de audio, `client_id`, edad, género ni acentos. Acceso MDC pendiente; 0 bytes.
2. **Tatoeba text corpus.** CC-BY-2.0-FR por defecto, CC0 para un subconjunto; el autor debe citarse por frase. Congelar export semanal, joins de licencias y enlaces de traducción con SHA-256; excluir audio, autor ausente, licencias ambiguas, material copiado/retirado y PII. Mantener cada componente de traducción en un único split. Calidad y veracidad no están garantizadas por Tatoeba. 0 bytes.
3. **World Bank Open Knowledge Repository.** Catálogo con licencias mixtas por obra: aceptar como candidatos solo CC-BY-4.0 o CC-BY-3.0-IGO exactas. Excluir NC, ND, SA, términos desconocidos y componentes de terceros; conservar atribución, handle/DOI, autor, año, publisher y avisos de traducción/adaptación. 0 bytes.
4. **Parlamento Europeo Open Data.** La regla institucional de diciembre de 2024 adopta CC-BY-4.0 para open data, pero no sustituye el chequeo por recurso, exclusión de terceros y revisión de datos personales de ponentes. El registro ya existente se mantiene en descubrimiento; no se descarga aún.

### Alerta de cuarentena pública

La run [42737780473](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42737780473) subió el directorio completo `staging/open-source-candidates/` a un artefacto de un repositorio público. El artefacto incluye payloads brutos de fuentes cuyo linaje/derechos todavía no han pasado todos los gates. Los artefactos públicos de GitHub Actions pueden descargarse sin autenticación por lectores de recursos públicos. Esto **no es una cuarentena privada**. Además, `review_candidate_samples.py` imprime extractos brutos en los logs públicos del job. No se borró el artefacto ni se canceló ningún workflow; registrar como bloqueo de seguridad antes de nuevas publicaciones de payloads no revisados. Prioridad: conservar artefactos públicos solo con manifiestos/hashes y mover payloads pendientes a almacenamiento privado o no publicarlos hasta que sus derechos estén acreditados.


### Corrección de publicación de candidatos — PR #30

La [PR #30](https://github.com/orbitalronin94/HERETIC-RONIN/pull/30) se integró en el commit [ca3fb47](https://github.com/orbitalronin94/HERETIC-RONIN/commit/ca3fb4714bbf94eb0cfe16b384ac04ef05cae3d6), validado por la [run 42830396419](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42830396419): compilación y suite de seguridad correctas, sin descargar datasets. En repositorios públicos, las futuras ejecuciones suben solo `OPEN-SOURCE-MANIFEST.json`; shards y muestras completos solo se publican si el repositorio es privado. El script de muestras deja de imprimir extractos en los logs y muestra únicamente recuentos. El trigger de push de adquisición queda limitado a `main`; los PR ejecutan solo validación.

La exposición histórica no desaparece: el artefacto [13737479716](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42737780473/artifacts/13737479716) figura con expiración **2027-02-08** en los metadatos de GitHub; los extractos también están en el log del job, pero su fecha exacta de retención no se ha verificado. No se han borrado artefactos ni cancelado workflows. La adquisición que ya se había disparado desde la rama antes de restringir el trigger ([run 42830186561](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42830186561)) continúa bajo la política de manifiesto público solamente; el push de `main` ([run 42830458157](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42830458157)) espera la exclusión mutua.


## Descubrimiento adicional — Parlamento de Austria (2026-11-10)

**Estado: discovery only; no descargar ni contar bytes todavía.**

La ficha oficial del dataset de protocolos estenográficos confirma:
- Protocolos completos del Nationalrat y Bundesrat en HTML desde la XX legislatura.
- Discursos individuales estructurados desde la XXVI legislatura.
- Los protocolos de ambos órganos son descritos como *freie Werke* y libremente utilizables sin licencia adicional. La ficha limita esta afirmación exclusivamente a esos protocolos.
- Las listas de resultados y metadatos de la API se publican bajo CC BY 4.0; separar esa licencia del texto de los protocolos.

API oficial: `POST https://www.parlament.gv.at/Filter/api/filter/data/211?js=eval&showAll=true`. Filtrar exclusivamente `NRSITZ` y `BRSITZ`. El endpoint es mutable, no una revisión inmutable.

Antes de adquirir:
1. Congelar el cuerpo POST, respuesta, timestamp, IDs de protocolo/sesión, URL HTML, tamaño y SHA-256 por documento.
2. Preservar cámara, legislatura, fecha, número de sesión, cita y procedencia.
3. Excluir adjuntos, imágenes, biografías y material no incluido en la ficha; revisar citas de terceros.
4. Auditar privacidad/PII, calidad, idioma, estructura y una muestra estratificada por cámara, legislatura y materia.
5. Ejecutar deduplicación exacta/aproximada global y contaminación de validation/test/benchmark/holdout; exigir G-0.

La fuente se añade como candidata de descubrimiento con `training_authorized=false`, `count_toward_admitted_bytes=false`, filas desconocidas y tamaño no medido. **0 bytes admitidos.**


## Descubrimiento multilingüe — Asamblea Nacional de Francia (2026-11-10)

**Estado: discovery only; no descargar ni contar bytes hasta cerrar privacidad y snapshot.**

La ficha oficial `Débats` describe el dataset `an-comptes-rendus` de la XVII legislatura: actas de sesiones, fechas, números, temas, oradores y textos de debates en francés, XML. La página oficial del Hackathon 2026 etiqueta ese recurso como **Licence Ouverte / Open Licence**. El export de la ficha consultada indica fecha 2026-11-06 y MD5 `a91c9d51574a8e89eb183a7bef74bf57`.

La licencia oficial enlazada es Etalab **Licence Ouverte v1.0**. Permite reproducir, redistribuir, adaptar y explotar comercialmente con atribución. No tiene un identificador SPDX estándar; registrar como `LicenseRef-Etalab-Open-License-v1.0`. El propio texto excluye datos personales salvo consentimiento, anonimización o base legal, y excluye derechos de terceros.

Antes de adquirir:
1. Congelar ZIP exacto, timestamp, MD5 del publicador, SHA-256 calculado, lista de miembros y IDs de registros.
2. Limitarse a `an-comptes-rendus`, XVII legislatura; no mezclar otras legislaturas ni otras colecciones.
3. Conservar atribución a Assemblée nationale, fecha de actualización, sesión, fecha, tema e identificadores.
4. Resolver speaker names y referencias a particulares bajo la cláusula de datos personales; excluir registros/campos sin base legal documentada.
5. Excluir citas/adjuntos de terceros sin derechos claros.
6. Validar XML, codificación, calidad, PII y seguridad; auditar muestra estratificada.
7. Deduplicar contra toda la biblioteca y holdouts y superar G-0.

No se ha descargado nada: filas desconocidas, 0 bytes staged y 0 bytes admitidos. `training_authorized=false`.


## Nuevos descubrimientos jurídicos y adquisición — 2026-11-11

### BOE — legislación consolidada (candidato)

- Fuente primaria: [API oficial](https://www.boe.es/datosabiertos/api/api.php); endpoint objetivo: /datosabiertos/api/legislacion-consolidada.
- Condiciones de reutilización AEBOE, resolución 27-06-2024: permiten uso comercial y adaptación con atribución. Registro local LicenseRef-BOE-Reuse-2024; no inventar SPDX.
- Excluir Biblioteca Jurídica Digital (CC BY-NC-ND 4.0 salvo excepción expresa), BORME, marcas, elementos compartidos con terceros y documentos con condiciones especiales.
- Texto consolidado siempre informativo; conservar atribución BOE y fecha de actualización.
- Estado: discovery-only, 0 descargas y 0 bytes.

### Légifrance / DILA — textos jurídicos (candidato)

- Fuente primaria: [Open data y API](https://www.legifrance.gouv.fr/contenu/pied-de-page/open-data-et-api), estable desde 04-04-2023.
- Licence Ouverte / Etalab 2.0, registrada como LicenseRef-Etalab-Open-License-2.0; CGU API permiten uso comercial, requieren PISTE/OAuth y aplican cuotas.
- Primera fase solo textos legislativos, códigos y reglamentos bajo responsabilidad de DILA. Jurisprudencia excluida por privacidad/terceros.
- Estado: discovery-only; sin credenciales PISTE ni snapshot, 0 descargas y 0 bytes.

### Bloqueos explícitos

- **Bundestag:** XML/JSON disponibles, pero sin licencia explícita del payload en la página oficial consultada. No adquirir.
- **GovInfo:** 17 U.S.C. §105 solo cubre obras federales estadounidenses que cumplan la definición legal; GovInfo advierte de contenido de terceros. No staging hasta revisión territorial España/UE y derechos por documento.

### Última ejecución

[Run 42976034496](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42976034496) — cancelado al límite de 360 minutos. Grupo 0/4:

- FineWeb-Edu: 100.000 filas, 428.092.222 bytes JSONL.
- Aya: 25.000 filas, 46.109.328 bytes JSONL.
- VoxPopuli alemán: 20.000 filas, 9.857.291 bytes JSONL.
- Total efímero: 145.000 filas, 484.058.841 bytes JSONL; 71.526 filas rechazadas por filtros de adquisición.
- arXiv y LibriSpeech clean.100 descartaron sus shards parciales por no alcanzar el mínimo de filas.
- Artefacto [13856681975](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42976034496/artifacts/13856681975): manifiesto de 2.190 bytes, SHA-256 ZIP 94863a5c62a333e2bb7fe94389e332ba0d237f7d8211264e23cc739815694587; SHA-256 del JSON b9fd726daa029e64edb8dcf1642c36d71a950506b2e1bba1d6a7ad5a1ef9c8d8.
- El payload no se retuvo (0 bytes); los hashes de shards no se pudieron verificar contra archivos recuperados.
- Near-dedup global, holdout, G-0, auditoría humana estratificada y escaneo completo de privacidad/secretos/malware siguen pendientes. 0 bytes admitidos.

Siguiente paso: reducir la carga por ejecución mediante ocho grupos deterministas; obtener snapshots de BOE y, si se autoriza el acceso, Légifrance; y construir una auditoría global que realmente incluya los candidatos antes de considerar cualquier admisión.


## Fuentes nórdicas — 2026-11-11

### Stortinget — candidato noruego

- Fuente: [data.stortinget.no](https://data.stortinget.no/), API XML/JSON.
- Las condiciones remiten a la licencia vigente NLOD; el enlace oficial lleva a NLOD 2.0. Registro local LicenseRef-NLOD-2.0. Permite uso comercial y modificación/redistribución, con atribución y sin tergiversar los datos.
- Excluir datos personales sin base jurídica, confidenciales, terceros no licenciables y marcas. Excluir endpoints de personas, biografías, fotos, listas de oradores y aportaciones de audiencias.
- Respetar 100 llamadas/minuto. El servicio solo muestra la versión vigente; congelar consultas y snapshots por registro.
- Estado: discovery-only, 0 descargas y 0 bytes.

### Folketinget — actas danesas bloqueadas

- Fuente: [Folketinget Open Data](https://www.ft.dk/dokumenter/aabne_data), OData v3, XML/JSON.
- Los términos generales permiten uso comercial y modificación, pero las actas tienen cláusula específica de reproducción, reserva derechos sobre colecciones de intervenciones de cada orador y limitan cambios a lo necesario para el uso permitido.
- Las actas provisionales pueden revisarse sin marcar cada cambio; hay que conservar y mostrar estado provisional/final. PDFs, imágenes y anexos de terceros no quedan automáticamente cubiertos.
- Estado: bloqueado hasta que se determine si extracción, normalización/tokenización, agregación y entrenamiento interno caben en esas condiciones. 0 descargas y 0 bytes.



## Descubrimiento multilingüe y jurídico — 2026-11-12

### ILO Research Repository — candidato, no descargado

- Fuente: [ILO Research Repository](https://researchrepository.ilo.org/esploro/); política primaria: [Rights and permissions](https://www.ilo.org/rights-and-permissions).
- Las publicaciones producidas desde **2023-05-03** son CC BY 4.0 por defecto, salvo que la página de copyright de la obra indique otra licencia. Las obras anteriores no heredan automáticamente esa licencia.
- Ámbitos potenciales: economía laboral, empleo, protección social, migración, formación, seguridad y salud laboral, relaciones industriales y estadísticas. El repositorio contiene obras en inglés, francés y español; el idioma debe preservarse por documento.
- Excluir co-publicaciones con otros términos, componentes de terceros, microdatos restringidos, fotografías CC BY-NC-ND, audio/vídeo CC BY-ND y emblemas.
- No se ha identificado todavía un contrato público de export/API reproducible. No se ha descargado nada: 0 filas, 0 bytes.

### Australia — Federal Register of Legislation — candidato, no descargado

- Fuente: [Federal Register](https://www.legislation.gov.au/) y [términos oficiales](https://www.legislation.gov.au/terms-of-use).
- CC BY 4.0 por defecto para el contenido del registro, salvo Commonwealth Coat of Arms y avisos específicos. Permite adaptación y uso comercial con atribución y fecha de descarga.
- Cada instrumento debe revisarse individualmente: el registro alberga documentos de múltiples agencias/autores y el contenido de terceros exige permiso. Ejemplo de exclusión: F2014L01500 contiene una licencia CC BY-NC 4.0.
- Fijar instrumento, versión (as-made/compilation), fecha, URL y SHA-256 por documento. No se ha descargado nada: 0 filas, 0 bytes.

### Canadá — Justice Laws bulk XML — bloqueado

- El [catálogo Open Government Portal](https://open.canada.ca/data/en/dataset/2f4bb174-b2e7-4fb2-a7a1-a313507acbc6) etiqueta el paquete bulk XML con Open Government Licence — Canada 2.0.
- El [Reproduction of Federal Law Order SI/97-5](https://laws-lois.justice.gc.ca/PDF/SI-97-5.pdf) permite reproducir leyes y consolidaciones sin permiso, con diligencia sobre la exactitud y sin presentar la reproducción como versión oficial; no expresa claramente derechos de adaptación.
- Bloqueado hasta aclarar si OGL Canada cubre el payload XML y si la transformación prevista para entrenamiento está autorizada. Excluir información personal, derechos de terceros y símbolos oficiales.
- No se ha descargado nada: 0 filas, 0 bytes; `training_authorized=false`.

## 2026-11-13 — revisión diaria (runs 92–93)

### Admisiones

- Nuevas admisiones: **0 documentos / 0 bytes**.
- Total acumulado verificado: **703.593.871 bytes**, 260.971 documentos; progreso **0,140719 %** hacia 500 GB. Referencia: [auditoría source-scoped 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447).

### Lotes

- [Run 92, grupo 7/8](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43298985874): 35.000 filas / 945.924.928 bytes JSONL efímeros. VoxPopuli EN 20.000 filas (9.695.378 bytes; `16d055db8451e1f247907265f38b5835d00f766e1cf9193438c93792d29a159f`); OpenThoughts3 15.000 (936.229.550 bytes; `c23a18348f6478acac2ed0549df655a1c3f433d6f6763d93e9892e877f3228a9`). LibreTexts 20.532/25.000 y Spanish-PD-Books 978/1.000 descartados. Manifiesto artifact [13983600253](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43298985874/artifacts/13983600253), ZIP SHA-256 `adc350c45bf60c66e1e35f62dcbc0fb449aad312ddc2e8bcf1d72983f9c98ebd`, JSON SHA-256 `c4d9055db2c098b1f05c6333c60df18636f74e125d65e7ea7ba57881c6296645`.
- [Run 93, grupo 6/8](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43383222519): 73.736 filas / 807.461.935 bytes JSONL efímeros. Los tres shards válidos son idénticos por hash, filas y bytes a run 87: 0 contenido único adicional. Spanish-PD-Books 954/1.000 y German Commons 0/500 descartados. Manifiesto artifact [14018112522](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43383222519/artifacts/14018112522), ZIP SHA-256 `79b3e47ad7467370f611b979bd7294a1022f6f114eca6ce4b59d075218965129`, JSON SHA-256 `59e692299981eca4403fa3836b7f1c4e38469315286e41620f0fd35055710d77`.

Ambos runs retuvieron solo manifiestos: 0 bytes de payload, 0 staged, 0 admitidos. Bytes remotos/comprimidos desconocidos; hashes de shards no recalculables tras perderse el runner. G-0, near-dedup global, holdout, privacidad, malware y revisión humana siguen pendientes.

### Nuevas fuentes en discovery-only

- Eurostat: política de reutilización comercial con atribución, pero excepciones por titularidad de terceros, co-publicaciones, países y series comerciales concretas. API mutable sin historial de versiones; cualquier futuro lote debe congelarse como snapshot con consulta, dataflow, DSD, codelists, timestamp y SHA-256. No se adquirió; API anunciada en mantenimiento el 13/11 de 14:00 a 23:00 CET.
- OECD: limitar a publicaciones escritas desde 2024-07-01 y confirmar CC-BY-4.0 en cada copyright page. Excluir obras con excepciones, co-publicaciones o material de terceros.
- OpenThoughts3: held y desactivado. La licencia Apache del dataset agregado no limpia los derechos de las preguntas upstream; no reacquirir sin procedencia/licencia por fila.

### Medidas operativas

- Rotación corregida a `((day_of_year - 1) * 4 + tranche_slot) % 8`: ocho grupos en 48 horas sin solapamiento.
- Eliminado el trigger `push` de adquisición; los PR solo validan.
- En repositorio público, no descargar sin el secreto Actions `HERETIC_STAGING_PASSPHRASE`. Sin él, el workflow registra `blocked_storage_gate` y cero bytes. Con él, publica un artefacto GPG AES-256 cifrado y elimina plaintext del runner. Retención de artefactos: 90 días. No se ha creado ni cambiado el secreto.

### Pendiente

1. Configurar el almacenamiento cifrado y recuperar los artefactos para revisión en un entorno controlado.
2. Ejecutar near-dedup contra todo el corpus y los splits protegidos, auditoría estratificada real y G-0.
3. Mantener todos los candidatos fuera de `training_eligible` hasta que todos los gates pasen.


**Fortaleza del secreto de staging:** en repositorios públicos el workflow solo descarga si `HERETIC_STAGING_PASSPHRASE` tiene al menos 32 caracteres; GPG usa AES-256, SHA-512 S2K y control de integridad. Sin ese mínimo, el lote se bloquea antes de descargar.


## Revisión de curación — 2026-11-14

- [Run 102](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43568604566): preflight correcto, adquisición bloqueada por almacenamiento. HERETIC_STAGING_PASSPHRASE no estaba presente o no alcanzaba 32 caracteres. 0 filas, 0 bytes descargados, 0 staged y 0 admitidos. Manifiesto [14103293875](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43568604566/artifacts/14103293875), ZIP SHA-256 88c9315417f8f9cb6531c0ed8df6b7b9bb79d240bae86163c94bef75753fb5da; JSON SHA-256 0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7.
- EuroVoc 4.24 queda discovery-only hasta confirmar licencia de la distribución actual; la licencia CC0 observada en distribuciones archivadas de 2020 no se extrapola.
- HUDOC queda bloqueado por sus condiciones de reutilización no comerciales; solo se reconsiderará con permiso previo escrito que cubra expresamente entrenamiento y adaptación.
- No reanudar adquisición hasta disponer de almacenamiento durable privado o cifrado; mantener G-0, near-dedup, holdout, privacidad y revisión humana sin excepciones.


## 2026-11-14 — EEA Datahub / FAO

- EEA Datahub: candidatos WISE Statistics–Nutrients (DOI 10.2909/c6e353a2-c004-41eb-b0c1-5a2a1da5ef3b) y WEI+ 2023 (DOI 10.2909/3c13b52b-36e5-44bc-a07f-8389d43dfd3b), ambos con metadatos que declaran CC-BY 4.0 y EEA como titular. Pendiente upstream WISE SoE/WISE-6, acuerdos de países, distribuciones y hashes, calidad, privacidad y G-0. 0 descargas.
- FAO Publications: bloqueado por los términos por defecto de uso no comercial y necesidad de permiso para reproducción/adaptación. No descargar sin autorización individual compatible.
- Ningún registro se marca training_eligible; 0 bytes admitidos nuevos.


- [Run 101](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43496984977), grupo 3/8: el preflight bloqueó antes de descargar por falta de HERETIC_STAGING_PASSPHRASE (mínimo 32 caracteres). 0 filas, 0 bytes remotos/descargados/comprimidos medidos, 0 staged y 0 admitidos. Artefacto [14071464119](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43496984977/artifacts/14071464119): ZIP 653 bytes, SHA-256 cddd161c01910852db6083f15ed157b2b4c6e2ad38308fa5ddc070b9767205b6; JSON interno 871 bytes, SHA-256 2829acd2e3d3d88cd5d58aa573fff9cfc9c9067d45dc1035e09e1c190c488b26. Hash del ZIP recalculado localmente y coincidente con GitHub; no hubo payload ni shards.


## 2026-11-15 — legislación británica y documentos del Consejo de la UE

- **legislation.gov.uk** añadido como candidato discovery-only: OGL-UK-3.0 para el texto legislativo cubierto por el aviso del sitio, con exclusiones de datos personales, derechos de terceros y excepciones por activo. EUR-Lex-derived material queda separado. Conservar versión/fecha, XML exacto y atribuciones especiales de Westlaw/British History Online. La API y los formatos XML están documentados oficialmente; respetar la fair-use policy y los límites de acceso.
- **Consejo de la UE / public register** añadido como candidato discovery-only bajo Decision (EU) 2017/1842 para documentos públicos producidos/held por el Consejo. La reutilización es comercial y no comercial con atribución, pero se excluyen derechos de terceros y restricciones de acceso de Estados miembros; confirmar condiciones adicionales y alcance de adaptación/training por documento. Privacidad y seguridad siguen aplicando.
- No se descargó ninguno de los candidatos. Ambos tienen `training_authorized=false` y `count_toward_admitted_bytes=false`.
- [Run 43687908071](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43687908071): grupo 1/8 bloqueado antes de descargar por falta de `HERETIC_STAGING_PASSPHRASE` (mínimo 32 caracteres). 0 filas, 0 bytes descargados/staged/admitidos. Artifact [14150964444](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43687908071/artifacts/14150964444), ZIP SHA-256 `a2bea5f0df4fdf616328872d3774265066685b7afea70ade5ef5db260dfc516d`; JSON SHA-256 `5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437`.
- Nuevas admisiones: **0 bytes**. Total: **703.593.871 bytes / 260.971 documentos**; progreso **0,140719 %** de 500 GB. G-0, near-dedup global, holdout, privacidad, seguridad y revisión humana siguen obligatorios.


## 2026-11-15 — European Parliament Think Tank / EPRS

- Candidato discovery-only limitado a publicaciones con declaración CC-BY-4.0 en la página individual y titularidad de la UE. No usar el aviso legal general como licencia universal.
- Preservar código EPRS, autores, fecha, DOI/ISBN, idioma, aviso exacto, PDF/HTML y SHA-256. Excluir figuras/tablas/anexos de terceros sin derechos independientes, material con términos no comerciales/reproducción limitada y datos personales no autorizados.
- Ejemplos oficiales consultados: EPRS_ATA(2025)769585 y EPRS_BRI(2026)789334. No se descargaron.
- `training_authorized=false`, `count_toward_admitted_bytes=false`; pendientes auditoría por obra, muestras, privacidad, near-dedup y G-0.


## 2026-11-16 — Open Research Europe y run 117

### Open Research Europe — candidato discovery-only

- Fuente: [Open Research Europe](https://open-research-europe.ec.europa.eu/); políticas: [editorial](https://ore.eu/editorial-policies/), [publicación](https://ore.eu/how-publishing-works), [guía de artículos](https://ore.eu/article-guidelines).
- La plataforma publica artículos bajo CC BY, pero la versión exacta puede variar y se muestra debajo del resumen. Solo admitir como candidato los artículos cuya página individual declare expresamente **CC-BY-4.0** y nombre al titular. El copyright suele permanecer en el autor o su institución.
- Ámbitos: ciencias naturales, ingeniería/tecnología, medicina, agricultura/veterinaria, ciencias sociales y humanidades. Preservar idioma real por versión; no inferir cobertura multilingüe.
- Las figuras, tablas, citas extensas, fotografías, mapas, anexos, suplementos y datos subyacentes pueden tener licencias distintas. No heredarles la licencia del artículo; exigir revisión independiente.
- ORE publica antes de la revisión abierta por pares. Solo considerar versiones con revisión completada y resultado aprobado; mantener en hold los artículos awaiting peer review, rechazados, con editorial note sin resolver, corregidos, retirados o retractados. Preservar DOI, versión, estado de revisión e historial.
- Para cada artículo: DOI/version DOI, código/versión, autores, fecha, copyright page, licencia exacta, idioma, URL exacta de HTML/JATS/PDF, timestamp UTC, bytes y SHA-256. Revisar PII, consentimiento y ética, especialmente en medicina y estudios con personas.
- Estado: discovery-only, 0 descargas, filas y bytes desconocidos; `training_authorized=false`, `count_toward_admitted_bytes=false`. G-0, deduplicación global y revisión humana pendientes.

### Run 117 — 2026-11-16

[Run 43821600133](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43821600133), grupo 5/8, terminó correctamente solo porque registró el bloqueo de almacenamiento. El secreto `HERETIC_STAGING_PASSPHRASE` faltaba o tenía menos de 32 caracteres. No contactó fuentes: 0 filas, 0 bytes remotos/descargados medidos, 0 JSONL, 0 staged y 0 admitidos. Artefacto [14204298738](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43821600133/artifacts/14204298738), 653 bytes; digest SHA-256 de metadatos GitHub `48650002b2d9f35b79cfb96df40186235259ce507596d35681489879abd7ca0f`, no recalculado independientemente.

Total admitido: **703.593.871 bytes / 260.971 documentos**, **0,140719 %** de 500 GB. Nuevas admisiones: **0**.


## 2026-11-16 — CORDIS (candidato discovery-only)

- Fuente: [CORDIS](https://cordis.europa.eu/), gestionado por Publications Office de la UE. El aviso legal vigente indica CC-BY-4.0 para contenido editorial propiedad de la UE salvo aviso distinto; aplica la Decisión 2011/833/UE. [Aviso legal](https://cordis.europa.eu/about/legal) · [Decisión 2011/833/UE](https://eur-lex.europa.eu/eli/dec/2011/833/oj/eng).
- Alcance candidato: solo noticias y *Thematic Packs* editoriales con titularidad de la UE y licencia confirmada por elemento. Excluir project-results, abstracts/deliverables/reportes aportados por beneficiarios salvo autorización específica del grant, terceros, material multimedia, logos/marcas y contenido confidencial.
- CORDIS publica contactos de participantes en proyectos; excluir nombres, emails, teléfonos y demás PII de esos registros. El portal ofrece UI ES/DE/EN/FR/IT/PL, pero la lengua real y disponibilidad de cada artículo deben verificarse. No incluir traducciones automáticas sin revisar términos de eTranslation.
- Congelar ID/URL, autores, fecha, versión, copyright notice, idioma, HTML/payload exacto, timestamp UTC, bytes y SHA-256. Auditoría de muestras, seguridad, privacidad, near-dedup global y G-0 obligatorios.
- Estado: discovery-only, no descargado, filas/bytes desconocidos; `training_authorized=false`, `count_toward_admitted_bytes=false`.


## 2026-11-17 — PLOS y reconciliación de runs 120/121

- **PLOS** añadido como candidato discovery-only para artículos cuya propia página declare exactamente CC-BY-4.0. Se usará Solr Search API para descubrir DOI y JATS XML para TDM; límites oficiales: 100 filas/consulta, 10 consultas/minuto, 300/hora y 7.200/día. Excluir licencias genéricas/ambiguas, NC/ND/SA, componentes de terceros no despejados, datasets/suplementos con licencia independiente y artículos retracted/withdrawn/removed. Revisar PII clínica, consentimiento y ética. Preservar DOI/version, autores, titular, copyright page, idioma, URL XML, timestamp, bytes y SHA-256. Evidencia: [licencias PLOS](https://journals.plos.org/plosone/s/licenses-and-copyright), [TDM](https://api.plos.org/text-and-data-mining.html), [API FAQ](https://api.plos.org/solr/faq/). No se descargó; training_authorized=false, count_toward_admitted_bytes=false.
- **Run 120** ([43970081452](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43970081452), grupo 7/8) y **run 121** ([44045933438](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44045933438), grupo 1/8) terminaron correctamente solo al registrar blocked_storage_gate. El secreto HERETIC_STAGING_PASSPHRASE faltaba o era menor de 32 caracteres. Ambos manifiestos dicen payload_downloaded=false, training_authorized=false, 0 filas y 0 bytes de payload. No se midieron bytes remotos/comprimidos.
- Run 120: artifact [14276384265](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/43970081452/artifacts/14276384265), ZIP 653 bytes, SHA-256 5ccaf40cebdf09513fe878878c686cd2c3e51307e81877c75db01e48ed52899b; JSON interno 871 bytes, SHA-256 3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992.
- Run 121: artifact [14312065087](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44045933438/artifacts/14312065087), ZIP 653 bytes, SHA-256 bd558141f5e6d4f3375aaba4fea21c00a0b70733c9bfeea2d0711c70c1a6e046; JSON interno 871 bytes, SHA-256 5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437. Los ZIP y JSON se descargaron y los hashes se recalcularon; los ZIP coinciden con los digests de GitHub.
- Total admitido sin cambios: **703.593.871 bytes / 260.971 documentos**, **0,140719 %** de 500 GB; referencia [auditoría source-scoped 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). Cero admisiones nuevas.


## Descubrimiento de fuentes — 2026-11-18

### WIPO Publications — candidata por obra

Se registra el catálogo de publicaciones de la OMPI para selección estricta por obra. La política de acceso abierto de WIPO declara CC BY 4.0 para muchas publicaciones nuevas, salvo avisos más restrictivos; los avisos individuales consultados de *WIPO IP Facts and Figures 2024* (10.34667/tind.57723), *World Intellectual Property Report 2024* (10.34667/tind.49284) y *A Primer on Technology Transfer in the Field of Biotechnology* (10.34667/tind.50126) muestran CC-BY-4.0. Solo se considerarán publicaciones cuyo aviso individual confirme la licencia y la titularidad de WIPO. Se excluyen emblemas/logos y elementos de terceros no despejados. No se ha descargado nada; queda pendiente snapshot, revisión por idioma/formato, privacidad, calidad, near-dedup global y G-0. Registro: `WIPO:online-publications-item-level-CC-BY-4.0`.

### WIPO Lex — bloqueada

Los términos oficiales limitan los textos jurídicos y traducciones a uso académico, de investigación y no comercial; los juicios no pueden adaptarse ni usarse comercialmente. También prohíben consultas automatizadas, adquisición/descarga masiva y scraping. No se harán consultas ni descargas automáticas. Solo se reconsiderará con permiso escrito de WIPO y de los titulares originales que cubra expresamente adaptación, uso comercial y entrenamiento. Registro: `WIPO Lex:IP-legal-texts-translations-and-judgments`, estado bloqueado.

### Runs 123 y 124

- [Run 123](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44177892230), grupo 3/8: storage gate bloqueado, 0 filas, 0 bytes descargados/staged/admitidos. ZIP [14370333374](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44177892230/artifacts/14370333374), SHA-256 `f6099c982aa2fe7a1ab0500f6fac06279223a46b59757849a8fdc7aed01cc4a8`; manifiesto JSON SHA-256 `2829acd2e3d3d88cd5d58aa573fff9cfc9c9067d45dc1035e09e1c190c488b26`.
- [Run 124](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44262175192), grupo 5/8: storage gate bloqueado, 0 filas, 0 bytes descargados/staged/admitidos. ZIP [14409340141](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44262175192/artifacts/14409340141), SHA-256 `0f4c06392971fb32a751e5878d6737deed43aa98196b002ff637ccf58ae7a650`; manifiesto JSON SHA-256 `0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7`.

En ambos runs el secreto `HERETIC_STAGING_PASSPHRASE` faltaba o era demasiado corto. No se contactó con fuentes para descargar payloads. El inventario admitido sigue en 703.593.871 bytes y 260.971 documentos; admisiones nuevas: cero.


## Canada Justice Laws — revisión de derechos 2026-11-19

La entrada existente se reclasifica de bloqueada a **candidate discovery-only**. La ficha oficial del recurso “Consolidated federal Acts and regulations – Bulk XML” (dataset `2f4bb174-b2e7-4fb2-a7a1-a313507acbc6`) identifica el recurso y declara Open Government Licence – Canada. El repositorio oficial enlazado, `justicecanada/laws-lois-xml`, está fijado en el commit `855cdfc65207a6906c414e09a77d7f93267c5356`; su `LICENSE.md` declara la misma OGL. La OGL Canada v2.0 permite copia, modificación, adaptación, traducción y uso comercial con atribución, y excluye PII, derechos de terceros y símbolos oficiales. La Reproduction of Federal Law Order SI/97-5 exige exactitud y que la reproducción no se presente como versión oficial.

- Alcance futuro: únicamente XML de Acts y Regulations en inglés/francés en el commit fijado.
- Excluir DTD/XSLT/lookup, código, PDFs, logos, PII, terceros y avisos diferentes.
- Preservar IDs, citas, títulos, idioma y fechas de consolidación/actualización.
- Snapshot exacto, SHA-256 por archivo, XML seguro sin XXE, privacidad, malware, calidad, muestra estratificada, deduplicación global y G-0 pendientes.
- No descargado; `training_authorized=false`, `count_toward_admitted_bytes=false`, 0 bytes admitidos.
- Evidencia primaria: [ficha del recurso](https://open.canada.ca/data/dataset/2f4bb174-b2e7-4fb2-a7a1-a313507acbc6), [OGL Canada v2.0](https://open.canada.ca/en/open-government-licence-canada), [LICENSE.md en commit fijado](https://raw.githubusercontent.com/justicecanada/laws-lois-xml/855cdfc65207a6906c414e09a77d7f93267c5356/LICENSE.md), [Reproduction of Federal Law Order](https://laws-lois.justice.gc.ca/eng/regulations/SI-97-5/page-1.html).

## Adquisiciones 128/129 — 2026-11-19

Runs [128](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44394965672) y [129](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44482327436) terminaron al registrar `blocked_storage_gate`: secreto `HERETIC_STAGING_PASSPHRASE` ausente o menor de 32 caracteres. Cada uno produjo únicamente manifiesto de 871 bytes en ZIP de 653 bytes. No se descargó payload; bytes remotos y comprimidos no medidos; 0 filas, 0 staged, 0 admitidos. Los hashes recalculados están en el registro y el inventario. No hay shards ni hashes de shards.


## Open Book Publishers — candidata por obra 2026-11-19

Añadida al registro como **candidate discovery-only**. La editorial tiene más de 450 títulos académicos y declara revisión por pares, pero los autores eligen la licencia de cada obra. Solo considerar títulos con aviso individual exacto CC BY 4.0.

Ejemplos comprobados en páginas/front matter de la propia editorial:
- Ovid, *Amores (Book 1)* — DOI 10.11647/OBP.0067, CC BY 4.0, inglés, ISBN XML.
- Diderot, *Rameau's Nephew / Le Neveu de Rameau* — DOI 10.11647/OBP.0098, CC BY 4.0, inglés/francés, ISBN XML.
- *Engaging Researchers with Data Management* — DOI 10.11647/OBP.0185, CC BY 4.0, ISBN XML.

La licencia del catálogo no se hereda: los MARC records de OBP son CC BY-SA 4.0 y quedan excluidos; Thoth CC0 es metadata, no texto de libro. Excluir NC/ND/SA, capítulos con derechos distintos, fair-use excerpts, citas/figuras/fotos/mapas/audio/vídeo/portadas/suplementos de terceros sin clearance independiente. No adquirir PDF/EPUB/XML hasta fijar edición y hash y completar revisión de privacidad, seguridad, calidad, muestra estratificada, deduplicación global y G-0. Cero payload adquirido, cero bytes admitidos; `training_authorized=false`.

Evidencia: [política editorial](https://www.openbookpublishers.com/publish-with-us/information-for-authors), [Ovid](https://www.openbookpublishers.com/books/10.11647/obp.0067), [Diderot bilingüe](https://www.openbookpublishers.com/books/10.11647/obp.0098), [Engaging Researchers](https://books.openbookpublishers.com/10.11647/obp.0185.07.pdf), [licencias de registros MARC/Thoth](https://www.openbookpublishers.com/libraries/marc-records).
 
## World Bank Data Catalog — candidata de datos estructurados (2026-11-20)

**Discovery-only; no descargada ni admitida.** La licencia por defecto para datasets del Banco Mundial es CC BY 4.0 salvo que el propio registro indique otra cosa. El catálogo también incluye ODbL, Microdata Research License, datasets de terceros, externos, custom y restringidos; por tanto, no se puede tratar el catálogo como una licencia global.

Solo evaluar datasets de titularidad del Banco Mundial cuando tanto los metadatos del dataset como los del recurso declaren exactamente CC-BY-4.0. Excluir ODbL/share-alike, microdatos y registros individuales, Microdata Research License, restricciones, terceros no despejados y cualquier licencia ausente o ambigua. Fijar dataset ID y versión, resource ID y versión, URL, timestamp y SHA-256. Preservar la atribución requerida por el Banco Mundial; revisar lineage, PII, seguridad, calidad, idioma, duplicados y G-0 global antes de admitir. No inferir multilingüismo del catálogo: registrar el idioma de cada recurso.

Evidencia oficial: [licencias](https://datacatalog.worldbank.org/public-licenses), [términos](https://www.worldbank.org/ext/en/legal/terms-conditions/datasets), [API](https://ddh-openapi.worldbank.org/docs/index.html), [guía](https://datacatalog.worldbank.org/getting-started), [FAQ](https://datacatalog.worldbank.org/faq). El registro queda en data/sources/registry.json como candidate_discovery_only, training_authorized=false y cero bytes admitidos.



## OECD Data Explorer — datos SDMX, discovery-only (2026-11-21)

**Candidata multidominio; 0 descargas, 0 filas y 0 bytes admitidos.** La OCDE permite la reutilización de sus datos para cualquier finalidad, incluso comercial, salvo restricciones adicionales o derechos de terceros. La política no equivale a una licencia general sobre todo el contenido del portal: la propia OCDE declara que no garantiza poseer/controlar todos los derechos. Solo se evaluarán series en las que los metadatos y la pestaña *source* acrediten derechos de OECD para todas las observaciones y ausencia de restricciones adicionales. Las series mixtas/de terceros sin autorización independiente, confidenciales, personales o de titularidad incierta se excluyen.

- Fuente de términos: https://www.oecd.org/en/about/terms-conditions.html (apartado 3, Data); no se asigna SPDX porque no es una licencia CC estándar.
- API: https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html; SDMX REST con estructura y datos consultables y formatos CSV/JSON/XML.
- Control de carga: límite actual publicado de 60 descargas/hora; no usar VPN ni fuentes anonimizadas; emplear contentconstraint, cache y consultas acotadas: https://www.oecd.org/en/data/insights/data-explainers/2024/11/Api-best-practices-and-recommendations.html.
- Antes de descargar: fijar agencia/dataflow y versiones, DSD, codelists, ValidFrom, consulta/dimensiones, formato, timestamp UTC, longitud y SHA-256; conservar cita y fuente por serie.
- Pendientes: rights check por serie, snapshot, calidad, privacidad/PII, malware/secretos, deduplicación exacta y aproximada contra todos los splits, contaminación holdout y G-0. Mantener training_authorized=false y count_toward_admitted_bytes=false.

### Runs 137–138: bloqueo de almacenamiento

- Run 137, grupo 7/8: https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44813247702 — artifact 14667188891, ZIP 653 bytes, SHA-256 a93086b9570d214b0036a5cfb9c7b2a8c5711a041ced85b175ed8a46c88f71ff; manifiesto 871 bytes, SHA-256 3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992.
- Run 138, grupo 1/8: https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/44881057593 — artifact 14697991415, ZIP 653 bytes, SHA-256 5941156dc57a7e31ad2dab81621f7344a9a6748e45ace8c73040f434d75db0f7; manifiesto 871 bytes, SHA-256 5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437.

Ambos preflights finalizaron correctamente pero el secreto HERETIC_STAGING_PASSPHRASE faltaba o tenía menos de 32 caracteres. No se contactó con fuentes para descargar payload; 0 filas, 0 bytes remotos/descargados medidos, 0 staged y 0 admitidos. El job de validación fue omitido en los eventos programados. El inventario sigue en **260.971 documentos / 703.593.871 bytes (0,140719 % de 500 GB)** según la auditoría source-scoped [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447).


## Statistics Canada — estadísticas agregadas bilingües, discovery-only (2026-11-21)

**Candidata; 0 descargas, 0 filas y 0 bytes admitidos.** La Statistics Canada Open Licence concede derechos mundiales y permite reproducción, distribución, venta y adaptación de los resultados no confidenciales cuando Statistics Canada es titular o licenciatario de todos los derechos. No es una licencia CC/SPDX. La licencia excluye los derechos de terceros, que permanecen en sus titulares. Solo se evaluarán tablas agregadas con titularidad de Statistics Canada acreditada por producto. Aunque la definición general menciona PUMF, la política del proyecto excluye microdatos y registros de personas/hogares/empresas por privacidad y riesgo de reidentificación.

- Derechos y alcance: https://www.statcan.gc.ca/en/terms-conditions/open-licence y FAQ https://www.statcan.gc.ca/en/terms-conditions/open-licence-faq.
- API: WDS JSON, SDMX REST, full-table CSV/SDMX y Delta Files: https://www.statcan.gc.ca/en/developers/wds y https://www.statcan.gc.ca/en/developers.
- El WDS publica actualizaciones diarias; la guía documenta PID, metadata de cubos/series, releaseTime, issueDate, code sets y límite de 25 solicitudes/s por IP: https://www.statcan.gc.ca/en/developers/wds/user-guide.
- Preservar el aviso exacto de fuente y el aviso de adaptación; excluir material de terceros, confidencial, granular o con riesgo de divulgación; no reidentificar ni usar logos o símbolos oficiales.
- Pendientes: rights check por producto, snapshot/hash, calidad, idioma EN/FR real, privacidad, malware/secretos, deduplicación global y contaminación de holdout/G-0. Mantener training_authorized=false y count_toward_admitted_bytes=false.

No se ha descargado contenido. No se cuentan tamaños anunciados, metadatos de catálogo ni bytes de manifiestos como admisión. El inventario sigue en **260.971 documentos / 703.593.871 bytes**, **0,140719 %** de 500 GB.


## ILOSTAT — estadísticas agregadas y diccionarios, discovery-only (2026-11-22)

**Candidata multidominio y trilingüe; 0 descargas, 0 filas y 0 bytes admitidos.** La política de derechos de ILO cubre bajo CC BY 4.0 las bases de datos, datasets y metadatos referenciales publicados o puestos a disposición desde el 3 de mayo de 2023, salvo indicación distinta. Excluye microdatos enviados u obtenidos de constituyentes y socios cuando están restringidos al uso exclusivo de ILO. ILOSTAT agrega datos de oficinas estadísticas nacionales, cuestionarios, procesamiento de microdatos y estimaciones modelizadas; por tanto, el portal no basta para resolver los derechos de cada tabla.

- Fuentes oficiales: [Rights and permissions](https://www.ilo.org/rights-and-permissions), [ILOSTAT bulk download](https://ilostat.ilo.org/data/bulk/), [data collection and production](https://ilostat.ilo.org/about/data-collection-and-production/).
- Alcance posible: tablas estadísticas agregadas, diccionarios y metadatos públicos con evidencia de licencia y derechos de origen. El portal documenta tablas de contenido y diccionarios EN/FR/ES.
- Excluir microdatos, registros de encuestas, fuentes restringidas a ILO, celdas confidenciales o reidentificables, datos personales y cualquier material de terceros sin autorización.
- Para cada tabla: fijar ruta, indicador/área de referencia, `last.update`, colección, fuente, notas, versión de diccionarios, timestamp UTC, bytes comprimidos/expandidos y SHA-256.
- Auditar CSV/gzip, esquema, valores ausentes, unidades, frecuencia, periodos, idioma, PII, secretos y malware; muestrear por dominio, país, idioma y formato.
- Deduplicar contra todo el corpus y todos los splits protegidos; ejecutar G-0 global antes de cualquier admisión.
- No está incluido en el colector Hugging Face actual. Requiere un workflow/descargador dedicado, acotado y determinista; permanece `acquisition_enabled=false` y `training_authorized=false` hasta implementarlo y superar todos los gates.


## Fuentes revisadas y excluidas/bloqueadas — 2026-11-22

- **UNESCO UIS Data Browser:** excluido por CC BY-SA 4.0; el proyecto no ha aprobado obligaciones share-alike. No descargar ni staging. [Términos oficiales](https://databrowser.uis.unesco.org/terms-and-conditions).
- **UN Comtrade:** bloqueado hasta acreditar que el uso encaja en la excepción de uso interno por una unidad institucional y obtener permiso para cualquier redistribución externa. La política incluye IA en uso interno, pero prohíbe re-difusión sin permiso de UNSD. No descargar ni staging. [Política de uso](https://uncomtrade.org/docs/policy-on-comtrade-data-use/) · [re-difusión](https://uncomtrade.org/docs/re-dissemination-of-data/).

Ambos registros tienen `acquisition_enabled=false`, `training_authorized=false` y `count_toward_admitted_bytes=false`.


## Hansard — informes parlamentarios diarios con OPL explícita (2026-11-23)

**Candidata discovery-only; 0 descargas, 0 filas y 0 bytes admitidos.** Se limita a PDFs diarios oficiales Commons/Lords cuyo propio documento incluya el aviso de reproducción bajo Open Parliament Licence v3.0 (SPDX `OPL-UK-3.0`). La muestra Commons del 2026-11-03 incluye el aviso en la página 1. La licencia permite adaptación y uso comercial con atribución, pero excluye datos personales y derechos de terceros.

- Fuentes: [Hansard PDF Commons 2026-11-03](https://hansard.parliament.uk/pdf/Commons/2026-11-03), [Open Parliament Licence](https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/), [SPDX OPL-UK-3.0](https://spdx.org/licenses/OPL-UK-3.0.html).
- El archivo Historic Hansard se excluye por defecto: su página declara que el material permanece bajo Parliamentary Copyright; no se infiere OPL desde la licencia general.
- Requisitos: aviso OPL en cada PDF; congelar cámara/fecha/volumen/número/URL/timestamp/páginas/bytes/SHA-256; extraer texto y hash separado; preservar atribución exacta; excluir datos personales y terceros; revisar privacidad por segmento y auditar muestras por cámara, fecha, tema y tipo documental.
- El endpoint no está conectado al colector HF; necesita colector PDF dedicado, almacenamiento seguro, revisión de privacidad/derechos, deduplicación completa y G-0. `acquisition_enabled=false`, `training_authorized=false`.

## Adquisiciones programadas — runs 149 y 150 (2026-11-23)

- [Run 149](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45063468144), grupo 7/8, artifact [14770830618](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45063468144/artifacts/14770830618): storage gate bloqueado antes de descargar; ZIP 653 bytes, SHA-256 `16fb4e6c8fae488456ed0faa8fee8e3e83cc502820c451c31dcc5e89c8525568`; JSON 871 bytes, SHA-256 `3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992`.
- [Run 150](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45135391130), grupo 1/8, artifact [14800025470](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45135391130/artifacts/14800025470): mismo bloqueo; ZIP 653 bytes, SHA-256 `26c72180952574f3919dfa467fe2921ae97e47ef626c36fbfd24083470697bce`; JSON 871 bytes, SHA-256 `5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437`.
- Ambos manifiestos registran `blocked_storage_gate`, 0 filas y 0 bytes de payload. Los hashes se verificaron descargando los artefactos y recalculando SHA-256.
- **Admisiones nuevas: 0 documentos / 0 bytes.** Inventario global sin cambios: 260.971 documentos y 703.593.871 bytes admitidos.


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


## Descubrimientos y bloqueos — 2026-11-25

### G-0: aclaración del alcance de la auditoría histórica

La run [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447) no es un G-0 global completo. `scripts/audit_heretic_training_corpus.py` importa el artefacto train de RONIN-IA y candidatos expresamente suministrados (Cosmopedia en esa ejecución); no enumera todos los splits de validation/test/benchmark/holdout. El diagnóstico de 120 preguntas es sintético y no sustituye los holdouts reales. La autorización histórica se limita a ese subconjunto source-scoped. **Bloqueo:** construir un manifiesto inmutable que cubra cada fuente y todos sus splits protegidos, ejecutar deduplicación exacta/aproximada y contaminación, y mantener cualquier fuente nueva fuera de training_eligible hasta entonces.

### MASSIVE 1.1 — candidato de texto multilingüe

- Release oficial: [alexa/massive](https://github.com/alexa/massive), revisión de metadata/NOTICE `f966f21846043aabef9b0f974fa7970027f43738`; tarball [MASSIVE 1.1](https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz).
- Más de 1M de utterances, 52 idiomas, 18 dominios, 60 intents y 55 slots; incluye catalán. NOTICE de Amazon declara CC BY 4.0 para MASSIVE y el texto SLURP; [SLURP LICENSE](https://github.com/pswietojanski/slurp/blob/8eb16545762be97ace75334109d73824217311f1/LICENSE.txt) separa el audio CC BY-NC 4.0, que se excluye.
- Solo `partition=train`; excluir dev/test y MMNLU-22 eval. Eliminar `worker_id` de cada fila y de `judgments`; conservar métricas agregadas. Verificar LICENSE del tarball, SHA-256, calidad, privacidad y lineage por idioma.
- Estado discovery-only, `acquisition_enabled=false`, 0 descargas y 0 bytes admitidos.

### Universal Dependencies 2.19 — candidato mixto por treebank

- Release [2.19](https://universaldependencies.org/download.html), [LINDAT handle 11234/1-6316](https://hdl.handle.net/11234/1-6316), publicado 2026-11-15: 402 treebanks, 226 idiomas.
- Licencia mixta: revisar por treebank `LICENSE.txt` y `README License:`; solo permitir exactamente CC BY 4.0 o CC0 1.0 y siempre con derechos del texto subyacente despejados. Excluir BY-SA, NC, ND, GPL, ausentes/contradictorias.
- Excluir Spanish AnCora hasta resolver su conflicto CC BY/GNU; excluir English GUMReddit porque no incluye el texto fuente. Solo `*-train.conllu`, nunca dev/test/test-only ni texto externo.
- Estado discovery-only, `acquisition_enabled=false`, 0 payload y 0 bytes admitidos.

### Common Voice v27.0 — términos actualizados

Los [términos oficiales](https://commonvoice.mozilla.org/oc/terms), efectivos 2025-10-31, limitan el acceso de datasets a Mozilla Data Collective y piden no publicar, distribuir ni mirror el dataset en otras plataformas. Sigue pendiente la procedencia de prompts por fila; no descargar ni re-hospedar hasta tener un flujo compatible con MDC y lineage validado.

### Preflights 157 y 158

- [Run 157](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45503206072), grupo 7/8, artifact 14971249604: ZIP SHA-256 `99c089bad3165b290c5d47d3677581cbe73ef1a7474579525d6c7ff272090dc5`; manifiesto SHA-256 `3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992`.
- [Run 158](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45581135551), grupo 1/8, artifact 15005629437: ZIP SHA-256 `63475b22bd76851a587b41c254468d7bde1eced8e9f6bdf78cec11c21a8ae7d4`; manifiesto SHA-256 `5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437`.
- Ambos ZIP contienen únicamente un manifiesto de 871 bytes; el ZIP mide 653 bytes. Storage gate bloqueado antes de descargar por falta de `HERETIC_STAGING_PASSPHRASE` (mínimo 32 caracteres). 0 filas, 0 bytes de payload, 0 staged, 0 admitted.
- Total admitido: **703.593.871 bytes / 260.971 documentos**, **0,140719 %** de 500 GB. Nuevas admisiones: **0**.


## Revisión diaria — 2026-11-26

### United Nations Parallel Corpus v1.0 — candidato de alta prioridad

- Fuente primaria: https://www.un.org/dgacm/en/content/uncorpus y https://www.un.org/dgacm/en/content/uncorpus/Download.
- DGACM describe el corpus como documentos oficiales y parlamentarios de la ONU en dominio público; su disclaimer indica que no se aplican otras restricciones y exige atribución/cita. No se asigna SPDX porque la fuente no publica un identificador estándar.
- Cobertura oficial: árabe, chino, inglés, francés, ruso y español; 799.276 documentos y 1.727.539 pares alineados anunciados por la fuente. No son bytes medidos.
- Alcance propuesto: solo v1.0 1990–2014. Excluir el archivo separado `UNv1.0.testsets.tar.gz` y cualquier test/dev de 2015. Preservar símbolo documental, número de traducción, fecha, keywords y alineamientos.
- Antes de staging: fijar cada parte y URL, hash SHA-256, longitud, estructura TEI/XML, alineamiento, calidad, privacidad y muestras por idioma/año. Estado discovery-only, acquisition_enabled=false, training_authorized=false.

### Multilingual Open Text v1.11 — candidato condicionado

- Release fijado: https://github.com/bltlab/mot/releases/tag/v1.11; tag resuelto a commit `9204cad746dfff0921e7a8f64c0cc0917bc75554`.
- El paper LREC 2022 declara la colección CC BY 4.0 y fuente de dominio público. El README v1.11 enumera 43 idiomas, mientras el paper de Release 1 habla de 44: resolver contra el manifiesto exacto del release.
- GitHub anuncia 54 assets con 8.342.562.863 bytes combinados; es tamaño remoto anunciado, no descargado. No hay digest SHA-256 publicado por asset.
- La política oficial de VOA aclara que solo el material producido exclusivamente por VOA es dominio público; AFP, AP y Reuters son contenido de terceros no redistribuible. Por tanto, solo texto de artículos con autoría VOA verificable; excluir cualquier wire copy, audio, vídeo, fotos, captions, snippets, logos y material ambiguo. Si no se puede demostrar por registro, no adquirir.
- Estado discovery-only, acquisition_enabled=false, training_authorized=false.

### Fuentes bloqueadas

- **JRC DCEP:** los términos oficiales conceden derechos no exclusivos para investigación; no existe autorización general para el uso de entrenamiento previsto. Bloqueado.
- **LR-Sum:** la ficha actual declara CC BY 4.0, pero también dice que el dataset se publica principalmente para investigación; deriva de MOT/VOA y no presenta una auditoría de derechos por registro. Bloqueado hasta aclaración del titular y procedencia por artículo.

### Preflights 162 y 163

- [Run 162](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45708741819), grupo 3/8, artifact [15066562283](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45708741819/artifacts/15066562283): ZIP 653 bytes, SHA-256 `73d43b33e273ceb588503f9a9e1366da21b7311d5da79a3368416afcb42a8df1`; manifiesto 871 bytes, SHA-256 `2829acd2e3d3d88cd5d58aa573fff9cfc9c9067d45dc1035e09e1c190c488b26`.
- [Run 163](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45785916162), grupo 5/8, artifact [15100551941](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45785916162/artifacts/15100551941): ZIP 653 bytes, SHA-256 `1cecaa91ba593acfdee3925a060a21eb2a0bb5818c239b72fb55728960a2e1b4`; manifiesto 871 bytes, SHA-256 `0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7`.
- Ambos manifiestos se descargaron y verificaron. Los logs muestran `HERETIC_STAGING_PASSPHRASE` vacío; el gate bloqueó antes de instalar las herramientas de descarga. 0 filas, 0 bytes remotos medidos, 0 descargados, 0 staged y 0 admitidos.
- Inventario: **260.971 documentos / 703.593.871 bytes**, sin variación. G-0 global permanece bloqueado; no se han ejecutado deduplicación ni revisión humana sobre nuevos payloads.

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


## Nueva fuente candidata — Federal Register / GovInfo (2026-11-27)

**Estado: discovery-only; 0 descargas, 0 filas medidas, 0 bytes admitidos.**

- Fuente primaria: https://www.govinfo.gov/bulkdata/FR. GovInfo expone directorios anuales de XML desde 2000; el 2026-11-27 el directorio 2026 figuraba actualizado el 26-11-2026 05:39 GMT.
- Base de reutilización: 1 CFR 2.6 permite reproducir o republicar sin restricción material de ediciones regulares/especiales del Federal Register; NARA/OFR lo confirma. No existe un SPDX estándar para esta base normativa. No usar `LicenseRef` como si fuera una licencia SPDX oficial.
- La guía GPO `usgpo/bulk-data@83a85170ce0bdd0cf218f6290bd739df8748e2ea` indica que el XML es una representación simplificada no oficial; solo PDF/Text son formatos oficiales online y las tablas/markup pueden presentar anomalías. Cotejar muestras con el formato oficial.
- La Library of Congress advierte que algunos ítems pueden reimprimir material protegido. Excluir terceros, gráficos, attachments, comentarios externos, user aids, sellos y logos sin autorización separada. Revisión de privacidad obligatoria para nombres/contactos y datos personales sensibles.
- Congelar por issue: fecha, volumen/número, package/document IDs, agencia, tipo, páginas, URL, headers, timestamp, longitud y SHA-256. Validar XML/UTF-8, tablas, seguridad, calidad y muestras estratificadas por agencia/año/tipo/dominio.
- No habilitar el colector hasta disponer de almacenamiento seguro, derechos por ítem, revisión de privacidad, deduplicación contra todo el corpus y G-0 global completo.

Fuentes oficiales: [1 CFR 2.6](https://www.ecfr.gov/current/title-1/chapter-I/subchapter-A/part-2/section-2.6), [NARA About the Federal Register](https://www.archives.gov/federal-register/the-federal-register/about.html), [GPO XML user guide](https://github.com/usgpo/bulk-data/blob/83a85170ce0bdd0cf218f6290bd739df8748e2ea/FR-XML_User-Guide.md), [17 USC §105](https://www.govinfo.gov/content/pkg/USCODE-2024-title17/html/USCODE-2024-title17-chap1-sec105.htm), [Library of Congress rights caveat](https://www.loc.gov/collections/federal-register/about-this-collection/rights-and-access/).

Acciones del día: [run 46009185876](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/46009185876) y [run 46009185814](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/46009185814) finalizaron correctamente, pero ambas auditorías son source-scoped; no completan G-0 global. El último preflight programado [run 45969736101](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/45969736101) quedó bloqueado por almacenamiento y descargó 0 bytes.


## DGT-Acquis / DGT-TM / JRC-Acquis — revisión de derechos (2026-11-27)

### DGT-Acquis

Estado: discovery-only. La página oficial describe corpus del Diario Oficial desde mediados de 2004 hasta finales de 2011, hasta 23 idiomas; publica 4.900.254 segmentos y tamaños comprimidos de 3 GB (da1-pc), 5 GB (da1-ft) y 9 GB (da1-fx). No se han medido ni descargado esos bytes.

La Comisión declara titularidad exclusiva del dataset y cede derechos mundiales para todo uso compatible con la Decisión 2011/833/EU. Requiere atribución, URL, fecha de última actualización y mención de titularidad. Sin SPDX estándar. El artículo 2(2)(b) de la Decisión excluye documentos con derechos de terceros; resolver NumDoc/CELEX uno a uno. Preferir da1-ft para contexto completo y no duplicar da1-pc como texto entrenable.

### DGT-TM

Estado: discovery-only. Memoria de traducción TMX en 24 idiomas, UTF-16LE, releases 2007–2021 (documentos hasta 2020). La Comisión declara derechos mundiales para todo uso bajo Decisión 2011/833/EU, con atribución y no distorsión. El corpus incluye documentos fuera del Acquis, usa inglés como pivote, fue preprocesado y las alineaciones son automáticas desde 2011. Verificar cada NumDoc, excluir terceros/no-Acquis sin derechos, no usar TMXtract y deduplicar contra DGT-Acquis/JRC-Acquis/EUR-Lex.

### JRC-Acquis v3.0

Estado: bloqueado por conflicto de términos. La página actual del JRC declara cesión mundial para todo uso, pero enlaza la licencia histórica actualizada en 2011 que limita el uso/distribución a fines de investigación y habla de distribución no comercial. No descargar hasta recibir aclaración escrita de JRC/OP sobre entrenamiento comercial. La estadística publicada (22 idiomas, 463.792 textos, 4.350.447 documentos alineados) no equivale a payload ni a admisión.

Fuentes oficiales: https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en ; https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-translation-memory_en ; https://joint-research-centre.ec.europa.eu/language-technology-resources/jrc-acquis_en ; https://wt-public.emm4u.eu/Acquis/JRC-Acquis.3.0/doc/licence.html ; https://eur-lex.europa.eu/eli/dec/2011/833/oj/eng ; https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en

Todos los registros permanecen sin SPDX estándar, sin descargas y sin autorización de entrenamiento. Se exige snapshot por ZIP/idioma, rights clearance por NumDoc, auditoría de idioma/alineación/privacidad, deduplicación y G-0 global.


## IATE — candidata bloqueada por condiciones de exportación (2026-11-28)

IATE es una termbase multidisciplinar de la UE, con exportaciones CSV/TBX y 24 idiomas oficiales. La descarga requiere EU Login y remite a condiciones de uso específicas que no se han podido verificar públicamente. No se ha encontrado una licencia uniforme del termbase. Las entradas incluyen definiciones, contextos y referencias a legislación, normas y publicaciones de terceros; el aviso de reutilización de un folleto no se extiende al conjunto de datos.

**Estado:** blocked_export_terms_and_entry_level_third_party_rights_unresolved; acquisition_enabled=false; training_authorized=false; 0 descargas, 0 staging y 0 bytes admitidos. No automatizar el exportador ni reutilizar sus contenidos hasta obtener condiciones y derechos por entrada/campo.

Fuentes: [IATE](https://iate.europa.eu/en), [FAQ](https://iate.europa.eu/faq), [guía de descarga](https://iate.europa.eu/assets/brochure_search_by_collections_and_download.pdf), [registro de catálogo](https://data.europa.eu/data/datasets/iate?locale=en).

## Reconciliación de preflights — runs 180 y 181 (2026-11-28)

- Run [180](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/46071076162), grupo 3/8, artifact [15232982518](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/46071076162/artifacts/15232982518): ZIP 653 B, SHA-256 7655fc1abd5f4f437b0dbbc2297a703a225aa86af31b82b3d0ce9386f68b685b; JSON 871 B, SHA-256 2829acd2e3d3d88cd5d58aa573fff9cfc9c9067d45dc1035e09e1c190c488b26.
- Run [181](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/46125173946), grupo 5/8, artifact [15255428113](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/46125173946/artifacts/15255428113): ZIP 653 B, SHA-256 ea15e4baf19f57b7673946c0fbcfe7b4ea85e644b72eb1cd506aff31e628541d; JSON 871 B, SHA-256 0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7.
- Los dos manifiestos confirman blocked_storage_gate, cero fuentes, cero filas y cero payload. El preflight terminó correctamente, pero omitió descarga y revisión porque falta HERETIC_STAGING_PASSPHRASE de al menos 32 caracteres.
- Bytes remotos anunciados: no medidos; descargados/comprimidos/expandidos: 0; staging durable: 0; admitidos: **0**. Los ZIP/JSON solo son manifiestos.
- G-0 global sigue bloqueado por inventario incompleto de validation/test/benchmark/holdout. Inventario histórico admitido: **260.971 documentos / 703.593.871 bytes (0,140719 % de 500 GB)**.

No se ha entrenado ni modificado ningún modelo o checkpoint.
