# Política de calidad del dataset Drosophila

El volumen no equivale a calidad. Cada lote declara objetivo, unidad de muestra, dominios, familias, procedencia, transformaciones, split y limitaciones.

Controles: esquema y campos; deduplicación exacta y semántica; corrección mediante oráculos deterministas; balance por dominio/habilidad/dificultad; trazabilidad; separación del holdout por familias; inspección humana estratificada.

El lote 01301–51300 contiene 50.000 muestras sintéticas procedimentales en diez dominios, con 50 familias y 1.000 parametrizaciones por familia. La validación automática comprueba estructura y resultados calculables, pero no certifica calidad pedagógica, verdad científica general ni independencia semántica. Se etiqueta train_candidate, nunca benchmark/holdout.

Referencias metodológicas: Hugging Face Dataset Cards; Apple Designing evaluation datasets; OxRML Construct Validity Checklist; GOV.UK AI-ready datasets.
