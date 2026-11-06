# HERETIC-RONIN

Laboratorio experimental de modelos pequeños y destilación. HERETIC-RONIN comparte resultados y materiales con RONIN-IA, pero no hereda su política de adquisición de conocimiento ni su exigencia de trazabilidad exhaustiva.

## Bootstrap inicial: Drosophila 100.9M

El workflow [Stage Drosophila model and datasets](.github/workflows/stage-drosophila.yml) prepara un paquete descargable con:

- Los datasets admitidos publicados en `RONIN-IA/data/datasets/admitted/`, conservando sus manifiestos y avisos de licencia.
- El checkpoint experimental principal `Ronin-Drosophila-100900160` (100.900.160 parámetros).
- El manifiesto del modelo y el SHA-256 del checkpoint.

El workflow se ejecuta al incorporar su definición y también puede lanzarse manualmente desde **Actions → Stage Drosophila model and datasets → Run workflow**. Al terminar, el paquete aparece en los artefactos de esa ejecución con el nombre `heretic-drosophila-100900160-and-admitted-datasets`.

### Checkpoint de origen

- Proyecto de origen: [RONIN-IA](https://github.com/orbitalronin94/RONIN-IA)
- Ejecución que promovió el main experimental: [#42207268776](https://github.com/orbitalronin94/RONIN-IA/actions/runs/42207268776)
- Artefacto de origen: `13497987527`
- Parámetros: `100,900,160`
- SHA-256 esperado: `f3f8e2e75e418f8630372c242378a28010db83148d169d85ad3e4f73114cda9a`

El checkpoint pesa unos 404 MB: no se introduce como blob Git ordinario. Se empaqueta como artefacto de GitHub Actions, con retención inicial de 90 días.

### Nota de evaluación

Drosophila es un punto de partida experimental, no una afirmación de capacidad general. El manifiesto de origen registra 500 pasos de entrenamiento sin tutor, screening pareado MMLU-Pro de 5/64 antes y después, G-0 en FAIL y comprobaciones globales de near-duplicates/contaminación de holdout pendientes. HERETIC podrá usar destilación en sus siguientes experimentos; este checkpoint concreto no fue destilado.

## Licencia

El código del repositorio usa MIT. Los datasets conservan sus propias condiciones, avisos y manifiestos dentro del paquete; la licencia MIT del código no sustituye las licencias de los datos ni de los pesos.
