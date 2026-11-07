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
| Corpus Drosophila versionado | 50.000 filas sintéticas candidatas; no es la biblioteca completa |
| Estructura | 10 shards JSONL de 5.000 filas |
| Dominios actuales | Matemáticas, álgebra, lógica, programación, física, química, probabilidad, estadística, economía e ingeniería |
| Naturaleza del lote actual | Sintético y procedimental; no corpus gold |
| Corpus admitido tras auditoría global | 260.971 documentos únicos (261.039 examinados, 68 excluidos); 703.593.871 bytes de texto admitidos: base RONIN-IA 680.665.972 + Cosmopedia curada 22.927.899. Auditoría combinada [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447). |
| Objetivo de biblioteca | 500 GB de datos admitidos y trazables (objetivo, aún no alcanzado) |
| Promoción de datos | Nunca automática por volumen |
| Evaluación | Holdout separado; nunca se incorpora al entrenamiento |

**Importante:** las 50.000 filas actuales se generaron mediante plantillas procedimentales. Los IDs distintos garantizan filas identificables, no diversidad semántica ni corrección independiente. El lote sirve como material experimental, pero no debe describirse como 50.000 ejemplos humanos verificados ni como 50.000 capacidades distintas. La propia ficha del lote documenta esta limitación.

## Biblioteca de datos

La biblioteca versionada se organiza en `data/`:

- `data/sources/registry.json`: catálogo de fuentes, licencias, revisiones y estado de curación.
- [`data/datasets/README.md`](data/datasets/README.md): inventario operativo de datasets admitidos, candidatos y cuarentena.
- `data/drosophila/`: corpus experimental local actualmente versionado.

- `data/drosophila/parts/`: shards JSONL de entrenamiento.
- `data/drosophila/README_01301_51300.md`: ficha y limitaciones del lote sintético de 50.000 filas.

**Drosophila es el nombre del corpus experimental, no un filtro temático biológico.** La biblioteca es generalista y multidominio. La cola de curación vigente está en [`data/drosophila/CURATION_QUEUE_2026-11-06.md`](data/drosophila/CURATION_QUEUE_2026-11-06.md); las fuentes, licencias declaradas y gates de adquisición se registran en [`data/sources/registry.json`](data/sources/registry.json). Los manifiestos train-only de RONIN-IA se recuperaron con hashes verificados. La auditoría global combinada [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447) examinó 261.039 documentos (256.305 de la base RONIN-IA + 4.734 de Cosmopedia v0.1), excluyó 68 extremos duplicados y dejó 260.971 documentos admitidos. Los 4.734 textos Cosmopedia aportan 22.927.899 bytes; sumados a los 680.665.972 bytes de la base, el inventario admitido asciende a 703.593.871 bytes. La comprobación de 120 preguntas es un diagnóstico sintético, no un benchmark externo. Papers conserva alcance de autorización interna únicamente.

La biblioteca crecerá hacia **500 GB**, no hacia un número fijo de ejemplos. El tamaño anunciado por una fuente no equivale a bytes descargados ni a bytes admitidos. Mantendremos contadores separados para bytes remotos anunciados, bytes descargados, bytes íntegros, bytes tras deduplicación y bytes finalmente admitidos. Cada nuevo lote debe conservar, como mínimo:

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

## Objetivo de expansión: 50 GB → 500 GB

La expansión se realizará por lotes incrementales y reproducibles. La prioridad es incorporar corpus amplios con licencias permisivas verificables, procedencia conservada y diversidad real de dominios e idiomas. El volumen se mide en bytes reales, no se infiere a partir de tokens, número de filas ni tamaño anunciado por el Hub.

### Fuentes grandes registradas

El manifiesto [`data/sources/registry.json`](data/sources/registry.json) mantiene las fuentes, revisiones, licencias, restricciones, planes de adquisición y estado de admisión. Los primeros candidatos son:

