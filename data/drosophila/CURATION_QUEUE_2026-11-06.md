# Cola de curación y admisión Drosophila

Fecha de revisión: 2026-11-06. Alcance: contenido científico y técnico específicamente relacionado con *Drosophila*, para ampliar `data/drosophila/`. Esta cola separa fuentes descubribles de payloads descargados y de contenido realmente admitido. **No suma candidatos al corpus ni los declara entrenables.**

## Diagnóstico del contenido actual

`parts/01..10_*.jsonl` contiene 50.000 ejemplos procedimentales sintéticos repartidos entre matemáticas, álgebra, lógica, programación, física, química, probabilidad, estadística, economía e ingeniería. El README upstream reconoce 50 familias con 1.000 parametrizaciones por familia y advierte que la identidad de fila no implica diversidad semántica. Es un buen conjunto de ejercicios generales, pero no equivale a 50.000 documentos científicos sobre Drosophila.

No mezclaré los nuevos materiales biológicos con esos shards ni cambiaré su entrenamiento hasta tener manifiesto, revisión y evaluación independientes.

## Fuentes prioritarias para adquisición

| Prioridad | Fuente / snapshot | Contenido aprovechable | Derechos observados | Decisión |
|---|---|---|---|---|
| P0 | FlyBase FB2026_03 | Descripciones de genes, alelos, fenotipos, interacciones genéticas/físicas, expresión, anatomía y desarrollo; exportaciones TSV/JSON y Chado | FlyBase declara CC BY 4.0 para los datos y anotaciones que produce y publica | Candidato de alta prioridad. Fijar release y hashes; conservar atribución; separar datos FlyBase propios de referencias o contenido de terceros. |
| P0 | Alliance of Genome Resources, release fijada | Datos integrados por organismo, anotaciones, interacciones, expresión, fenotipos y ortología; archivos específicos FB/Drosophila | La ficha del Open Data Registry indica que la mayoría es CC0 y algunos conjuntos CC BY 4.0; hay que resolver licencia por colección/archivo | Candidato. No asumir CC0 global: allowlist por recurso y versión, con atribución cuando corresponda. |
| P0 | Dryad, datasets Drosophila con CC0 explícito | Datos experimentales reutilizables, tablas de fenotipos, comportamiento, genética y biología de sistemas | Dryad indica que sus datasets se publican bajo CC0; validar el registro y la versión individual, y citar el artículo/dataset | Candidato por DOI, no descarga masiva ciega. Comenzar por DOI 10.5061/dryad.45177sc y 10.5061/dryad.r2280gbv8 tras comprobar los archivos y metadatos de licencia. |
| P1 | FlyRNAi / DRSC / TRiP | Pantallas RNAi, recursos funcionales, expresión y fenotipos | El portal ofrece datos públicos, pero acceso público no acredita una licencia uniforme de cada dataset | Discovery solamente hasta resolver derechos por dataset y archivos. |
| P1 | NCBI GEO / SRA y ENA — estudios Drosophila | Expresión, RNA-seq y datos ómicos; metadatos de muestras y protocolos | Los datos primarios pueden tener condiciones específicas; artículos vinculados conservan sus derechos | Selección estudio a estudio. No importar secuencias crudas como texto de entrenamiento; derivar descripciones/ejemplos solo desde metadatos reutilizables y documentación autorizada. |
| P2 | PubMed Central OA — artículos Drosophila | Texto científico narrativo, métodos, resultados y explicaciones | Solo artículos/versiones con licencia de reutilización compatible; filtrar por artículo y versión | Mantener CC0/CC BY con versión exacta. Excluir NC/ND/SA no compatibles, retractaciones, material de terceros y datos personales. |

## Primeros registros concretos

- **FlyBase FB2026_03** — release publicada el 17-09-2026. Empezar por tablas de genes, fenotipos, interacciones, expresión y ontologías FBbt/FBdv. No empezar por FASTA/GFF masivos: son datos biológicos estructurados, no texto instructivo; conservarlos como datos auxiliares y no volcarlos a prosa artificial.
- **Dryad 10.5061/dryad.45177sc** — conjunto de datos de circuito de navegación y morfología neuronal en Drosophila; archivos tabulares grandes y README explicativo. Revisar cada archivo, variables, unidades y licencia antes de transformación.
- **Dryad 10.5061/dryad.r2280gbv8** — dataset 2026 sobre adaptación y contexto genético en *D. melanogaster*; la página declara CC0 1.0. Verificar snapshot y contenido de cada archivo antes de admitir.
- **Alliance Genome Resources** — seleccionar exclusivamente los objetos FB de la release y aplicar su licencia por objeto.

## Transformación a ejemplos entrenables

1. Mantener el payload original inmutable y sus hashes.
2. Extraer solo texto/documentación y tablas que puedan interpretarse sin perder unidades, controles, población, especie, genotipo y contexto experimental.
3. Convertir filas en registros estructurados con pregunta/respuesta únicamente cuando la respuesta sea determinista y esté respaldada por columnas o documentación. No inventar explicaciones causales.
4. Incluir referencia, DOI/URL, release, licencia, autores/proveedor, archivo original y hash en cada registro.
5. Excluir nombres/datos personales, muestras humanas incidentales, identificadores sensibles y materiales de terceros sin permiso.
6. Deduplicar exacta y semánticamente contra todos los shards actuales y el holdout. Separar por estudio/DOI y no por filas aleatorias para evitar fuga entre train y evaluación.
7. Revisar manualmente una muestra estratificada por fuente, archivo, tipo de dato y dominio; validar respuestas contra los datos originales.
8. Admitir solo después de ejecutar validadores y producir manifiesto reproducible con particiones disjuntas.

## Estados permitidos

- `discovery`: fuente identificada, aún sin verificar archivos.
- `candidate`: payload adquirido, hash y metadatos fijados; no entrenable.
- `reviewed`: derechos, calidad, privacidad y contenido revisados; falta deduplicación/splits globales.
- `admitted_train`: solo registros que superan todas las compuertas y tienen partición train verificable.
- `held` / `rejected`: bloqueado o excluido con motivo.

**Estado de esta cola:** 4 líneas de adquisición priorizadas; 0 payloads nuevos descargados por esta revisión; 0 documentos nuevos admitidos. No se modifica el holdout ni se afirma que el corpus entrenable haya aumentado.

## Referencias oficiales

- FlyBase bulk downloads: https://flybase.org/downloads/bulkdata
- FlyBase licencia CC BY 4.0: https://wiki.flybase.org/wiki/FlyBase:About#FlyBase_Licenses_and_Availability
- Alliance Genome Resources open-data registry: https://github.com/awslabs/open-data-registry/blob/main/datasets/alliance-genome-resources.yaml
- Dryad reutilización CC0: https://datadryad.org/help/guides/reuse
- Dryad 10.5061/dryad.45177sc: https://doi.org/10.5061/dryad.45177sc
- Dryad 10.5061/dryad.r2280gbv8: https://doi.org/10.5061/dryad.r2280gbv8
- FlyRNAi / DRSC: https://www.flyrnai.org/
