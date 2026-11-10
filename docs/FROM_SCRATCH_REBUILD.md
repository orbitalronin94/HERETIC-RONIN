# HERETIC-RONIN: reconstrucción desde cero

## Decisión de arquitectura

HERETIC-RONIN se reconstruye como una implementación independiente del modelo decoder-only de MINIRONIN/MAXIRONIN. Se conserva la topología de 500M auditada: 37 bloques Transformer, ancho 1.024, 16 cabezas, FFN 4.096, contexto 512 y vocabulario BPE byte-level de 32.768 entradas. Las matrices de embedding de entrada y salida están ligadas.

**No se importan pesos ni estados de optimizador.** Cada ejecución de entrenamiento desde cero crea una inicialización nueva y reproducible por semilla. No se permite cargar el checkpoint histórico de HERETIC ni un checkpoint de MINIRONIN/MAXIRONIN.

## Filas de vocabulario desbloqueadas

Las 32.768 filas de la matriz de embeddings pertenecen al mismo parámetro entrenable; no hay máscaras, rangos congelados, inicialización tardía ni exclusiones de gradiente. El LM head comparte exactamente ese parámetro. El trainer debe auditar `requires_grad=True` para todos los parámetros y comprobar que embedding y LM head comparten almacenamiento.

## Tokenizador nuevo

Se entrenará un byte-level BPE nuevo sobre el corpus train aprobado de HERETIC-RONIN, con normalización Unicode NFC, alfabeto byte-level completo y tokens especiales explícitos. El tokenizador se entrenará antes de inicializar el modelo y quedará congelado para toda la vida de ese checkpoint. No se reutilizarán IDs ni merges del tokenizador anterior. El manifiesto guardará SHA-256 del tokenizador, corpus de entrenamiento, configuración y recuentos.

El tamaño inicial se mantiene en 32.768 para preservar la escala de parámetros de la arquitectura MAXIRONIN auditada; la mejora de calidad debe venir de aprender merges desde el corpus real, no de ampliar arbitrariamente la matriz.

## Reglas de entrenamiento y evaluación

1. Crear modelo desde cero con semilla declarada; verificar recuento total/entrenable y ausencia de pesos heredados.
2. Separar train/validation/holdout por manifiesto y procedencia antes de entrenar el tokenizador.
3. Tokenizar solo train y validation con el tokenizador nuevo; el holdout no participa en entrenamiento ni en selección de merges.
4. Registrar SHA-256 de corpus, tokenizador, configuración, código y checkpoint.
5. Cada tramo registra evaluación antes/después con el mismo holdout, mismas preguntas y mismo decodificador; resultados por dominio y predicciones completas.
6. No promover por pérdida de train, número de pasos o tamaño del corpus. La promoción requiere mejora reproducible frente al baseline y revisión del holdout.

## Fases de refactor

- [x] Añadir paquete de arquitectura independiente con todas las filas entrenables.
- [ ] Añadir tokenizador BPE byte-level nuevo y pruebas de round-trip multilingüe.
- [ ] Sustituir los trainers heredados por un trainer único de inicialización aleatoria.
- [ ] Rehacer workflows de corpus, entrenamiento segmentado, holdout y artefactos.
- [ ] Retirar workflows de continuación heredada una vez que los reemplazos estén validados.
- [ ] Ejecutar smoke test pequeño y luego primer entrenamiento real desde cero.

Los workflows son la fuente de verdad operativa. El checkpoint histórico permanece como evidencia archivada y nunca será una inicialización válida para el nuevo modelo.