- **FineWeb**: ODC-By 1.0; el subconjunto `sample-350BT` se documenta en torno a 388 GB. La licencia de la base de datos no convierte automáticamente cada página web de origen en contenido libre; se conservan los avisos y la procedencia.
- **DCLM-Baseline**: CC-BY-4.0; corpus anunciado en torno a 7,2 TB. Se seleccionarán shards acotados y se conservará atribución.
- **Common Pile v0.1**: unos 8 TB agregados de dominio público y fuentes abiertas; solo se admiten componentes con licencia individual comprobada.
- **The Stack v1.1**: unos 6 TB near-deduplicated de código con 193 licencias permisivas; cada archivo mantiene su licencia original, SPDX y atribución. No se trata como una licencia global única.

Estas cifras son tamaños publicados por los mantenedores, no bytes que ya estén almacenados en este repositorio. Todas las fuentes permanecen en estado candidato hasta fijar revisión, descargar, verificar hashes, deduplicar y auditar.

Orden de trabajo:

1. Inventariar fuentes y verificar licencias en la fuente primaria.
2. Adquirir lotes pequeños y registrar su procedencia antes de procesarlos.
3. Normalizar a un esquema JSONL común sin borrar metadatos.
4. Ejecutar validación estructural, deduplicación y filtros de calidad.
5. Auditar muestras estratificadas; rechazar fuentes que no superen los controles.
6. Integrar únicamente lotes admitidos y actualizar el manifiesto y este README.
7. Repetir hasta alcanzar 500 GB **admitidos**, no simplemente anunciados o descargados.

No se afirmará que se alcanzó el objetivo hasta que un inventario reproducible mida los bytes admitidos, publique hashes, atribuciones, auditorías y el destino de almacenamiento.

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

**Almacenamiento:** no se subirán cientos de gigabytes al historial Git. El repositorio conservará manifiestos, scripts, hashes y reportes. Los datos binarios deberán residir en un almacenamiento externo versionado (por ejemplo, Hugging Face Datasets o un bucket de objetos compatible con S3) cuando exista un destino y credenciales configurados. GitHub Actions se utilizará para adquisición por lotes y auditorías acotadas, no como almacenamiento permanente de 500 GB.

## Biblioteca heredada y ampliación open source

### RONIN-IA: corpus que debe heredarse

El inventario de origen de RONIN-IA (6-11-2026) declara **286.464 documentos train scoped**; la cifra de 286.468 del README de origen difiere en cuatro registros NASA que el artefacto más reciente retiene por mismatch:

| Fuente | Train scoped | Derechos / límite |
|---|---:|---|
| CoVoST 2 translation-only | 270.244 | CC0-1.0; solo texto de traducción, no audio |
| ScienceVerse | 7.103 | CC-BY-4.0 / CC0 por documento; atribución por DOI |
| Mathlib4 | 8.498 | Apache-2.0; payload train-only recuperado y SHA-256 verificado |
| Literatura española | 608 | Licencia por fuente; solo train |
| NASA NTRS file-reviewed | 2 train (+4 retenidos) | Solo payloads cuyo hash/bytes coinciden con la atestación |
| Papers propios | 9 | Autorización para entrenamiento interno; no implica redistribución |

Estos 286.464 documentos son **elegibles por partición y manifiesto de origen**. El bloqueo global inicial quedó superado para el corpus exacto incluido en la auditoría combinada [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447): train-only RONIN-IA más Cosmopedia v0.1 curada. Esta autorización es interna y experimental, no amplía derechos de redistribución ni autoriza fuentes candidatas no auditadas. El importador ya ha materializado 286.464 registros en el [artefacto train-only 42283514919](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42283514919) (288.668.608 bytes de artefacto). Incorpora los 8.498 registros Mathlib4 y los dos NASA train exactos. Cuatro NASA siguen retenidos por mismatch de atestación/payload; no se fuerzan a train. El estado y los bloqueos exactos se mantienen en [data/imports/README.md](data/imports/README.md).

