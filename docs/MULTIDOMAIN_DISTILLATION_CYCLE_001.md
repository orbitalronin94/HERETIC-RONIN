# Ciclo 001 — Destilación de razonamiento multidominio

## Hipótesis

Un estudiante HERETIC de 500.102.144 parámetros puede continuar aprendiendo desde su checkpoint de 100 pasos mediante ejemplos sintéticos creados por un instructor de 4B, y después medirse en las mismas preguntas que el modelo experimental principal de RONIN-IA.

**No se reinicializa el estudiante.** El punto de partida obligatorio es el artefacto heretic-student-500m-first-100-steps del run [42220358202](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42220358202), artifact [13503178199](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42220358202/artifacts/13503178199). Su digest de archivo es:

sha256:035e7671f798cc9aa9f52e6b72a8d4e7dfb11433868012dee781a37b38e9e972

El workflow verifica ese digest antes de extraer el checkpoint y comprueba que el metadata interno declara el paso 100 y los 500.102.144 parámetros esperados.

## Instructor

- Modelo: [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B)
- Paquete: [SoAIHQ/Qwen3.5-4B-GGUF](https://huggingface.co/SoAIHQ/Qwen3.5-4B-GGUF)
- Archivo: Qwen3.5-4B-Q4_K_M.gguf
- Cuantización: Q4_K_M
- SHA-256 esperado: 2ebe6eb67cb92adeffc7073c48dd4e3baf79465ac650793dc751cad2b29cf219
- Licencia declarada por el distribuidor: Apache-2.0

El instructor genera 1.000 ejemplos, distribuidos en seis dominios:

| Dominio | Ejemplos |
|---|---:|
| Matemáticas | 167 |
| Programación | 167 |
| Lógica | 167 |
| Ciencias naturales | 167 |
| Lengua | 166 |
| Interdisciplinar | 166 |
| **Total** | **1.000** |

Cada registro conserva pregunta, respuesta y explicación breve. Se comprueban estructura, longitudes y duplicados. **No se afirma que las respuestas del instructor estén verificadas semánticamente**: esta primera iteración no incorpora un verificador independiente del contenido de entrenamiento.

## Continuación del estudiante

- Checkpoint de partida: 500M, paso 100.
- Checkpoint de salida: paso 600 (100 pasos iniciales + 500 pasos de destilación).
- Optimizador: AdamW.
- Tasa máxima: 1e-5 con warm-up de 20 pasos.
- Loss: únicamente sobre los bytes de respuesta y explicación; los bytes de pregunta sirven como contexto y no reciben loss.
- Tokenizador: byte-v1.
- Contexto: 128 bytes, sin ampliar la arquitectura ni cambiar el tokenizador.
- Dispositivo previsto: CPU en GitHub Actions.

La ventana de 128 bytes es una limitación importante: obliga a usar preguntas y explicaciones concisas y limita la profundidad de razonamiento que este ciclo puede enseñar. No se ocultará ni se reinterpretará como una arquitectura de contexto largo.

## Comparación final: contra el método largo

El holdout local contiene 60 preguntas deterministas, diez por dominio. Se genera dentro del script, después de preparar el conjunto de entrenamiento, y no se envía al instructor.

Se compara, con las mismas preguntas y decodificación greedy:

1. **RONIN-IA — Drosophila experimental main:** 100.900.160 parámetros, derivado del checkpoint ganador de 10.000 pasos y continuado durante 500 pasos. Checkpoint publicado con SHA-256 f3f8e2e75e418f8630372c242378a28010db83148d169d85ad3e4f73114cda9a.
2. **HERETIC — estudiante 500M destilado:** los mismos pesos de partida del paso 100, continuados durante 500 pasos de SFT multidominio.

El resultado se puntúa por coincidencia exacta de la primera línea normalizada y se desglosa por dominio. Se guardan todas las predicciones, respuestas esperadas y aciertos en paired-holdout-results.json.

Esta comparación es un diagnóstico sintético pequeño, no un benchmark oficial ni una certificación de razonamiento general. Los dos modelos tienen arquitecturas y tamaños distintos; la lectura correcta será qué modelo resuelve mejor este conjunto concreto bajo el mismo protocolo, no quién es universalmente superior.

## Artefactos esperados

El workflow .github/workflows/multidomain-distillation-holdout.yml publica:

- teacher-multidomain-1000.jsonl y teacher-dataset-manifest.json
- student-500m-multidomain-distilled.pt
- paired-holdout-results.json
- experiment-report.json
- Log del servidor instructor.

No se promociona automáticamente ningún checkpoint. La promoción requiere revisar el holdout, las predicciones por dominio y la integridad del artefacto.

## Cambios operativos tras el primer fallo

La siguiente iteración sustituye la compilación de llama.cpp y el servidor HTTP por inferencia GGUF en proceso mediante una rueda CPU precompilada de llama-cpp-python. No se levanta llama-server ni se abre un endpoint local.

La generación es reanudable: cada ejemplo aceptado se escribe en JSONL, se hace flush y fsync, y se reconstruye el recuento por dominio al reiniciar. Si la última escritura quedó truncada por una interrupción, se recuperan las líneas completas anteriores. El parser busca el primer objeto JSON completo con JSONDecoder.raw_decode y tolera texto o fences alrededor del objeto.

Antes de entrenar se exige el total exacto de 1.000 ejemplos y la distribución 167/167/167/167/166/166. La instalación exige una rueda binaria CPU de llama-cpp-python==0.3.36; si no existe una rueda compatible, el job falla explícitamente y no compila silenciosamente desde fuentes.

El instructor se cierra y libera antes de cargar el estudiante 500M y el optimizador. La limitación de calidad no cambia: las respuestas del instructor solo pasan controles estructurales, de longitud y duplicados; no se presentan como verificadas semánticamente. El holdout sintético tampoco equivale a un benchmark oficial.
