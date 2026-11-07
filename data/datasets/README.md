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

La PR [#21](https://github.com/orbitalronin94/HERETIC-RONIN/pull/21) prepara el arreglo de inferencia de esquema y nuevas muestras separadas para inspección:

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
| [Spanish-PD-Books](https://huggingface.co/datasets/PleIAs/Spanish-PD-Books) | 52,1 GB; 302.640 libros; 13,9B palabras | 4 shards Parquet fijados (~1,7 GB comprimidos; máximo 12.000 textos) | El publicador afirma dominio público en la UE por autor fallecido hace más de 70 años; agregación BDH + Internet Archive | Candidato: verificar autor/fecha, procedencia y OCR por muestra |
| [CourtListener / docketx](https://huggingface.co/datasets/docketx/us-caselaw-fed-district) | 8,47 GB; ~1,31M opiniones | Hasta 100.000 opiniones | CC0 de empaquetado; opiniones judiciales estadounidenses de dominio público | Candidato: verificar tipo de opinión, calidad, metadatos y deduplicación |
| [OpenStax text](https://huggingface.co/datasets/crumb/openstax-text) | 3.354.565 filas; 159 MB; 76 libros | Hasta 50.000 textos | CC-BY-4.0 declarado por la ficha del dataset | Candidato: comprobar licencia por libro/edición y atribución embebida |

### Detalles de adquisición

- Spanish-PD-Books: shards `spanish_pd_1.parquet`, `spanish_pd_10.parquet`, `spanish_pd_100.parquet` y `spanish_pd_101.parquet`; se preservan `identifier`, `creator`, `title`, `publication_date` y `word_count`. La ficha muestra problemas de esquema en el visor; la adquisición aislada por shard evita mezclar esquemas incompatibles. El estado sigue siendo candidato hasta revisar derechos y OCR.
- CourtListener: solo `text` como payload, conservando identificador, jurisdicción, título, fuente, licencia, cita, tribunal y fecha.
- OpenStax: se conserva el texto con atribución original; la licencia general de OpenStax puede variar por libro/edición, así que la etiqueta CC-BY-4.0 de la colección no es suficiente para admitirla.

Los nuevos artefactos se separan por fuente para facilitar descarga e inspección sin depender de un único ZIP multi-GB. Referencias: [ficha Spanish-PD-Books](https://huggingface.co/datasets/PleIAs/Spanish-PD-Books), [ficha CourtListener](https://huggingface.co/datasets/docketx/us-caselaw-fed-district), [ficha OpenStax](https://huggingface.co/datasets/crumb/openstax-text).
