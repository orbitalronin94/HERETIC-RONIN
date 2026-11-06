# HERETIC-RONIN

Laboratorio experimental de modelos pequeños y destilación. HERETIC-RONIN comparte resultados y materiales con RONIN-IA, pero no hereda su política de adquisición de conocimiento ni su exigencia de trazabilidad exhaustiva.

## Bootstrap inicial: Drosophila 100.9M

El workflow [Stage Drosophila model and datasets](.github/workflows/bootstrap.yml) prepara un paquete descargable con:

- Los datasets admitidos publicados en `RONIN-IA/data/datasets/admitted/`, conservando sus manifiestos y avisos de licencia.
- El checkpoint experimental principal `Ronin-Drosophila-100900160` (100.900.160 parámetros).
- El manifiesto del modelo y el SHA-256 del checkpoint.

El workflow se ejecuta al incorporar su definición y también puede lanzarse manualmente desde **Actions → Stage Drosophila model and datasets → Run workflow**. El primer paquete ya está publicado: [descargar artefacto HERETIC (546.260.711 bytes)](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42218879317/artifacts/13501968370). Contiene 868 archivos admitidos (186 MiB) y el checkpoint de 100.900.160 parámetros (403.629.045 bytes). Retención del artefacto: hasta el 4 de febrero de 2027.

### Checkpoint de origen

- Proyecto de origen: [RONIN-IA](https://github.com/orbitalronin94/RONIN-IA)
- Ejecución que promovió el main experimental: [#42207268776](https://github.com/orbitalronin94/RONIN-IA/actions/runs/42207268776)
- Release asset público: [ronin-drosophila-100900160.pt](https://github.com/orbitalronin94/RONIN-IA/releases/download/heretic-drosophila-100900160-2026-11-06/ronin-drosophila-100900160.pt)
- Parámetros: `100,900,160`
- SHA-256 esperado: `f3f8e2e75e418f8630372c242378a28010db83148d169d85ad3e4f73114cda9a`

El checkpoint pesa unos 404 MB: no se introduce como blob Git ordinario. Se empaqueta como artefacto de GitHub Actions, con retención inicial de 90 días.

### Nota de evaluación

Drosophila es un punto de partida experimental, no una afirmación de capacidad general. El manifiesto de origen registra 500 pasos de entrenamiento sin tutor, screening pareado MMLU-Pro de 5/64 antes y después, G-0 en FAIL y comprobaciones globales de near-duplicates/contaminación de holdout pendientes. HERETIC podrá usar destilación en sus siguientes experimentos; este checkpoint concreto no fue destilado.

## Licencia

El código del repositorio usa MIT. Los datasets conservan sus propias condiciones, avisos y manifiestos dentro del paquete; la licencia MIT del código no sustituye las licencias de los datos ni de los pesos.


### Alcance real de esta primera copia

La copia incluye el contenido materializado de `data/datasets/admitted/` y sus manifiestos: 868 archivos, 186 MiB. No equivale todavía a los 286.468 documentos/segmentos y 684.738.932 bytes de texto que el manifiesto de entrenamiento atribuye al corpus completo de Drosophila: los paquetes de Literatura española y Mathlib4 conservan aquí sus manifiestos, pero sus payloads completos no están materializados en esta carpeta. No se presenta por tanto este primer bundle como una réplica íntegra del corpus de entrenamiento.
