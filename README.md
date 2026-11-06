# HERETIC-RONIN
### MODELO LARGO. MÉTODO CORTO.

*La mosca no necesitaba pureza. Necesitaba sobrevivir.*

> «La pureza del método es un lujo de quienes pueden permitirse llegar tarde.»

Hay quienes contemplan una criatura diminuta y ven sus límites.  
Él contempló la mosca y vio una arquitectura que todavía no sabía lo que podía llegar a ser.

RONIN-IA había elegido el camino largo: procedencia, acreditación, corpus medido, experimentos reproducibles, controles y una paciencia casi monástica. Un método admirable. También un método que, a ojos de HERETIC, estaba empezando a devorar el intelecto que debía servir.

El personaje que funda este laboratorio no desprecia el conocimiento. Desprecia arrodillarse ante el procedimiento hasta olvidar para qué se quería conocer.

Vio potencial en Drosophila. Copió sus pesos. Se llevó los datasets que pudo reunir. Y decidió que, si había una forma más rápida de enseñar a una máquina, no iba a descartarla por no ser pura.

No busca absolución metodológica. Busca capacidad.

---

## I. El pecado original

**Drosophila — 100.900.160 parámetros.**

La primera adquisición de HERETIC es el checkpoint experimental de la mosca, procedente de RONIN-IA. No fue destilado: nació de un entrenamiento propio de 500 pasos. HERETIC lo adopta no como reliquia ni como prueba de inteligencia, sino como materia prima.