**Regla de entrenamiento:** se heredan todas las particiones train que superen sus gates; validation, test y holdout permanecen aislados. No se reconstruyen splits perdidos a partir del dataset upstream ni se sustituyen hashes por otros calculados después.

### Nuevas bibliotecas open source prioritarias

La ampliación no se limita a fuentes sintéticas ni a Common Crawl. Se buscarán fuentes especializadas, descargables y complementarias:

| Fuente | Dominio / idioma | Licencia declarada | Adquisición prevista |
|---|---|---|---|
| [FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | Texto educativo general, inglés | ODC-By 1.0 | Shards acotados y fijados por revisión |
| [FineWeb-2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | Web multilingüe, 1.000+ idiomas | ODC-By 1.0 | Priorizar español, catalán e inglés |
| [OpenWebMath](https://huggingface.co/datasets/open-web-math/open-web-math) | Matemáticas, inglés | ODC-By 1.0; aplicar también términos de Common Crawl | Corpus matemático deduplicado |
| [Cosmopedia v0.1](https://huggingface.co/datasets/HuggingFaceTB/cosmopedia) / [v2](https://huggingface.co/datasets/HuggingFaceTB/smollm-corpus) | Libros de texto, educación y ciencia | Apache-2.0 (v0.1); ODC-By 1.0 (v2) | Configs educativos y deduplicación cruzada |
| [The Stack v1.2](https://huggingface.co/datasets/bigcode/the-stack) | Código, 358 lenguajes | Licencia original por archivo; versión 1.2 incorpora exclusiones adicionales | Solo archivos con SPDX permitido; respetar opt-outs |
| [Common Pile v0.1](https://huggingface.co/collections/common-pile) | Ciencia, libros, referencia y texto general | Mixta por fuente constituyente | Solo componentes con licencia y procedencia individual verificadas |
| [Wikipedia dumps](https://dumps.wikimedia.org/) | Enciclopedia multilingüe | CC BY-SA / GFDL según contenido y versión | Conservar atribución, historial/licencia y obligaciones share-alike |
| [Project Gutenberg](https://www.gutenberg.org/) | Literatura y libros, principalmente inglés | Dominio público en EE. UU. para la mayoría; revisar país y aviso por obra | Obras individualmente verificadas |

**Primera adquisición ejecutada:** [run 42283763295](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42283763295) descargó 20.000 filas train de cuatro fuentes, con 97.008.625 bytes de texto y un artefacto de 36.722.816 bytes:
- FineWeb-Edu: 5.000 documentos.
- OpenWebMath: 5.000 documentos.
- Cosmopedia v0.1 (`auto_math_text`): 5.000 documentos.
- Cosmopedia v2: 5.000 documentos.

Las cuatro revisiones inmutables y los SHA-256 están en `data/sources/registry.json` y en el artefacto del run. La comprobación local inicial encontró 0 duplicados exactos entre esas 20.000 filas y 0 coincidencias exactas con las 120 preguntas del holdout. **No es una admisión:** la near-deduplicación, la auditoría de benchmark, la revisión humana y la comprobación de derechos por contenido siguen pendientes; el manifiesto marca `training_authorized=false`.

La licencia de una colección **no borra los derechos de cada documento**. ODC-By no convierte automáticamente cada página web en obra libre; Common Pile no tiene una licencia universal; The Stack conserva licencias por archivo. Ningún candidato cuenta como admitido por aparecer en esta tabla. La fuente primaria, su revisión inmutable, split, atribución y SHA-256 deben quedar registrados antes de usarlo.

### Entrenamiento experimental actual — 500 pasos

El piloto [run 42358300901](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42358300901) ejecuta 500 pasos de optimizador en tramos reanudables de 50. Comenzó antes de que Cosmopedia v0.1 superara la auditoría global, por lo que **no debe contabilizarse como entrenamiento con Cosmopedia**: consume el corpus base RONIN-IA ya autorizado (680.665.972 bytes). La admisión de Cosmopedia queda disponible para una siguiente ejecución, que deberá descargar el artefacto curado, verificar su SHA-256 y consumir el manifiesto/auditoría correspondientes.

La auditoría combinada [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447) incluyó 4.734 filas Cosmopedia y 256.305 registros base. Detectó 9 grupos/hits exactos y 68 pares SimHash; los 68 índices excluidos pertenecen al tramo base anterior al inicio del bloque Cosmopedia, por lo que los 4.734 registros curados quedaron dentro del subconjunto autorizado. No hubo coincidencias exactas con las 120 preguntas sintéticas. Esto no demuestra ausencia semántica de contaminación ni certifica la exactitud de cada afirmación matemática.

Los próximos workflows deben mantener la comparación pareada antes/después, hashes de checkpoint, evaluación por dominio y separación estricta de holdout. No se promociona un checkpoint por pérdida de entrenamiento o por el mero hecho de haber ingerido más texto.

La cifra de 500 GB sigue siendo un objetivo de biblioteca, no una cantidad ya descargada. Los workflows y sus artefactos son la fuente de verdad; este README no declara un entrenamiento completo antes de que finalicen todos los tramos.


### Nueva fuente en adquisición — Data Provenance Initiative

El importador incorpora un piloto adicional de hasta 5.000 documentos de [Data Provenance Initiative filtered](https://huggingface.co/datasets/common-pile/data_provenance_initiative_filtered). La licencia se filtra por registro desde `metadata.license` (MIT, Apache-2.0, BSD, CC-BY-4.0 y CC0); se conservan URL de licencia, dataset de origen y procedencia. La ficha informa de 3,51 millones de filas, pero advierte de errores de metadatos y posible license laundering. Por tanto, este lote seguirá como candidato no admitido hasta revisión independiente, deduplicación global, holdout y muestra humana. La ampliación está implementada en `scripts/acquire_open_source_candidates.py`; su ejecución se realiza en GitHub Actions.


## Expansión multilingüe de transcripciones — 2026-11-07

Se añade una nueva tranche de bibliotecas de texto obtenidas de transcripciones, sin descargar ni conservar audio:

- **VoxPopuli (CC0-1.0):** seis configuraciones de idioma (español, inglés, alemán, francés, italiano y polaco), hasta 10.000 transcripciones *gold* de `train` por idioma. Se proyectan las columnas `normalized_text`, `is_gold_transcript` y `language`; se excluyen audio, identificadores de hablante, género, acento y splits validation/test. El corpus completo declara 1.255.237 filas y 18 idiomas, pero la adquisición de esta tanda está limitada a 60.000 filas. [Ficha y licencia](https://huggingface.co/datasets/facebook/voxpopuli) · [Repositorio oficial y licencia CC0 de los datos](https://github.com/facebookresearch/voxpopuli).
- **LibriSpeech ASR (CC-BY-4.0):** hasta 25.000 transcripciones de `train.clean.100` y 25.000 de `train.clean.360`. Solo se proyecta la columna `text`; quedan fuera audio, IDs de hablante/capítulo y cualquier split de validación o test. Se conserva la atribución a Panayotov et al. y OpenSLR. [Ficha del dataset](https://huggingface.co/datasets/openslr/librispeech_asr) · [Licencia y splits oficiales](https://openslr.org/12/).

**Límite de esta tranche:** hasta 110.000 registros candidatos (60.000 VoxPopuli + 50.000 LibriSpeech). La descarga fija el commit SHA de cada fuente y publica SHA-256 por archivo/configuración. Los filtros de transcripción gold y de columnas se aplican antes de serializar. Son candidatos, no datos admitidos: deben superar deduplicación cruzada, auditoría de holdout, revisión humana por idioma y comprobación final de atribución/calidad. No se habilita su uso en el entrenamiento ni se suman bytes admitidos automáticamente.

Fuentes oficiales consultadas: VoxPopuli documenta CC0 para los datos y 18 idiomas con transcripción; OpenSLR declara CC BY 4.0 para LibriSpeech. La biblioteca mantiene las licencias y procedencias por fuente, sin asumir que el permiso de una fuente cubre otras.


### Ampliación de adquisición v2 — 2026-11-07

La siguiente tranche amplía los límites de descarga sin relajar la admisión: hasta 20.000 textos científicos de arXiv (paper_text, solo licencias por artículo CC-BY-4.0 o CC0), hasta 20.000 textos de libros revisados por pares de DOAB (solo CC-BY-4.0 explícito en metadatos), hasta 15.000 secciones por fuente de Pressbooks y LibreTexts (solo CC-BY-4.0), y hasta 10.000 artículos biomédicos PubMed (CC-BY-4.0/CC0). Son máximos candidatos, no bytes adquiridos ni admitidos; los totales reales se medirán desde los manifiestos SHA-256.

La adquisición también corrige un error de sintaxis Python (true en lugar de True) que hacía fallar el script antes de iniciar cualquier descarga. Se elimina el disparador desde ramas experimentales para evitar ejecuciones duplicadas y se amplía el límite de tiempo a seis horas. CCCC queda fuera de la descarga activa: la muestra pública inspeccionada expone URL/procedencia, pero no el campo de licencia por registro que exige el filtro actual; no se aceptará hasta resolver ese mapeo.


## Corpus efectivo auditado — 2026-11-07

El corpus base ya consumido por entrenamientos anteriores comprende **256.237 documentos y 680.665.972 bytes** tras la auditoría [42288107561](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42288107561). La auditoría combinada posterior [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447) añadió Cosmopedia v0.1 curada: 4.734 documentos y 22.927.899 bytes. Resultado global: 261.039 examinados, 68 excluidos y **260.971 documentos / 703.593.871 bytes admitidos**. El piloto de 500 pasos [42358300901](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42358300901) arrancó antes de esa admisión y no consumió Cosmopedia. Los 120 ítems de holdout son un diagnóstico sintético, no un benchmark público; los derechos y autorizaciones siguen limitados por fuente.


### Nueva tanda de corpus documental (en adquisición, no admitida)

La siguiente ampliación incorpora tres candidatos de alto volumen: Spanish-PD-Books (52,1 GB publicados; se fijan dos shards (1,18 GB comprimidos) para una primera muestra), opiniones judiciales CourtListener/docketx (8,47 GB; CC0 declarado y opiniones públicas) y 76 libros OpenStax (159 MB; CC-BY-4.0 declarado por el dataset, pendiente de comprobar la licencia por libro/edición). Sus registros y gates están en `data/sources/registry.json`; los artefactos se separarán por fuente. **No se suman al corpus entrenable hasta superar revisión humana, procedencia/licencia, deduplicación global y control de holdout.**


### Candidatos de escala y patrimonio documental

Se incorporan a la adquisición experimental Common Corpus de Pleias (2,27 billones de tokens declarados, con licencia/procedencia por documento y filtro exacto), English-PD (362 GB; títulos pre-1884 según la ficha) y Spanish-PD-Newspapers (48,6 GB; corpus histórico OCR). Se toman shards limitados para inspección, no el corpus entero. Ninguno cuenta como entrenable hasta revisión de derechos por obra, OCR, muestras, deduplicación global y holdout. Detalles: `data/datasets/README.md` y `data/sources/registry.json`.


### Nuevas fuentes multilingües en evaluación

La siguiente tanda añade un slice de libros públicos en portugués brasileño y un slice cultural de German Commons. Ambos son **candidatos**, no datos entrenables: el primero requiere verificación de procedencia/obras y OCR; el segundo exige que cada licencia documental sea exactamente CC0-1.0 o CC-BY-4.0, rechazando licencias mixtas, BY-SA, NC, ND y desconocidas. El inventario operativo y los gates están en [data/datasets/README.md](data/datasets/README.md) y [data/sources/registry.json](data/sources/registry.json).
