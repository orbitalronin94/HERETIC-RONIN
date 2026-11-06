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

1. **Adquirir un instructor de primera línea.** Candidato inicial: [Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B), modelo abierto de 27B parámetros con licencia Apache-2.0. Se conservará la referencia exacta del modelo, su licencia, revisión y hashes. La cuantización elegida se registrará como parte del experimento: no se tratará una versión GGUF cuantizada como si fueran los pesos originales.
2. **Ejecutar 100 pasos de preparación del estudiante de 500M** mientras avanza la descarga del instructor. Este primer tramo será una prueba de viabilidad: pérdida, tiempo por paso, memoria, throughput y checkpoint. No se presentará como una mejora de capacidad ni como una evaluación final.

### Regla de adquisición

La versión Q4_K_M del instructor de 27B ocupa aproximadamente 15–17 GB según la distribución consultada; eso excede el margen cómodo de un runner estándar. Por tanto, el trabajo de descarga debe resolver primero el almacenamiento disponible y el formato de persistencia. No se reducirá silenciosamente a una cuantización extrema para poder anunciar que «ya está descargado». Si hace falta una cuantización menor, se documentará su coste de calidad y se comparará antes de usarla para generar datos.

**Orden de operaciones:** instructor en adquisición + 100 pasos en paralelo → verificación del instructor → destilación controlada → escalado y evaluación del estudiante de 500M.

Los 100 pasos son un arranque técnico, no una promesa de rendimiento. El primer resultado válido será el que sobreviva a una comparación medible.

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