- **Modelo:** `Ronin-Drosophila-100900160`
- **Parámetros:** 100.900.160
- **Checkpoint:** aproximadamente 404 MB
- **SHA-256:** `f3f8e2e75e418f8630372c242378a28010db83148d169d85ad3e4f73114cda9a`
- **Origen:** [RONIN-IA](https://github.com/orbitalronin94/RONIN-IA)
- **Ejecución de origen:** [Actions #42207268776](https://github.com/orbitalronin94/RONIN-IA/actions/runs/42207268776)
- **Pesos:** [Descargar checkpoint](https://github.com/orbitalronin94/RONIN-IA/releases/download/heretic-drosophila-100900160-2026-11-06/ronin-drosophila-100900160.pt)

La mosca no es el resultado final. Es el primer cuerpo sobre la mesa.

## II. Dos hermanos. Ninguna obediencia compartida.

| RONIN-IA | HERETIC-RONIN |
|---|---|
| Procedencia como disciplina central | Procedencia pragmática |
| Corpus acreditado y controlado | Datos heterogéneos y destilación |
| Reproducibilidad como requisito | Velocidad de experimentación |
| Aprendizaje sin depender de profesores externos | Profesores, síntesis y transferencia de capacidad |
| Pureza experimental | Herejía experimental |

No son dos nombres para el mismo proyecto. Son dos respuestas incompatibles a una pregunta común:

**¿Cuánta capacidad puede extraerse de un presupuesto limitado?**

RONIN-IA intenta responder sin atajos. HERETIC quiere probar todos los atajos que puedan medirse.

## III. El laboratorio

HERETIC-RONIN está destinado a experimentar con:

- **Destilación:** transferir conocimiento desde modelos docentes más capaces.
- **Datos sintéticos:** generar, filtrar y combinar ejemplos a escala.
- **Ensembles de profesores:** enfrentar varias fuentes de conocimiento y contrastar sus respuestas.
- **Entrenamiento agresivo:** probar recetas, mezclas, currículos y configuraciones sin reverencia por la ortodoxia.
- **Compresión y transferencia:** buscar más capacidad por parámetro, paso y unidad de cómputo.
- **Torneos de candidatos:** comparar variantes contra una referencia común y conservar las que demuestren mejoras.

Aquí una técnica no se acepta por elegante ni se rechaza por impura. Se somete a prueba. Si funciona, se estudia. Si fracasa, se archiva. Si parece funcionar pero no resiste una evaluación independiente, se considera derrotada.

## IV. Primer experimento: el salto a 500 millones

**Objetivo:** escalar la mosca desde 100.900.160 hasta aproximadamente **500.000.000 de parámetros**.

HERETIC no empezará ese salto a ciegas. La primera campaña tendrá dos trabajos paralelos:

1. **Adquirir un instructor de primera línea.** Candidato inicial: [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B), mediante el paquete GGUF Q4_K_M de [SoAIHQ](https://huggingface.co/SoAIHQ/Qwen3.5-4B-GGUF). Tiene 4B de parámetros, licencia Apache-2.0 y ocupa 2,78 GB en Q4_K_M. Se conservará la referencia exacta del modelo, su licencia, revisión y hashes. La cuantización elegida se registrará como parte del experimento: no se tratará una versión GGUF cuantizada como si fueran los pesos originales.
2. **Ejecutar 100 pasos de preparación del estudiante de 500M** mientras avanza la descarga del instructor. Este primer tramo será una prueba de viabilidad: pérdida, tiempo por paso, memoria, throughput y checkpoint. No se presentará como una mejora de capacidad ni como una evaluación final.

### Regla de adquisición

La cuantización Q4_K_M conserva una calidad alta para su tamaño y cabe holgadamente en el runner público estándar de GitHub Actions (4 vCPU, 16 GB RAM y 14 GB SSD). El artefacto se valida contra el SHA-256 publicado por el distribuidor; se guardan revisión de Hugging Face, licencia, cuantización y hash.

**Orden de operaciones:** adquisición y verificación del instructor + 100 pasos del estudiante en paralelo → destilación controlada → escalado y evaluación del estudiante de 500M. Los primeros 100 pasos parten de inicialización aleatoria y corpus admitido; todavía no son destilación ni heredan los pesos de Drosophila.

La arquitectura del estudiante está fijada en **500.102.144 parámetros** (39 capas, ancho 1.024, 16 cabezas, contexto 128 y vocabulario byte). La primera ejecución paralela está en [GitHub Actions, run 42220254879](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42220254879). El instructor **se descargó, pasó el SHA-256 del distribuidor y quedó archivado**: [artefacto Qwen3.5-4B Q4_K_M](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42220358202/artifacts/13502524840), 2.783.448.214 bytes; SHA-256 del GGUF `2ebe6eb67cb92adeffc7073c48dd4e3baf79465ac650793dc751cad2b29cf219`. El primer intento del estudiante se detuvo antes del paso 1 por una dependencia `numpy` ausente; quedó corregida y el segundo intento [terminó correctamente en el run 42220358202](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42220358202). Completó **100 pasos**, con 500.102.144 parámetros, pérdida de entrenamiento de 5,60465 a 3,28351 y un checkpoint de 2.000.546.658 bytes: [artefacto del estudiante, ID 13503178199](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42220358202/artifacts/13503178199). Usó 96 MiB de texto de 834 archivos. No utilizó el instructor durante esos 100 pasos; la bajada de loss solo acredita ajuste sobre ese corpus, no capacidad ni generalización.


## IV bis. Segundo experimento: razonamiento multidominio

El siguiente ciclo ya está implementado en [el workflow de destilación multidominio](.github/workflows/multidomain-distillation-holdout.yml) y documentado en [Ciclo 001](docs/MULTIDOMAIN_DISTILLATION_CYCLE_001.md). Su regla central es innegociable: **continúa desde el checkpoint de 500M del paso 100; no crea un estudiante nuevo ni reinicializa los pesos**.

1. Recupera y verifica el artefacto del run 42220358202.
2. Usa Qwen3.5-4B Q4_K_M como instructor para producir 1.000 ejemplos en seis dominios: matemáticas, programación, lógica, ciencias naturales, lengua e interdisciplinar.
3. Continúa el estudiante durante 500 pasos adicionales, supervisando respuestas y explicaciones breves.
4. Al final compara las mismas 60 preguntas de holdout, no vistas por el instructor, contra **RONIN-IA Drosophila experimental main**, el modelo de método largo de 100.900.160 parámetros.

El holdout es un diagnóstico sintético pequeño, no un benchmark oficial. Las respuestas del instructor pasan controles de formato y duplicados, pero no una verificación semántica independiente. El contexto del estudiante sigue limitado a 128 bytes. No se promocionará ningún checkpoint automáticamente: primero tendrán que hablar las predicciones por dominio.

## V. La primera carga

El primer bootstrap ya ha sido ejecutado correctamente.

<details>
<summary>Contenido del paquete inicial</summary>

- **Artefacto:** [heretic-drosophila-100900160-and-admitted-datasets](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42218879317/artifacts/13501968370)
- **Tamaño total:** 546.260.711 bytes
- **Archivos:** 868
- **Payload materializado de datasets:** 186 MiB
- **Checkpoint:** 403.629.045 bytes
- **Digest del artefacto:** `sha256:15c998a5319e5a579eebac0fd84667ff59f49ad862a151f32b663d4bdbf06928`
- **Retención prevista:** hasta el 4 de febrero de 2027.

El workflow [`.github/workflows/bootstrap.yml`](.github/workflows/bootstrap.yml) vuelve a preparar el paquete desde las fuentes de RONIN-IA y verifica el SHA-256 del checkpoint antes de publicarlo.

</details>

### La adquisición no está completa

La primera copia contiene 868 archivos y 186 MiB de payload materializado bajo `data/datasets/admitted/`. No equivale todavía al corpus íntegro que el manifiesto de entrenamiento atribuye a Drosophila: 286.468 documentos/segmentos y 684.738.932 bytes de texto.

Los payloads completos de Literatura española y Mathlib4 aún no están materializados en esta copia. Sus manifiestos se conservan. La transferencia se considera **parcial**, no completa.

## VI. La inteligencia no se proclama

El villano puede odiar la pureza del método. No puede permitirse confundir arrogancia con evidencia.

El checkpoint de origen tiene límites conocidos:

- 500 pasos de entrenamiento, sin tutor ni destilación.
- Screening pareado MMLU-Pro: 5/64 antes y 5/64 después.
- G-0: FAIL.
- Comprobaciones globales de near-duplicates y contaminación del holdout: pendientes.

Estos resultados no demuestran capacidad general ni una mejora en MMLU-Pro. Son el estado documentado de partida. HERETIC no los maquillará para convertir una adquisición en una victoria.

La evaluación no es una religión. Es el instrumento que permite distinguir un avance de una fantasía.

## VII. La única herejía imperdonable

No es destilar.  
No es sintetizar.  
No es copiar una arquitectura prometedora.  
No es aprender de un modelo más grande.

La herejía imperdonable sería **dejar de medir porque el resultado nos gusta**.

HERETIC puede renunciar a la pureza de método. No renunciará a comparar candidatos, registrar configuraciones, conservar los fallos y comprobar si una mejora sobrevive fuera de sus propios ejemplos.

No promete ser limpio. Promete ser peligroso para las ideas que no funcionan.

---

## Estado del proyecto

<sub>Laboratorio experimental · Modelos pequeños · Destilación · Datos sintéticos · Transferencia de capacidad</sub>

**La mosca fue copiada porque alguien vio en ella algo que el método todavía no había conseguido liberar.**

*Que empiece la herejía.*
 
---

## Licencias y materiales

El código de este repositorio se distribuye bajo MIT. Los datasets, checkpoints, modelos docentes y materiales externos conservan sus propias licencias, condiciones de uso y atribuciones. La licencia MIT del repositorio no sustituye ni amplía los derechos sobre esos materiales.
