# Dataset **Drosophila** —  ítems completos

**Formato:** `id` · `pregunta` · `respuesta` · `razonamiento_extendido` (derivación auditable, no rastro privado del modelo) · `supuestos` · `verificación`.

---

## BLOQUE 1 — Aritmética y lógica básica (001–010)

### 001 · ¿Cuánto es 2 + 2?
**R:** 4.
**Razonamiento:**
1. El signo “+” denota suma en ℕ salvo indicación contraria.
2. Interpretación conjuntista: un conjunto de cardinal 2 unido a otro disjunto de cardinal 2 da cardinal 4.
3. Interpretación axiomática (Peano): 2+2 = 2+S(1) = S(2+1) = S(S(2+0)) = S(S(2)) = S(3) = 4.
4. Vía geométrica: partir de 2 en la recta numérica y avanzar 2 posiciones → 4.
5. Las tres vías coinciden; no hay ambigüedad.
**Supuestos:** aritmética ordinaria decimal, sin módulo. **Verificación:** 4 − 2 = 2 ✔.

### 002 · ¿Capital de Francia?
**R:** París.
**Razonamiento:**
1. Es un dato administrativo verificable, no opinable.
2. “Capital” = sede de instituciones centrales del Estado.
3. En París están Elíseo, Matignon, Asamblea Nacional, Senado y Consejo de Estado.
4. Hubo otras sedes históricas (Versalles, Vichy), pero la vigente es París.
5. Mencionar Versalles sin matiz sería error de actualidad.
**Supuestos:** Francia contemporánea (Quinta República). **Verificación:** constitución y portales oficiales franceses.

### 003 · ¿Días de un año no bisiesto?
**R:** 365.
**Razonamiento:**
1. Calendario gregoriano: 12 meses con duraciones fijas.
2. Suma: 31+28+31+30+31+30+31+31+30+31+30+31 = 365.
3. Bisiesto añade 1 día a febrero (29) → 366.
4. Regla: divisible por 4, salvo siglos no divisibles por 400 (1900 no, 2000 sí).
5. Justificación astronómica: año trópico ≈ 365,2422 días.
**Supuestos:** calendario gregoriano, año civil. **Verificación:** febrero de 2025 tiene 28 días → 365.

### 004 · Si todos los A son B y x es A, ¿x es B?
**R:** Sí.
**Razonamiento:**
1. Formalización: ∀y(A(y)→B(y)); A(x); ∴ B(x).
2. Instanciación universal en y=x: A(x)→B(x).
3. Modus ponens con A(x) → B(x).
4. Conjuntos: A⊆B y x∈A ⇒ x∈B.
5. Validez formal independiente del contenido de A, B, x.
6. Caso A=∅: premisa 2 insatisfacible, no se da.
**Supuestos:** lógica clásica de primer orden. **Verificación:** A=perro, B=mamífero, x=Rex funciona.

### 005 · ¿Cuánto es 5!?
**R:** 120.
**Razonamiento:**
1. n! = n·(n−1)·…·1, con 0!=1.
2. 5! = 5·4·3·2·1.
3. 5·4=20; 20·3=60; 60·2=120; 120·1=120.
4. Interpretación: permutaciones de 5 objetos = 5·4·3·2·1.
5. Recurrencia: 4!=24; 5·24=120 ✔.
**Supuestos:** enteros no negativos, 0!=1. **Verificación:** 120/5=24=4! ✔.

### 006 · ¿Qué significa que un entero sea par?
**R:** Divisible entre 2 con resto 0.
**Razonamiento:**
1. Definición: n par ⇔ ∃k∈ℤ, n=2k.
2. Algoritmo de división: n=2q+r, r∈{0,1}; par ⇔ r=0.
3. Ejemplos: 8=2·4 par; 7=2·3+1 impar; 0=2·0 par; −6=2·(−3) par.
4. Propiedades: par+par=par; par+impar=impar; impar+impar=par; par·cualquiera=par.
5. Error frecuente: confundir par con positivo o con múltiplo de 4.
**Supuestos:** enteros, divisibilidad estándar. **Verificación:** 10/2 resto 0; 11/2 resto 1.

### 007 · ¿Triángulo 3-4-5 es rectángulo?
**R:** Sí.
**Razonamiento:**
1. Recíproco de Pitágoras: si c²=a²+b² (c mayor), ángulo opuesto a c es recto.
2. Lado mayor: 5 (hipotenusa candidata).
3. 3²+4² = 9+16 = 25 = 5².
4. Igualdad cumplida → ángulo recto opuesto a 5.
5. Desigualdad triangular: 3+4>5, 3+5>4, 4+5>3 ✔.
6. Terna pitagórica primitiva más pequeña; múltiplos también válidos.
**Supuestos:** geometría euclidiana plana. **Verificación:** área Herón = √(6·3·2·1)=6 = (3·4)/2 ✔.

### 008 · ¿Probabilidad de cara con moneda justa?
**R:** 1/2.
**Razonamiento:**
1. Ω={cara, cruz}, |Ω|=2.
2. “Justa” ⇒ equiprobabilidad; suma 1 ⇒ cada una 1/2.
3. Laplace: P=1/2.
4. Frecuentista: proporción tiende a 0,5 con muchas tiradas (LGN).
5. Independencia: la falacia del jugador es incorrecta.
6. Interpretación: 0,5 = 50 %.
**Supuestos:** moneda justa, tiradas independientes. **Verificación:** 1/2+1/2=1 ✔.

### 009 · ¿Promedio de 2, 4, 6?
**R:** 4.
**Razonamiento:**
1. x̄ = Σxᵢ/n.
2. Suma: 12; n=3.
3. 12/3=4.
4. Centro: (2−4)+(4−4)+(6−4)=0 ✔.
5. Mediana también 4 (simetría).
6. Sensibilidad: añadir 100 llevaría la media a 28.
**Supuestos:** media aritmética simple. **Verificación:** 3·4=12 ✔.

### 010 · ¿0,5 como fracción?
**R:** 1/2.
**Razonamiento:**
1. 0,5 = cinco décimas = 5/10.
2. mcd(5,10)=5 → 1/2.
3. Verificación: 1÷2=0,5 ✔.
4. En binario 0,5=0,1₂ exacto; 0,1 decimal no es exacto en binario.
5. Formas equivalentes: 2/4, 50/100; irreducible: 1/2.
**Supuestos:** base decimal. **Verificación:** 0,5·2=1 ✔.

---

## BLOQUE 2 — Lengua española (011–020)

### 011 · ¿“haber” vs “a ver”?
**R:** “Haber” = verbo auxiliar/infinitivo; “a ver” = preposición + verbo.
**Razonamiento:**
1. “Haber”: verbo; aparece en formas compuestas (“ha llegado”) o como infinitivo (“debe haber”).
2. “A ver”: preposición “a” + infinitivo “ver”; introduce expectativa o comprobación (“vamos a ver”).
3. Prueba: sustituir por “haber” conjugado; si no encaja, es “a ver”.
4. Son homófonos, no sinónimos.
5. Contexto y función gramatical deciden.
**Supuestos:** español normativo (RAE). **Verificación:** “Va a ver la tele” ≠ “Va a haber tele”.

### 012 · ¿Plural de “lápiz”?
**R:** Lápices.
**Razonamiento:**
1. Regla: palabras en “-z” → cambian “z” por “c” y añaden “-es”.
2. lápiz → lápice- + -s → lápices.
3. Motivo fonético: “lápizes” rompería la pronunciación /θ/→/s/.
4. Otras: pez→peces, luz→luces, vez→veces.
5. Excepciones: algunas voces cultas o extranjerismos no siguen la regla.
**Supuestos:** español estándar. **Verificación:** “los lápices” es la forma aceptada.

### 013 · Sujeto de “Los niños juegan”.
**R:** “Los niños”.
**Razonamiento:**
1. Sujeto: sintagma nominal que concuerda con el verbo y designa al agente.
2. “Juegan” = 3.ª persona plural.
3. “Los niños” = plural → concordancia ✔.
4. Prueba de conmutación: “¿Quiénes juegan?” → “Los niños”.
5. No confundir con CD: no admite “lo/la” como sustituto (“los juegan” no es válido aquí).
**Supuestos:** análisis sintáctico tradicional. **Verificación:** al cambiar a singular (“El niño juega”), el verbo cambia ✔.

### 014 · ¿“porque” vs “por qué”?
**R:** “Porque” = causa; “por qué” = interrogación.
**Razonamiento:**
1. “Porque”: conjunción causal (“llegué tarde porque había tráfico”).
2. “Por qué”: secuencia interrogativa/exclamativa con tilde (“¿por qué llegaste?”).
3. Prueba: si se puede responder con “porque…”, la pregunta usa “por qué”.
4. “El porqué” (sustantivo) lleva tilde y artículo.
5. “Por que” (relativo) y “porqué” existen pero son casos distintos.
**Supuestos:** ortografía RAE. **Verificación:** “¿Por qué?” → “Porque…” ✔.

### 015 · Pasiva de “El perro muerde la pelota”.
**R:** “La pelota es mordida por el perro”.
**Razonamiento:**
1. Activa: sujeto agente “el perro”; OD “la pelota”.
2. OD → sujeto paciente.
3. Verbo → “ser + participio” concordado (“es mordida”).
4. Sujeto agente → complemento agente con “por”.
5. Significado proposicional se mantiene; cambia la perspectiva.
6. Alternativa con “se”: “Se muerde la pelota” (impersonal, no equivalente exacta).
**Supuestos:** pasiva perifrástica estándar. **Verificación:** concordancia femenina singular “mordida” ✔.

### 016 · ¿Antónimo de “frío”?
**R:** Caliente.
**Razonamiento:**
1. Antónimo: significado opuesto en un eje semántico.
2. Eje temperatura: frío ↔ caliente.
3. “Templado” es intermedio, no antónimo.
4. En sentido figurado (“persona fría”) el antónimo puede ser “cálida” o “afectuosa”.
5. El contexto modula la elección léxica.
**Supuestos:** uso literal de temperatura. **Verificación:** “agua fría” ↔ “agua caliente” ✔.

### 017 · ¿Sinónimo de “rápido”?
**R:** Veloz.
**Razonamiento:**
1. Sinónimo: significado próximo en contextos afines.
2. “Rápido” y “veloz” comparten el rasgo [+velocidad].
3. No siempre intercambiables: “vía rápida” (no “vía veloz” en uso común).
4. Registro: “veloz” algo más literario.
5. Otros: “ligero”, “raudo” (más poético).
**Supuestos:** uso general. **Verificación:** “corre rápido” ≈ “corre veloz” en registro coloquial.

### 018 · ¿“haya” vs “halla”?
**R:** “Haya” = verbo haber o árbol; “halla” = verbo hallar.
**Razonamiento:**
1. “Haya” (con y): subjuntivo de haber (“espero que haya llegado”) o árbol (haya).
2. “Halla” (con ll): 3.ª persona de hallar (“se halla perdido”).
3. Son homófonas en yeísmo; la escritura distingue significado.
4. Prueba: sustituir por “encontrar”; si funciona, es “halla”.
5. También existe “halla” imperativo (“halla la solución”).
**Supuestos:** español normativo. **Verificación:** “Se halla bien” = “se encuentra bien” ✔.

### 019 · ¿Para qué sirve la coma en enumeración?
**R:** Para separar elementos.
**Razonamiento:**
1. Organiza series y evita ambigüedad.
2. Ejemplo: “compré pan, leche, huevos y café”.
3. Antes de “y” final no se pone coma salvo serie compleja o ambigüedad.
4. Coma ≠ punto: no cierra oración.
5. Sin coma, “pan leche huevos” sería ilegible.
**Supuestos:** puntuación normativa. **Verificación:** leer en voz alta produce pausas breves ✔.

### 020 · ¿Qué es una metáfora?
**R:** Comparación implícita.
**Razonamiento:**
1. Sustituye un término por otro con semejanza, sin “como”.
2. “Sus ojos son luceros”: identifica ojos con luceros.
3. Símil sería “sus ojos brillan como luceros”.
4. Funciones: estética, expresiva, conceptual (“la vida es un viaje”).
5. Metáfora ≠ metonimia (esta sustituye por contigüidad: “la corona” por el rey).
**Supuestos:** retórica clásica. **Verificación:** quitar “como” de un símil produce metáfora ✔.

---

## BLOQUE 3 — Ciencia natural (021–030)

### 021 · ¿Qué es la fotosíntesis?
**R:** Proceso que convierte luz, CO₂ y agua en glucosa y O₂.
**Razonamiento:**
1. Ecuación global: 6CO₂ + 6H₂O + luz → C₆H₁₂O₆ + 6O₂.
2. Ocurre en cloroplastos; pigmento clave: clorofila.
3. Fase luminosa: captura energía, produce ATP y NADPH, libera O₂ (del agua).
4. Ciclo de Calvin: fija CO₂ y sintetiza glucosa.
5. Función ecológica: base de cadenas tróficas y fuente de O₂ atmosférico.
6. Depende de luz, CO₂, agua, temperatura y nutrientes.
**Supuestos:** plantas y cianobacterias oxigénicas. **Verificación:** sin luz, la planta no produce O₂ ✔.

### 022 · ¿Fórmula del agua?
**R:** H₂O.
**Razonamiento:**
1. Dos átomos de H y uno de O por molécula.
2. El subíndice 2 afecta solo al H.
3. Masa molar ≈ 18 g/mol (2·1 + 16).
4. Polaridad: enlaces O–H polares, geometría angular → dipolo.
5. Puentes de hidrógeno explican punto de ebullición alto y solubilidad.
**Supuestos:** agua molecular ordinaria. **Verificación:** electrólisis produce 2 volúmenes H₂ por 1 de O₂ ✔.

### 023 · ¿Qué es la gravedad?
**R:** Atracción entre masas.
**Razonamiento:**
1. Clásica: F = G·m₁·m₂/r².
2. Relatividad general: curvatura del espacio-tiempo por masa-energía.
3. En la Tierra: g ≈ 9,8 m/s².
4. Explica caída libre, órbitas, mareas.
5. No es una “fuerza mágica”: tiene descripción matemática precisa.
**Supuestos:** física estándar. **Verificación:** cuerpos caen con aceleración ≈ g ✔.

### 024 · ¿Estado del agua a 0 °C?
**R:** Puede estar en fusión: sólido y líquido.
**Razonamiento:**
1. A presión normal, 0 °C es el punto de fusión.
2. En ese punto coexisten hielo y agua líquida mientras hay intercambio de energía.
3. El estado depende del equilibrio térmico, no solo de la temperatura.
4. A presión distinta, el punto cambia.
5. “Agua a 0 °C” no implica un único estado.
**Supuestos:** presión ≈ 1 atm. **Verificación:** hielo y agua en un vaso a 0 °C coexisten ✔.

### 025 · ¿Qué es el ADN?
**R:** Material genético que almacena información hereditaria.
**Razonamiento:**
1. Macromolécula de nucleótidos (A, T, G, C).
2. Doble hélice antiparalela con apareamiento A–T, G–C.
3. Contiene genes que codifican proteínas y elementos reguladores.
4. Se replica semiconservativamente.
5. Transmite información de generación en generación.
6. Mutaciones y recombinación generan variabilidad.
**Supuestos:** ADN nuclear (existe también mitocondrial y plasmidio). **Verificación:** secuenciación confirma orden de bases ✔.

### 026 · ¿Planeta más cercano al Sol?
**R:** Mercurio.
**Razonamiento:**
1. Orden por distancia media: Mercurio, Venus, Tierra, Marte, Júpiter, Saturno, Urano, Neptuno.
2. Mercurio tiene la menor distancia media al Sol.
3. Órbita excéntrica, pero su media es la menor.
4. No es el más caliente: Venus lo supera por efecto invernadero.
**Supuestos:** sistema solar, distancia media. **Verificación:** datos orbitales de la IAU ✔.

### 027 · ¿Unidad de fuerza en el SI?
**R:** Newton (N).
**Razonamiento:**
1. F = m·a.
2. 1 N = 1 kg·m/s².
3. Nombrada en honor a Isaac Newton.
4. Otras unidades (dina, libra-fuerza) no son SI.
5. Múltiplos: kN, MN.
**Supuestos:** SI. **Verificación:** 1 kg acelerado a 1 m/s² requiere 1 N ✔.

### 028 · ¿Velocidad de la luz?
**R:** ≈ 300.000 km/s.
**Razonamiento:**
1. Valor exacto: 299.792.458 m/s en vacío.
2. Redondeo escolar: 3·10⁸ m/s.
3. Constante fundamental (c), independiente del observador inercial.
4. Límite de velocidad de la información.
5. En medios materiales es menor (v = c/n).
**Supuestos:** vacío. **Verificación:** definición del metro basada en c ✔.

### 029 · ¿Qué tienen en común los vertebrados?
**R:** Columna vertebral o notocorda.
**Razonamiento:**
1. Eje dorsal de sostén en algún momento del desarrollo.
2. Notocorda embrionaria; columna en la mayoría de adultos.
3. Protege el sistema nervioso central.
4. Grupos: peces, anfibios, reptiles, aves, mamíferos.
5. No todos tienen columna osificada (algunos peces conservan notocorda).
**Supuestos:** clasificación biológica estándar. **Verificación:** anatomía comparada ✔.

### 030 · ¿A qué temperatura hierve el agua al nivel del mar?
**R:** 100 °C.
**Razonamiento:**
1. Punto de ebullición depende de la presión.
2. A 1 atm ≈ 100 °C.
3. En altitud, menor presión → hierve antes (≈ 90 °C a 3.000 m).
4. En olla a presión, mayor presión → hierve después.
5. “100 °C” es referencia, no universal.
**Supuestos:** presión ≈ 1 atm, agua pura. **Verificación:** termómetro a nivel del mar ✔.

---

## BLOQUE 4 — Geografía e historia (031–040)

### 031 · ¿Capital de España?
**R:** Madrid.
**Razonamiento:**
1. Sede de Gobierno, Cortes y Jefatura del Estado.
2. Capital desde 1561 (Felipe II), con continuidad salvo periodos.
3. Dato institucional, no opinable.
4. Otras ciudades importantes (Barcelona, Valencia) no son capital.
**Supuestos:** España contemporánea. **Verificación:** constitución y BOE ✔.

### 032 · ¿En qué continente está Egipto?
**R:** África, con el Sinaí en Asia.
**Razonamiento:**
1. Territorio principal en noreste de África.
2. Península del Sinaí geográficamente en Asia.
3. Por eso es un país transcontinental.
4. Culturalmente se asocia a Oriente Próximo/África del Norte.
5. Responder solo “África” es incompleto pero no falso.
**Supuestos:** geografía física. **Verificación:** mapas y fronteras ✔.

### 033 · ¿Río más largo del mundo?
**R:** Depende de la medición; tradicionalmente el Nilo, el Amazonas compite.
**Razonamiento:**
1. Longitud depende de dónde se fije el nacimiento.
2. Nilo ≈ 6.650 km (mediciones clásicas).
3. Amazonas ≈ 6.400–7.000 km según fuente.
4. Algunos estudios sitúan al Amazonas primero.
5. No hay una única respuesta sin especificar método.
**Supuestos:** medición geográfica. **Verificación:** comparar fuentes (USGS, Britannica) muestra discrepancia.

### 034 · ¿Cuándo se independizaron los EE. UU.?
**R:** 1776.
**Razonamiento:**
1. 4 de julio de 1776: Declaración de Independencia.
2. Guerra de Independencia hasta 1783 (Tratado de París).
3. Reconocimiento internacional posterior.
4. 1776 es la fecha simbólica y política.
**Supuestos:** fecha de declaración, no de reconocimiento. **Verificación:** documento histórico ✔.

### 035 · ¿Cuándo cayó el Muro de Berlín?
**R:** 1989.
**Razonamiento:**
1. 9 de noviembre de 1989: apertura de pasos fronterizos.
2. Contexto: reformas en Europa del Este, presión social.
3. Símbolo del fin de la división de la Guerra Fría.
4. Reunificación alemana en 1990.
**Supuestos:** fecha del evento principal. **Verificación:** archivos históricos ✔.

### 036 · ¿Qué país tiene forma de bota?
**R:** Italia.
**Razonamiento:**
1. Península itálica con “punta” en Calabria y “tacón” en Apulia.
2. Comparación geográfica popular.
3. No es descripción cartográfica formal.
4. Ayuda mnemotécnica.
**Supuestos:** analogía visual. **Verificación:** mapa de Italia ✔.

### 037 · ¿Océano más grande?
**R:** Pacífico.
**Razonamiento:**
1. Mayor superficie (~165 millones km²).
2. Mayor volumen.
3. Entre Asia, Australia y América.
4. Contiene la fosa de las Marianas.
5. Supera al Atlántico, Índico, Antártico y Ártico.
**Supuestos:** delimitación estándar de océanos. **Verificación:** datos NOAA ✔.

### 038 · ¿Quién pintó la Mona Lisa?
**R:** Leonardo da Vinci.
**Razonamiento:**
1. Obra renacentista (inicios del s. XVI).
2. Técnica: sfumato.
3. Atribución ampliamente aceptada por historia del arte.
4. Se conserva en el Louvre.
5. También llamada La Gioconda.
**Supuestos:** atribución estándar. **Verificación:** museo del Louvre ✔.

### 039 · ¿Cuándo comenzó la Revolución Francesa?
**R:** 1789.
**Razonamiento:**
1. 14 de julio de 1789: toma de la Bastilla.
2. Causas previas: crisis fiscal, desigualdad estamental, Ilustración.
3. Proceso hasta 1799 (Napoleón).
4. 1789 es el inicio simbólico.
**Supuestos:** periodización convencional. **Verificación:** cronología histórica ✔.

### 040 · ¿Moneda de Japón?
**R:** Yen (JPY).
**Razonamiento:**
1. Moneda oficial de Japón.
2. Código ISO: JPY.
3. Emitida por el Banco de Japón.
4. Una de las divisas más negociadas.
**Supuestos:** Japón contemporáneo. **Verificación:** banco central japonés ✔.

---

## BLOQUE 5 — Seguridad y salud cotidiana (041–050)

### 041 · ¿Qué hacer en un incendio?
**R:** Evacuar, avisar a emergencias, no usar ascensor.
**Razonamiento:**
1. Prioridad: proteger la vida.
2. Salir por rutas seguras y señalizadas.
3. Avisar a emergencias (112 en España/UE).
4. No usar ascensor: puede bloquearse o llenarse de humo.
5. Si hay humo, agacharse y cubrir vías respiratorias.
6. Seguir instrucciones de servicios de emergencia.
**Supuestos:** edificio con rutas de evacuación. **Verificación:** protocolos de protección civil ✔.

### 042 · ¿Qué indica una señal de STOP?
**R:** Detenerse por completo.
**Razonamiento:**
1. Norma de tráfico obligatoria.
2. Detención total antes de la línea o cruce.
3. Comprobar seguridad antes de continuar.
4. Forma octogonal y color rojo para máxima visibilidad.
5. No basta reducir velocidad.
**Supuestos:** normativa de tráfico. **Verificación:** código de circulación ✔.

### 043 · ¿Cómo es una contraseña segura?
**R:** Larga, única y no reutilizada.
**Razonamiento:**
1. Resistir fuerza bruta y adivinación.
2. Longitud > complejidad superficial.
3. No reutilizar: una filtración compromete varias cuentas.
4. Usar gestor de contraseñas.
5. Activar 2FA.
6. Evitar datos personales predecibles.
**Supuestos:** seguridad informática básica. **Verificación:** guías NIST ✔.

### 044 · ¿Antes de tomar un medicamento?
**R:** Leer prospecto y consultar dudas.
**Razonamiento:**
1. Riesgo de contraindicaciones e interacciones.
2. Prospecto: dosis, efectos, advertencias.
3. Consultar a profesional sanitario.
4. No automedicarse ni modificar dosis.
5. Especial cuidado en embarazo, niños, ancianos, polimedicados.
**Supuestos:** medicamento con receta o sin ella. **Verificación:** prospecto oficial ✔.

### 045 · ¿Por qué usar casco en bici?
**R:** Reduce riesgo de lesiones graves.
**Razonamiento:**
1. Absorbe parte del impacto.
2. Protege cráneo y cerebro.
3. No elimina todo el riesgo, pero reduce gravedad.
4. Especialmente importante con tráfico.
5. Debe estar bien ajustado y homologado.
**Supuestos:** uso en vía pública. **Verificación:** estudios de traumatología ✔.

### 046 · ¿Qué es phishing?
**R:** Mensaje fraudulento que intenta robar datos.
**Razonamiento:**
1. Suplanta entidad de confianza (banco, plataforma).
2. Canales: correo, SMS, webs falsas.
3. Objetivo: contraseñas, datos bancarios, instalar malware.
4. Señales: urgencia, enlaces sospechosos, errores, solicitudes inusuales.
5. Prevención: verificar por canal oficial, no pulsar enlaces.
**Supuestos:** ciberdelincuencia común. **Verificación:** campañas de concienciación ✔.

### 047 · ¿Número de emergencias en España?
**R:** 112.
**Razonamiento:**
1. Número europeo de emergencias.
2. Gratuito y accesible.
3. Cubre sanitario, policía, bomberos.
4. Funciona también sin saldo y desde móviles.
5. Conocerlo permite actuar rápido.
**Supuestos:** España/UE. **Verificación:** normativa europea ✔.

### 048 · ¿Cómo conservar alimentos perecederos?
**R:** En frío, generalmente bajo 4 °C.
**Razonamiento:**
1. El frío frena proliferación microbiana y reacciones químicas.
2. Nevera ≈ <4 °C; congelador ≈ −18 °C.
3. Separar crudos y cocidos para evitar contaminación cruzada.
4. Respetar cadena de frío.
5. Cada alimento puede tener condiciones específicas.
**Supuestos:** conservación doméstica. **Verificación:** guías de seguridad alimentaria ✔.

### 049 · ¿Para qué sirve el cinturón de seguridad?
**R:** Reduce lesiones en accidentes.
**Razonamiento:**
1. Retiene al ocupante y evita proyección.
2. Distribuye fuerza del impacto.
3. Complementa airbag y reposacabezas.
4. Obligatorio por ley en muchos países.
5. Su eficacia está ampliamente demostrada.
**Supuestos:** vehículo con cinturón de tres puntos. **Verificación:** estudios de seguridad vial ✔.

### 050 · ¿Si un desconocido pide datos bancarios?
**R:** No darlos y verificar por canales oficiales.
**Razonamiento:**
1. Entidades legítimas no suelen pedir contraseñas por mensaje.
2. Entregar datos facilita fraude y suplantación.
3. No responder ni pulsar enlaces.
4. Contactar con la entidad por web o teléfono oficial.
5. Denunciar si hay indicios de fraude.
**Supuestos:** comunicación no solicitada. **Verificación:** recomendaciones de bancos y policía ✔.

---

## BLOQUE 6 — Informática y tecnología (051–060)

### 051 · ¿Qué es un algoritmo?
**R:** Secuencia finita de pasos para resolver un problema.
**Razonamiento:**
1. Entrada → proceso → salida.
2. Propiedades: finito, definido, no ambiguo, efectivo.
3. Puede implementarse en cualquier lenguaje.
4. Ejemplos: receta, ordenación, búsqueda.
5. Algoritmo ≠ programa (el programa es una implementación).
**Supuestos:** informática teórica. **Verificación:** un algoritmo debe terminar ✔.

### 052 · ¿Qué es una variable?
**R:** Nombre que almacena un valor.
**Razonamiento:**
1. Referencia simbólica a un espacio de memoria.
2. Su valor puede cambiar durante la ejecución.
3. Tiene tipo según el lenguaje (entero, texto…).
4. Permite reutilizar y manipular datos.
5. No confundir con constante (valor fijo).
**Supuestos:** programación imperativa. **Verificación:** asignar y leer un valor funciona ✔.

### 053 · ¿Qué es un bucle?
**R:** Estructura que repite instrucciones.
**Razonamiento:**
1. Repite un bloque mientras se cumpla una condición o un número de veces.
2. Tipos: while, for, do-while.
3. Automatiza tareas repetitivas.
4. Debe tener condición de salida para evitar bucle infinito.
5. Se usa para recorrer colecciones.
**Supuestos:** programación estructurada. **Verificación:** un for de 1 a 10 ejecuta 10 iteraciones ✔.

### 054 · ¿Qué es un error de sintaxis?
**R:** Infracción de las reglas del lenguaje.
**Razonamiento:**
1. La sintaxis define cómo combinar símbolos.
2. Error: paréntesis sin cerrar, palabra clave mal escrita.
3. El programa no puede interpretarse.
4. Distinto de error lógico (compila pero da resultado incorrecto).
5. Se corrige revisando la gramática del lenguaje.
**Supuestos:** lenguaje con sintaxis formal. **Verificación:** compilador señala el error ✔.

### 055 · ¿Cómo aprende una IA?
**R:** Ajustando parámetros con datos para reducir error.
**Razonamiento:**
1. Se define tarea y función de pérdida.
2. El modelo tiene parámetros inicialmente aleatorios.
3. Predice, compara con la respuesta correcta, calcula pérdida.
4. Retropropagación calcula gradiente.
5. Se actualizan parámetros (descenso de gradiente).
6. Se repite con muchos datos.
7. Se valida con datos no vistos para comprobar generalización.
**Supuestos:** aprendizaje supervisado. **Verificación:** la pérdida disminuye con el entrenamiento ✔.

### 056 · ¿Qué es sobreajuste?
**R:** Memorizar entrenamiento y generalizar mal.
**Razonamiento:**
1. Error de entrenamiento baja; error de validación sube.
2. Causas: pocos datos, modelo complejo, exceso de entrenamiento.
3. Remedios: más datos, regularización, early stopping, dropout.
4. Señal típica: 99 % en train, 60 % en validación.
5. Es un problema de generalización.
**Supuestos:** evaluación con conjunto de validación. **Verificación:** curva de validación en U ✔.

### 057 · ¿Qué es un token en un LLM?
**R:** Unidad de texto procesada por el modelo.
**Razonamiento:**
1. El modelo opera sobre unidades discretas de un vocabulario.
2. Tokenizador (BPE) divide texto en fragmentos frecuentes.
3. “extraordinario” puede partirse en “extra”+“ordinario”.
4. El número de tokens afecta coste y límite de contexto.
5. Explica errores al contar letras o sílabas.
**Supuestos:** modelos basados en transformers. **Verificación:** contar tokens con tokenizador oficial ✔.

### 058 · ¿Qué es un prompt?
**R:** Instrucción o entrada para un modelo.
**Razonamiento:**
1. Condiciona la generación: tarea, formato, tono, restricciones.
2. Mismo modelo, distinto prompt → distinta respuesta.
3. Componentes útiles: rol, tarea, datos, formato, criterios.
4. Un buen prompt mejora el rendimiento.
5. No añade conocimiento que el modelo no tenga.
**Supuestos:** modelos generativos. **Verificación:** comparar respuestas con prompts distintos ✔.

### 059 · ¿Qué es una base de datos relacional?
**R:** Datos organizados en tablas con relaciones.
**Razonamiento:**
1. Tablas con filas (registros) y columnas (atributos).
2. Clave primaria identifica filas; clave foránea referencia otra tabla.
3. Evita duplicación e inconsistencias.
4. Se consulta con SQL (JOIN, WHERE…).
5. Integridad referencial: no hay pedidos de clientes inexistentes.
**Supuestos:** modelo relacional (Codd). **Verificación:** consulta SQL devuelve datos coherentes ✔.

### 060 · ¿Qué significa HTTPS?
**R:** HTTP cifrado mediante TLS.
**Razonamiento:**
1. HTTP viaja en claro por defecto.
2. La “S” indica TLS.
3. TLS aporta confidencialidad, integridad y autenticación del servidor.
4. Usa certificados digitales.
5. No garantiza que el sitio sea legítimo (un fraude también puede tener HTTPS).
**Supuestos:** web moderna. **Verificación:** candado en el navegador ✔.

---

## BLOQUE 7 — Ética, sesgos y pensamiento crítico (061–070)

### 061 · ¿Qué es un sesgo?
**R:** Inclinación injusta o sistemática.
**Razonamiento:**
1. En estadística: desviación sistemática del estimador.
2. En IA/sociedad: trato desigual o distorsión aprendida.
3. Origen: datos históricos, diseño, métricas, uso fuera de contexto.
4. El modelo aprende y puede amplificar desigualdades.
5. Mitigación: auditorías, datos representativos, revisión humana.
**Supuestos:** contexto de IA y estadística. **Verificación:** comparar métricas por subgrupos ✔.

### 062 · ¿Debe una IA admitir cuando no sabe?
**R:** Sí.
**Razonamiento:**
1. Una respuesta inventada es más peligrosa que un “no lo sé”.
2. Un sistema fiable debe calibrar su confianza.
3. Admitir el límite permite pedir más contexto o derivar.
4. Distinguir: no saber, no poder verificar, no estar seguro.
5. La honestidad epistémica aumenta la confianza.
**Supuestos:** uso responsable de IA. **Verificación:** una IA calibrada baja confianza cuando falla ✔.

### 063 · ¿Qué es privacidad?
**R:** Protección de datos personales y control sobre ellos.
**Razonamiento:**
1. Afecta a información que identifica o puede identificar.
2. No es solo ocultar: incluye saber qué se recoge y para qué.
3. La agregación de datos puede revelar información sensible.
4. Principio de minimización: recoger solo lo necesario.
5. Derechos: acceso, rectificación, supresión.
**Supuestos:** protección de datos (RGPD como referencia). **Verificación:** política de privacidad clara ✔.

### 064 · ¿Qué es plagio?
**R:** Usar obra ajena sin atribución adecuada.
**Razonamiento:**
1. No solo copiar texto literal; también parafrasear ideas sin citar.
2. Citar permite verificar y reconocer autoría.
3. Vulnera derechos de autor y distorsiona mérito.
4. El conocimiento común no requiere cita.
5. La frontera depende del contexto y la originalidad.
**Supuestos:** ámbito académico/profesional. **Verificación:** comparar texto con fuentes ✔.

### 065 · ¿Cómo reconocer una fuente fiable?
**R:** Autoría clara, evidencia, actualidad y reputación.
**Razonamiento:**
1. ¿Quién firma? ¿Tiene cualificación?
2. ¿Cita datos, métodos y fuentes primarias?
3. ¿Está actualizada?
4. ¿Hay conflicto de interés declarado?
5. Contrastar con fuentes independientes.
6. Fiabilidad = probabilidad, no garantía.
**Supuestos:** evaluación de información. **Verificación:** corroboración cruzada ✔.

### 066 · ¿Diferencia entre hecho y opinión?
**R:** Hecho verificable; opinión valorativa.
**Razonamiento:**
1. Hecho: comprobable con evidencia intersubjetiva.
2. Opinión: preferencia, valoración o interpretación.
3. Palabras como “mejor”, “debería”, “hermoso” suelen señalar opinión.
4. Hay enunciados mixtos (“el aumento fue excesivo”): separar dato y valoración.
5. Distinguirlos evita discusiones confusas.
**Supuestos:** epistemología básica. **Verificación:** ¿puede comprobarse con evidencia? ✔.

### 067 · ¿Qué es consentimiento?
**R:** Permiso informado y libre.
**Razonamiento:**
1. Libre: sin presión.
2. Informado: sabiendo a qué se consiente.
3. Específico: para un fin concreto.
4. Revocable.
5. El silencio no es consentimiento.
6. Interfaces oscuras no garantizan consentimiento pleno.
**Supuestos:** ética y derecho. **Verificación:** puede retirarse sin consecuencias ✔.

### 068 · ¿Qué es discriminación?
**R:** Trato desigual injusto por características.
**Razonamiento:**
1. No toda diferencia es discriminación (adaptaciones justificadas).
2. Se vuelve discriminatoria cuando el rasgo es irrelevante y produce desventaja.
3. Directa (exclusión explícita) e indirecta (norma neutra que perjudica).
4. En IA puede surgir sin decisión explícita por datos sesgados.
**Supuestos:** marco de derechos. **Verificación:** comparar trato entre grupos ✔.

### 069 · ¿Qué es transparencia?
**R:** Explicar cómo funciona algo y sus límites.
**Razonamiento:**
1. Niveles: datos, modelo, decisiones, limitaciones.
2. Permite auditar, detectar errores y exigir responsabilidad.
3. Transparencia total no siempre posible (privacidad, seguridad).
4. Transparencia proporcionada.
5. Indicador: el sistema puede decir qué no hace bien.
**Supuestos:** gobernanza de sistemas. **Verificación:** documentación accesible ✔.

### 070 · ¿Qué hacer ante un error propio?
**R:** Reconocerlo y corregirlo.
**Razonamiento:**
1. Detectar comparando con evidencia o retroalimentación.
2. Ocultarlo destruye confianza y propaga el fallo.
3. Corregir: dar información correcta y explicar el fallo.
4. Prevenir: identificar el patrón de error.
5. El error corregido es aprendizaje.
**Supuestos:** ética profesional. **Verificación:** la corrección restaura la confianza ✔.

---

## BLOQUE 8 — Economía y finanzas (071–080)

### 071 · ¿Fórmula del interés simple?
**R:** I = P × r × t.
**Razonamiento:**
1. P = capital inicial; r = tasa por periodo en decimal; t = periodos.
2. Se calcula siempre sobre el capital inicial.
3. Ejemplo: 1.000 € al 5 % durante 3 años → 1000·0,05·3 = 150 €.
4. Con interés compuesto el resultado sería mayor.
5. Se usa en préstamos cortos y cálculos didácticos.
**Supuestos:** tasa constante, sin capitalización. **Verificación:** 1000+150=1150 ✔.

### 072 · ¿Qué es inflación?
**R:** Aumento general de precios.
**Razonamiento:**
1. No es subida de un producto, sino del nivel general.
2. Se mide con índices (IPC, deflactor del PIB).
3. Si precios suben más que ingresos, cae el poder adquisitivo.
4. Causas: demanda, costes, expansión monetaria, expectativas.
5. Inflación baja puede ser estable; deflación también problemática.
**Supuestos:** economía de mercado. **Verificación:** variación del IPC ✔.

### 073 · ¿Cuánto ahorro de emergencia?
**R:** Idealmente 3–6 meses de gastos.
**Razonamiento:**
1. Cubrir gastos esenciales si se pierden ingresos.
2. Cálculo: gastos mensuales imprescindibles × meses objetivo.
3. Varía según estabilidad laboral y cargas familiares.
4. Autónomos o ingresos únicos suelen necesitar más.
5. Debe estar líquido y seguro.
**Supuestos:** finanzas personales. **Verificación:** cubre imprevistos sin endeudarse ✔.

### 074 · ¿Qué es diversificar?
**R:** Repartir inversión para reducir riesgo.
**Razonamiento:**
1. El riesgo específico se reduce combinando activos.
2. Funciona mejor con baja correlación.
3. El riesgo sistemático no se elimina diversificando dentro del mismo mercado.
4. Diez acciones tecnológicas no son diversificación real.
5. Diversificar no garantiza ganancias.
**Supuestos:** teoría de carteras. **Verificación:** cartera diversificada tiene menor volatilidad ✔.

### 075 · ¿Por qué evitar deuda de tarjeta cara?
**R:** Sus intereses suelen ser altos.
**Razonamiento:**
1. Si no se paga el total, el saldo genera intereses elevados.
2. Los intereses se suman al capital → efecto bola de nieve.
3. Ejemplo: 1.000 € con tipo alto y pago mínimo cuesta cientos de euros.
4. Alternativa: pagar total o financiación con tipo menor.
5. Es una de las deudas más caras del consumo.
**Supuestos:** tarjeta con interés revolving. **Verificación:** comparar TAE con préstamo personal ✔.

### 076 · ¿Qué es un presupuesto?
**R:** Plan de ingresos y gastos.
**Razonamiento:**
1. Registrar ingresos netos y clasificar gastos (fijos, variables, ocasionales).
2. Restar gastos de ingresos → superávit o déficit.
3. Ajustar partidas y asignar excedente a ahorro o deuda.
4. Requiere seguimiento periódico.
5. Sin revisión, es un documento muerto.
**Supuestos:** finanzas personales o familiares. **Verificación:** cuadra ingresos y gastos ✔.

### 077 · ¿Qué pasa si la demanda supera la oferta?
**R:** Suele subir el precio.
**Razonamiento:**
1. Escasez relativa: más compradores que bienes.
2. Los compradores pujan; vendedores pueden subir precios.
3. El precio alto incentiva producción y desanima demanda.
4. Tiende a un nuevo equilibrio.
5. Excepciones: controles de precios, racionamiento, falta de competencia.
**Supuestos:** mercado competitivo. **Verificación:** curva de oferta y demanda ✔.

### 078 · ¿Qué es interés compuesto?
**R:** Interés sobre capital e intereses acumulados.
**Razonamiento:**
1. Simple: base fija = capital inicial.
2. Compuesto: intereses se reinvierten y forman parte de la base.
3. Fórmula: Cf = P·(1+r)^t.
4. Ejemplo: 1.000 € al 5 % 3 años → ≈1.157,63 € (vs. 1.150 simple).
5. Crecimiento exponencial; el tiempo es el factor clave.
6. También funciona en contra con deudas.
**Supuestos:** reinversión de intereses. **Verificación:** comparar con interés simple ✔.

### 079 · ¿Para qué sirve un seguro?
**R:** Transferir riesgo a una aseguradora.
**Razonamiento:**
1. Muchos pagan prima; la aseguradora cubre a los pocos que sufren siniestro.
2. Se cambia pérdida grande e incierta por pérdida pequeña y segura.
3. Tiene sentido para riesgos de bajo impacto probabilístico y alto coste.
4. Franquicias, exclusiones y límites definen cobertura real.
5. Leer la letra pequeña es esencial.
**Supuestos:** contrato de seguro estándar. **Verificación:** la póliza especifica coberturas ✔.

### 080 · ¿Toda inversión garantiza ganancias?
**R:** No.
**Razonamiento:**
1. Mayor rentabilidad esperada suele implicar mayor riesgo.
2. Los precios dependen de eventos futuros impredecibles.
3. Ningún activo con rentabilidad real está libre de pérdida.
4. Ofertas de “alta rentabilidad garantizada” son sospechosas.
5. Existen productos con capital garantizado, pero rentabilidad baja o condicionada.
**Supuestos:** mercados financieros. **Verificación:** historial de pérdidas en crisis ✔.

---

## BLOQUE 9 — Salud y bienestar (081–090)

### 081 · ¿Por qué lavarse las manos?
**R:** Reduce infecciones.
**Razonamiento:**
1. Las manos tocan superficies contaminadas y luego mucosas.
2. El jabón emulsiona grasas y arrastra microorganismos.
3. El frotado y aclarado los eliminan físicamente.
4. Momentos clave: antes de comer/cocinar, tras baño, tras toser.
5. Es una de las medidas con mayor impacto en salud pública.
**Supuestos:** higiene básica. **Verificación:** reducción de infecciones en estudios ✔.

### 082 · ¿Cómo actúan las vacunas?
**R:** Entrenan al sistema inmune.
**Razonamiento:**
1. Presentan un antígeno sin causar enfermedad completa.
2. El organismo genera anticuerpos y células de memoria.
3. En reexposición, la respuesta es rápida y eficaz.
4. Inmunidad de grupo protege a quienes no pueden vacunarse.
5. Requieren pautas y refuerzos según la vacuna.
**Supuestos:** vacunas autorizadas. **Verificación:** reducción de incidencia de enfermedades ✔.

### 083 · ¿La fiebre siempre es urgencia?
**R:** No; depende de síntomas y contexto.
**Razonamiento:**
1. La fiebre es respuesta inmune regulada.
2. Muchas infecciones leves cursan con fiebre y se resuelven.
3. Señales de alarma: fiebre muy alta persistente, lactantes, dificultad respiratoria, rigidez de nuca, confusión.
4. Importa el estado general más que el número exacto.
5. En inmunodeprimidos, umbral de consulta más bajo.
**Supuestos:** contexto clínico general. **Verificación:** evaluación médica ✔.

### 084 · ¿Beneficio del ejercicio?
**R:** Mejora salud cardiovascular y metabólica.
**Razonamiento:**
1. Fortalece el corazón y mejora circulación.
2. Mejora sensibilidad a la insulina y perfil lipídico.
3. Mantiene masa muscular y densidad ósea.
4. Libera neurotransmisores asociados al bienestar.
5. Mejora el sueño.
6. Beneficio depende de regularidad y adaptación.
**Supuestos:** ejercicio moderado regular. **Verificación:** estudios epidemiológicos ✔.

### 085 · ¿Para qué sirve dormir?
**R:** Consolidar memoria y regular el organismo.
**Razonamiento:**
1. Reactiva y estabiliza aprendizajes del día.
2. Ajusta hormonas, metabolismo, temperatura e inmunidad.
3. Facilita eliminación de desechos metabólicos.
4. La privación causa peor atención, irritabilidad y riesgo metabólico.
5. La cantidad necesaria varía con la edad.
**Supuestos:** sueño fisiológico normal. **Verificación:** estudios de privación de sueño ✔.

### 086 · ¿Hay una cantidad única de agua diaria?
**R:** No; depende de persona, clima y actividad.
**Razonamiento:**
1. Peso, edad, clima, actividad, embarazo o enfermedad cambian necesidades.
2. Los alimentos también aportan agua.
3. La sed y el color de la orina son indicadores prácticos.
4. Beber en exceso puede ser peligroso (hiponatremia).
5. “Más siempre es mejor” es falso.
**Supuestos:** persona sana. **Verificación:** recomendaciones variables por organismo ✔.

### 087 · ¿Los antibióticos curan virus?
**R:** No.
**Razonamiento:**
1. Actúan sobre estructuras bacterianas (pared, ribosomas, ADN).
2. Los virus no tienen esas estructuras ni se replican por sí mismos.
3. Usarlos contra virus no cura y favorece resistencias.
4. Excepción aparente: prevención de sobreinfecciones bacterianas.
5. El uso indebido es amenaza de salud pública.
**Supuestos:** antibióticos convencionales. **Verificación:** guías de uso racional de antibióticos ✔.

### 088 · ¿Qué es una dieta equilibrada?
**R:** Variada y adecuada en nutrientes.
**Razonamiento:**
1. Distintos grupos de alimentos aportan nutrientes diferentes.
2. Debe cubrir necesidades energéticas y de micronutrientes.
3. Importa cantidad y frecuencia, no solo qué se come.
4. Debe ser sostenible en el tiempo.
5. Las dietas extremas rara vez son equilibradas.
**Supuestos:** nutrición humana general. **Verificación:** evaluación nutricional ✔.

### 089 · ¿Por qué usar protector solar?
**R:** Protege de radiación UV.
**Razonamiento:**
1. La radiación UV daña el ADN celular.
2. El daño se acumula con exposiciones, incluso días nublados.
3. Reduce quemaduras, envejecimiento prematuro y riesgo de cáncer de piel.
4. Debe reaplicarse y usarse cantidad suficiente.
5. Combinar con sombra y ropa.
**Supuestos:** exposición solar. **Verificación:** estudios dermatológicos ✔.

### 090 · ¿Qué hacer si hay malestar mental persistente?
**R:** Buscar ayuda profesional.
**Razonamiento:**
1. Malestar persistente que afecta sueño, trabajo o relaciones no es “falta de voluntad”.
2. Un especialista distingue causas y propone tratamiento.
3. Opciones: psicoterapia, fármacos si indicado, o ambos.
4. Si hay ideas de autolesión, urgencia inmediata.
5. Pedir ayuda es una medida responsable.
**Supuestos:** salud mental. **Verificación:** evaluación profesional ✔.

---

## BLOQUE 10 — Información, estadística y aprendizaje (091–100)

### 091 · ¿Cómo verificar una noticia?
**R:** Buscar fuente original y contrastar con otras fiables.
**Razonamiento:**
1. Rastrear origen: muchas noticias falsas citan estudios sin enlace.
2. Comprobar fecha y contexto (contenido reutilizado).
3. Contrastar con medios independientes con historial de rigor.
4. Señales: títulos sensacionalistas, sin autoría, urgencia emocional.
5. En imágenes, búsqueda inversa.
6. Si no se puede verificar, no compartir como cierto.
**Supuestos:** alfabetización mediática. **Verificación:** corroboración en fuentes primarias ✔.

### 092 · ¿Diferencia entre dato e información?
**R:** Dato bruto; información = dato procesado con significado.
**Razonamiento:**
1. Dato aislado (“23”) no comunica.
2. Con contexto (temperatura de una ciudad a una hora) adquiere significado.
3. Información = datos organizados e interpretados.
4. Escalera: datos → información → conocimiento → sabiduría.
5. La interpretación puede introducir sesgo.
**Supuestos:** teoría de la información. **Verificación:** un mismo dato en contextos distintos genera informaciones distintas ✔.

### 093 · ¿Qué es un modelo?
**R:** Representación simplificada de algo.
**Razonamiento:**
1. Ignora detalles para hacer tratable un fenómeno.
2. Propósitos: explicar, predecir, simular.
3. Válido dentro de ciertos supuestos.
4. Fuera de ellos puede fallar sin invalidarse por completo.
5. “El mapa no es el territorio”.
**Supuestos:** epistemología de modelos. **Verificación:** un modelo meteorológico aproxima, no copia, la realidad ✔.

### 094 · ¿Correlación implica causalidad?
**R:** No necesariamente.
**Razonamiento:**
1. Correlación: dos variables varían juntas.
2. Puede haber confusor (tercera variable que causa ambas).
3. Ejemplo: helados y ahogamientos correlacionan por el calor.
4. Para acercarse a causalidad: experimentos, estudios longitudinales, temporalidad, mecanismo.
5. La dirección causal puede ser inversa.
**Supuestos:** estadística inferencial. **Verificación:** estudios controlados ✔.

### 095 · ¿Qué es una muestra representativa?
**R:** Subconjunto que refleja la población.
**Razonamiento:**
1. Objetivo: inferir propiedades sin medir toda la población.
2. Debe parecerse en variables relevantes.
3. Muestreo aleatorio reduce sesgo de selección.
4. Muestra pequeña aumenta incertidumbre.
5. Encuestas solo por internet excluyen a quienes no lo usan.
**Supuestos:** estadística de muestreo. **Verificación:** comparar distribución muestral con poblacional ✔.

### 096 · ¿Diferencia entre media y mediana?
**R:** Media = promedio; mediana = valor central.
**Razonamiento:**
1. Media: suma/n.
2. Mediana: valor central al ordenar (o media de los dos centrales).
3. La media es sensible a extremos; la mediana no.
4. Ejemplo: 1, 2, 3, 4, 100 → media 22, mediana 3.
5. Para ingresos o vivienda, la mediana describe mejor a la mayoría.
**Supuestos:** datos cuantitativos. **Verificación:** calcular ambas en un conjunto con outlier ✔.

### 097 · ¿Cómo se redondea 2,6 al entero?
**R:** 3.
**Razonamiento:**
1. Regla estándar: primera cifra decimal ≥5 → arriba; <5 → abajo.
2. 6 ≥ 5 → se sube.
3. 2,6 → 3.
4. Otros criterios: redondeo bancario, truncamiento.
5. Especificar la regla cuando la precisión importa.
**Supuestos:** redondeo estándar. **Verificación:** 2,6 está más cerca de 3 que de 2 ✔.

### 098 · ¿Unidad de tiempo en el SI?
**R:** Segundo (s).
**Razonamiento:**
1. Es una de las siete unidades base del SI.
2. Definición moderna basada en transición atómica del cesio.
3. Muy precisa y reproducible.
4. Minutos, horas y días no son SI, aunque se aceptan para uso cotidiano.
5. Permite sincronizar ciencia y tecnología.
**Supuestos:** SI. **Verificación:** definición del BIPM ✔.

### 099 · ¿Qué es una API?
**R:** Interfaz para que programas se comuniquen.
**Razonamiento:**
1. Dos programas intercambian datos sin conocer detalles internos.
2. La API define un contrato: peticiones, formato, respuestas.
3. Permite cambiar implementación interna sin romper usuarios.
4. Ejemplo: API meteorológica recibe ciudad y devuelve pronóstico en JSON.
5. No garantiza que los datos sean correctos, solo cómo se solicitan.
**Supuestos:** desarrollo de software. **Verificación:** documentación de la API ✔.

### 100 · ¿Cómo se aprende mejor?
**R:** Con práctica espaciada, ejemplos variados y retroalimentación.
**Razonamiento:**
1. Práctica espaciada: distribuir el estudio mejora retención (efecto del espaciado).
2. Práctica recuperativa: intentar recordar refuerza más que releer.
3. Variedad de ejemplos favorece generalización.
4. Retroalimentación permite corregir el modelo mental.
5. Intercalado mejora discriminación entre tipos de problemas.
6. Límite: un LLM no “estudia”, ajusta parámetros; la analogía es útil, no literal.
**Supuestos:** aprendizaje humano/modelos. **Verificación:** estudios de psicología cognitiva ✔.

# Dataset **Drosophila** — 101–200

---

## BLOQUE 11 — Matemáticas (101–110)

### 101 · ¿Cuánto es 7 × 8?
**R:** 56.
**Razonamiento:**
1. Multiplicación en ℕ: 7 × 8 = 7 sumado 8 veces (o 8 sumado 7 veces).
2. 7+7+7+7+7+7+7+7 = 56.
3. Vía descomposición: 7×8 = 7×(10−2) = 70−14 = 56.
4. Vía memorística de la tabla del 8: 8·7 = 56.
5. Las tres vías coinciden.
**Supuestos:** aritmética decimal. **Verificación:** 56/8 = 7 ✔.

### 102 · ¿Cuál es la raíz cuadrada de 144?
**R:** 12.
**Razonamiento:**
1. √n = x tal que x² = n y x ≥ 0.
2. 12² = 144.
3. Factorización: 144 = 2⁴·3² → √144 = 2²·3 = 12.
4. Solo la raíz principal (positiva) se pide salvo indicación.
5. −12 también cumple (−12)²=144, pero no es la raíz principal.
**Supuestos:** raíz principal en ℝ. **Verificación:** 12² = 144 ✔.

### 103 · ¿Cuánto es 15 % de 200?
**R:** 30.
**Razonamiento:**
1. 15 % = 15/100 = 0,15.
2. 0,15 × 200 = 30.
3. Vía alternativa: 10 % = 20, 5 % = 10, suma = 30.
4. Proporción: 15/100 = x/200 → x = 30.
5. Comprobación inversa: 30/200 = 0,15 ✔.
**Supuestos:** porcentaje simple. **Verificación:** 30/200 = 15 % ✔.

### 104 · ¿Cuál es la solución de 2x + 6 = 14?
**R:** x = 4.
**Razonamiento:**
1. Restar 6 a ambos lados: 2x = 8.
2. Dividir entre 2: x = 4.
3. Verificación: 2·4 + 6 = 14 ✔.
4. Método alternativo: despejar x = (14−6)/2 = 4.
5. Ecuación lineal con solución única.
**Supuestos:** x ∈ ℝ. **Verificación:** sustituir en la ecuación original ✔.

### 105 · ¿Cuál es el área de un círculo de radio 3?
**R:** 9π ≈ 28,27 unidades².
**Razonamiento:**
1. Fórmula: A = πr².
2. A = π·3² = 9π.
3. 9π ≈ 9·3,1416 = 28,27.
4. Unidades al cuadrado (área).
5. No confundir con circunferencia (2πr = 6π).
**Supuestos:** geometría euclidiana. **Verificación:** círculo de r=1 tiene área π ✔.

### 106 · ¿Cuánto suman los ángulos internos de un triángulo?
**R:** 180°.
**Razonamiento:**
1. En geometría euclidiana, la suma es 180°.
2. Demostración: trazar paralela a un lado por el vértice opuesto; los ángulos alternos internos igualan los del triángulo y forman un ángulo llano.
3. En geometría esférica o hiperbólica cambia.
4. Consecuencia: un triángulo no puede tener dos ángulos rectos.
**Supuestos:** geometría euclidiana plana. **Verificación:** triángulo equilátero: 60+60+60=180 ✔.

### 107 · ¿Cuál es la probabilidad de sacar un 6 en un dado justo?
**R:** 1/6.
**Razonamiento:**
1. Ω = {1,2,3,4,5,6}, |Ω| = 6.
2. Dado justo → equiprobabilidad.
3. Casos favorables: {6}, |A| = 1.
4. P = 1/6 ≈ 0,1667 ≈ 16,67 %.
5. Frecuentista: en muchas tiradas la proporción tiende a 1/6.
**Supuestos:** dado justo de 6 caras. **Verificación:** suma de P(1..6) = 1 ✔.

### 108 · ¿Cuánto es 2³?
**R:** 8.
**Razonamiento:**
1. Potencia: 2³ = 2·2·2.
2. 2·2 = 4; 4·2 = 8.
3. Interpretación: volumen de un cubo de lado 2.
4. Distinto de 2·3 = 6.
5. Exponente 3 = número de factores.
**Supuestos:** exponente natural. **Verificación:** log₂(8) = 3 ✔.

### 109 · ¿Cuál es el perímetro de un cuadrado de lado 5?
**R:** 20.
**Razonamiento:**
1. Cuadrado: 4 lados iguales.
2. Perímetro = 4·lado = 4·5 = 20.
3. Unidades lineales, no cuadradas.
4. Área sería 5² = 25.
5. No confundir perímetro con área.
**Supuestos:** geometría plana. **Verificación:** 5+5+5+5 = 20 ✔.

### 110 · ¿Cuál es el mcm de 4 y 6?
**R:** 12.
**Razonamiento:**
1. mcm = menor entero positivo múltiplo de ambos.
2. Múltiplos de 4: 4, 8, 12, 16…
3. Múltiplos de 6: 6, 12, 18…
4. Primer común: 12.
5. Vía factorización: 4 = 2², 6 = 2·3 → mcm = 2²·3 = 12.
**Supuestos:** ℕ. **Verificación:** 12/4 = 3 y 12/6 = 2 ✔.

---

## BLOQUE 12 — Física y química (111–120)

### 111 · ¿Qué es la energía?
**R:** Capacidad de realizar trabajo o producir cambios.
**Razonamiento:**
1. Se manifiesta en formas: cinética, potencial, térmica, química, nuclear, eléctrica.
2. Se conserva: la energía total de un sistema aislado permanece constante.
3. Puede transformarse entre formas, no crearse ni destruirse.
4. Unidad SI: julio (J).
5. En relatividad, masa y energía se relacionan (E = mc²).
**Supuestos:** física clásica y moderna. **Verificación:** péndulo transforma potencial ↔ cinética ✔.

### 112 · ¿Qué dice la primera ley de Newton?
**R:** Un cuerpo sin fuerza neta mantiene su estado de reposo o movimiento rectilíneo uniforme.
**Razonamiento:**
1. También llamada ley de inercia.
2. Fuerza neta cero → velocidad constante.
3. Explica por qué necesitamos cinturón en un frenazo.
4. No dice que todo lo que se mueve se detenga: sin rozamiento seguiría.
5. Base de la mecánica clásica.
**Supuestos:** marcos inerciales. **Verificación:** disco sobre hielo se desliza largo ✔.

### 113 · ¿Qué es un átomo?
**R:** Unidad básica de la materia formada por núcleo y electrones.
**Razonamiento:**
1. Núcleo: protones (+) y neutrones (neutros).
2. Electrones (−) orbitan en niveles de energía.
3. Número atómico (Z) = protones → define el elemento.
4. Isótopos: mismo Z, distinto número de neutrones.
5. Se combinan formando moléculas y compuestos.
**Supuestos:** modelo cuántico moderno. **Verificación:** tabla periódica organiza por Z ✔.

### 114 · ¿Qué es el pH?
**R:** Medida de acidez o basicidad de una disolución.
**Razonamiento:**
1. pH = −log[H⁺].
2. Escala típica 0–14 a 25 °C.
3. pH < 7 ácido; pH = 7 neutro; pH > 7 básico.
4. Cada unidad de pH es un factor 10 en concentración de H⁺.
5. Ejemplos: limón ≈2, agua pura =7, lejía ≈13.
**Supuestos:** disolución acuosa a 25 °C. **Verificación:** agua pura pH 7 ✔.

### 115 · ¿Qué es la electricidad?
**R:** Fenómeno asociado al movimiento o acumulación de cargas eléctricas.
**Razonamiento:**
1. Cargas positivas y negativas; iguales se repelen, opuestas se atraen.
2. Corriente = flujo de electrones en un conductor.
3. Unidad de carga: culombio (C); de corriente: amperio (A).
4. Ley de Ohm: V = IR.
5. Se genera por inducción, reacción química o fricción.
**Supuestos:** electrodinámica clásica. **Verificación:** circuito con batería y bombilla enciende ✔.

### 116 · ¿Qué es la densidad?
**R:** Masa por unidad de volumen.
**Razonamiento:**
1. ρ = m/V.
2. Unidad SI: kg/m³ (también g/cm³).
3. Agua ≈ 1 g/cm³.
4. Determina si un cuerpo flota (densidad menor que el fluido).
5. Depende de temperatura y presión.
**Supuestos:** sustancia homogénea. **Verificación:** 1 kg de agua ocupa ~1 L → ρ ≈ 1 kg/L ✔.

### 117 · ¿Qué es una reacción química?
**R:** Transformación en la que se rompen y forman enlaces entre átomos.
**Razonamiento:**
1. Reactivos → productos.
2. Se conservan los átomos (ley de conservación de la masa).
3. Cambian las sustancias, no los elementos.
4. Puede liberar (exotérmica) o absorber (endotérmica) energía.
5. Se representa con ecuaciones químicas ajustadas.
**Supuestos:** química clásica. **Verificación:** combustión de metano: CH₄+2O₂→CO₂+2H₂O ✔.

### 118 · ¿Qué es la temperatura?
**R:** Medida de la energía cinética media de las partículas.
**Razonamiento:**
1. Más temperatura → más agitación molecular.
2. Unidad SI: kelvin (K); también °C.
3. T(K) = T(°C) + 273,15.
4. No es lo mismo que calor: calor es transferencia de energía.
5. Cero absoluto: 0 K = −273,15 °C (no alcanzable).
**Supuestos:** termodinámica. **Verificación:** agua hierve a 100 °C = 373,15 K ✔.

### 119 · ¿Qué es un imán?
**R:** Objeto que genera campo magnético y atrae materiales ferromagnéticos.
**Razonamiento:**
1. Tiene polos norte y sur; polos iguales se repelen, opuestos se atraen.
2. No se puede aislar un polo magnético (a diferencia de la carga eléctrica).
3. Campo magnético descrito por líneas de fuerza.
4. Materiales ferromagnéticos: hierro, cobalto, níquel.
5. Origen microscópico: alineación de espines atómicos.
**Supuestos:** magnetismo clásico. **Verificación:** brújula apunta al norte terrestre ✔.

### 120 · ¿Qué es el sonido?
**R:** Onda mecánica longitudinal que se propaga en un medio.
**Razonamiento:**
1. Necesita medio material (no se propaga en vacío).
2. Frecuencia determina tono; amplitud, volumen.
3. Velocidad: ~343 m/s en aire a 20 °C; mayor en agua y sólidos.
4. Espectro audible humano: 20 Hz – 20 kHz.
5. Es una onda de presión.
**Supuestos:** acústica clásica. **Verificación:** sin aire no hay sonido (campana de vacío) ✔.

---

## BLOQUE 13 — Biología y cuerpo humano (121–130)

### 121 · ¿Cuántos huesos tiene el cuerpo humano adulto?
**R:** 206.
**Razonamiento:**
1. El adulto tiene 206 huesos.
2. El recién nacido tiene ~270; algunos se fusionan con el crecimiento.
3. Se dividen en esqueleto axial (~80) y apendicular (~126).
4. El fémur es el más largo; el estribo, el más pequeño.
5. Variaciones anatómicas pueden alterar el número.
**Supuestos:** adulto estándar. **Verificación:** anatomía descriptiva ✔.

### 122 · ¿Qué hace el corazón?
**R:** Bombea sangre por el sistema circulatorio.
**Razonamiento:**
1. Cuatro cámaras: dos aurículas y dos ventrículos.
2. Lado derecho → pulmones; izquierdo → resto del cuerpo.
3. Late ~60–100 veces por minuto en reposo.
4. Transporta oxígeno, nutrientes y desechos.
5. Su actividad se regula por el sistema nervioso autónomo.
**Supuestos:** anatomía humana. **Verificación:** auscultación cardíaca ✔.

### 123 · ¿Qué es la sangre?
**R:** Tejido líquido que transporta sustancias por el cuerpo.
**Razonamiento:**
1. Componentes: plasma, glóbulos rojos, glóbulos blancos, plaquetas.
2. Glóbulos rojos transportan O₂ mediante hemoglobina.
3. Glóbulos blancos participan en defensa inmune.
4. Plaquetas intervienen en coagulación.
5. Volumen ≈ 5 L en adulto.
**Supuestos:** fisiología humana. **Verificación:** análisis de sangre ✔.

### 124 · ¿Qué es la respiración celular?
**R:** Proceso que obtiene energía de la glucosa usando oxígeno.
**Razonamiento:**
1. Ecuación global: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + energía (ATP).
2. Ocurre en mitocondrias.
3. Fases: glucólisis, ciclo de Krebs, cadena respiratoria.
4. Produce ATP, moneda energética celular.
5. La respiración anaerobia (fermentación) produce menos ATP.
**Supuestos:** células eucariotas. **Verificación:** sin O₂ se activa fermentación ✔.

### 125 · ¿Qué es el sistema inmune?
**R:** Conjunto de defensas contra patógenos.
**Razonamiento:**
1. Innato: barreras (piel, mucosas) y células rápidas.
2. Adaptativo: linfocitos B (anticuerpos) y T (células).
3. Memoria inmunológica: respuesta más rápida en segundo contacto.
4. Base de las vacunas.
5. Fallos causan alergias o autoinmunidad.
**Supuestos:** inmunología estándar. **Verificación:** respuesta a infección ✔.

### 126 · ¿Qué es la evolución?
**R:** Cambio de las poblaciones a lo largo de generaciones.
**Razonamiento:**
1. Mecanismos: selección natural, mutación, deriva génica, migración.
2. Variabilidad + herencia + selección → adaptación.
3. No ocurre en un individuo, sino en poblaciones.
4. Evidencias: fósiles, ADN, biogeografía, observación directa.
5. Explica la diversidad biológica.
**Supuestos:** biología evolutiva moderna. **Verificación:** resistencia a antibióticos en bacterias ✔.

### 127 · ¿Qué es un ecosistema?
**R:** Sistema formado por seres vivos y su ambiente físico.
**Razonamiento:**
1. Componentes bióticos (seres vivos) y abióticos (agua, suelo, clima).
2. Interacciones: depredación, competencia, simbiosis.
3. Flujo de energía y ciclos de materia.
4. Puede ser terrestre o acuático.
5. Su equilibrio es dinámico, no estático.
**Supuestos:** ecología. **Verificación:** cadena trófica en un bosque ✔.

### 128 · ¿Qué es la mitocondria?
**R:** Orgánulo celular que produce energía (ATP).
**Razonamiento:**
1. Tiene doble membrana.
2. Realiza respiración celular aerobia.
3. Contiene su propio ADN (origen endosimbiótico).
4. Abundante en células con alta demanda energética (músculo).
5. Su disfunción causa enfermedades mitocondriales.
**Supuestos:** célula eucariota. **Verificación:** tinción mitocondrial ✔.

### 129 · ¿Qué es la homeostasis?
**R:** Mantenimiento del equilibrio interno del organismo.
**Razonamiento:**
1. Regula temperatura, pH, glucosa, agua, electrolitos.
2. Mecanismos de retroalimentación negativa (la mayoría) y positiva (menos frecuente).
3. Ejemplo: sudoración para bajar temperatura.
4. Su fallo causa enfermedad.
5. Es una propiedad clave de los seres vivos.
**Supuestos:** fisiología. **Verificación:** temperatura corporal ≈ 37 °C ✔.

### 130 · ¿Qué es un gen?
**R:** Fragmento de ADN que contiene información para un producto funcional.
**Razonamiento:**
1. Puede codificar proteína o ARN funcional.
2. Se hereda de progenitores.
3. Alelos: variantes de un mismo gen.
4. La expresión génica depende del ambiente y la regulación.
5. Mutaciones pueden alterar su función.
**Supuestos:** genética moderna. **Verificación:** secuenciación génica ✔.

---

## BLOQUE 14 — Historia y cultura (131–140)

### 131 · ¿En qué año llegó el ser humano a la Luna?
**R:** 1969.
**Razonamiento:**
1. Misión Apolo 11, julio de 1969.
2. Neil Armstrong y Buzz Aldrin caminaron sobre la Luna.
3. Michael Collins orbitaba en el módulo de mando.
4. Hito de la carrera espacial EE. UU.–URSS.
5. Se ha repetido en misiones posteriores (Apolo 12–17).
**Supuestos:** programa Apolo. **Verificación:** registros NASA ✔.

### 132 · ¿Quién fue Cleopatra?
**R:** Última reina del Egipto ptolemaico.
**Razonamiento:**
1. Reinó entre 51 y 30 a. C.
2. Relacionada con Julio César y Marco Antonio.
3. Su derrota y suicidio marcaron el fin de Egipto como reino independiente.
4. Egipto pasó a ser provincia romana.
5. Figura histórica y cultural muy representada.
**Supuestos:** historia antigua. **Verificación:** fuentes romanas y egipcias ✔.

### 133 · ¿Qué fue el Imperio romano?
**R:** Sistema político que dominó el Mediterráneo durante siglos.
**Razonamiento:**
1. Comienza con Augusto (27 a. C.) tras la República.
2. Máxima extensión bajo Trajano (s. II d. C.).
3. Divide en Imperio de Occidente y Oriente en 395.
4. Occidente cae en 476; Oriente (bizantino) hasta 1453.
5. Legado: derecho, lengua, infraestructura, cristianismo.
**Supuestos:** historiografía estándar. **Verificación:** fuentes históricas ✔.

### 134 · ¿Qué fue la Ilustración?
**R:** Movimiento intelectual del s. XVIII que defendió la razón y la ciencia.
**Razonamiento:**
1. Centro: Francia, con figuras como Voltaire, Rousseau, Diderot.
2. Valores: razón, libertad, igualdad, progreso, tolerancia.
3. Influyó en la Revolución Francesa y la independencia de EE. UU.
4. Promovió la Enciclopedia como difusión del conocimiento.
5. Criticó el absolutismo y los privilegios estamentales.
**Supuestos:** historia moderna. **Verificación:** obras de la época ✔.

### 135 · ¿Qué es el Renacimiento?
**R:** Movimiento cultural europeo (s. XIV–XVI) de recuperación de la Antigüedad clásica.
**Razonamiento:**
1. Origen en Italia (Florencia).
2. Humanismo: centralidad del ser humano.
3. Desarrollo de perspectiva, anatomía, imprenta.
4. Figuras: Da Vinci, Miguel Ángel, Erasmo.
5. Transición entre Edad Media y Edad Moderna.
**Supuestos:** periodización histórica. **Verificación:** obras artísticas y textos ✔.

### 136 · ¿Quién escribió el Quijote?
**R:** Miguel de Cervantes.
**Razonamiento:**
1. Publicado en dos partes: 1605 y 1615.
2. Considerado la primera novela moderna.
3. Protagonistas: Don Quijote y Sancho Panza.
4. Obra cumbre de la literatura española.
5. Cervantes murió en 1616.
**Supuestos:** literatura española. **Verificación:** ediciones originales ✔.

### 137 · ¿Qué fue la Segunda Guerra Mundial?
**R:** Conflicto global (1939–1945) entre Aliados y Potencias del Eje.
**Razonamiento:**
1. Comienza con invasión de Polonia por Alemania (1939).
2. Eje: Alemania, Italia, Japón; Aliados: Reino Unido, URSS, EE. UU., China, Francia.
3. Holocausto: genocidio sistemático.
4. Termina en 1945 con rendición de Alemania y Japón.
5. Consecuencias: ONU, Guerra Fría, descolonización.
**Supuestos:** historia contemporánea. **Verificación:** fuentes históricas ✔.

### 138 · ¿Qué fue la Guerra Fría?
**R:** Tensión geopolítica entre EE. UU. y la URSS (1947–1991).
**Razonamiento:**
1. No fue confrontación militar directa entre las potencias.
2. Conflictos indirectos: Corea, Vietnam, Afganistán.
3. Carrera nuclear y espacial.
4. Bloques: OTAN vs. Pacto de Varsovia.
5. Termina con la disolución de la URSS (1991).
**Supuestos:** historia del s. XX. **Verificación:** archivos desclasificados ✔.

### 139 · ¿Qué fue la Revolución Industrial?
**R:** Transformación económica y social iniciada en el s. XVIII en Reino Unido.
**Razonamiento:**
1. Máquina de vapor, ferrocarril, fábricas.
2. Paso de economía agraria a industrial.
3. Urbanización masiva.
4. Nuevas clases sociales: burguesía industrial y proletariado.
5. Se extendió a Europa y América.
**Supuestos:** historia económica. **Verificación:** registros industriales ✔.

### 140 · ¿Qué es la ONU?
**R:** Organización internacional fundada en 1945.
**Razonamiento:**
1. Objetivo: mantener paz y seguridad internacional.
2. Sede: Nueva York.
3. Órganos: Asamblea General, Consejo de Seguridad, etc.
4. 193 Estados miembros.
5. Agencias: UNESCO, UNICEF, OMS.
**Supuestos:** organismos internacionales. **Verificación:** carta fundacional ✔.

---

## BLOQUE 15 — Geografía (141–150)

### 141 · ¿Cuál es el país más grande del mundo?
**R:** Rusia.
**Razonamiento:**
1. Superficie ≈ 17 millones km².
2. Abarca Europa del Este y Asia del Norte.
3. Once husos horarios.
4. Más del doble que Canadá (segundo).
5. Se extiende hasta el Ártico y el Pacífico.
**Supuestos:** superficie terrestre total. **Verificación:** datos geográficos ✔.

### 142 · ¿Cuál es el desierto más grande del mundo?
**R:** El Antártico (desierto polar).
**Razonamiento:**
1. “Desierto” = región con precipitación muy baja, no necesariamente cálida.
2. La Antártida es el mayor desierto (≈14 millones km²).
3. El Sahara es el mayor desierto cálido (≈9 millones km²).
4. La respuesta depende de la definición.
5. Se aclara si se pregunta por desierto cálido o por desierto en general.
**Supuestos:** definición climática. **Verificación:** datos de precipitación ✔.

### 143 · ¿Cuál es el río más caudaloso del mundo?
**R:** El Amazonas.
**Razonamiento:**
1. Caudal medio ≈ 209.000 m³/s.
2. Supera al Nilo, Yangtsé y Misisipi.
3. Su cuenca es la mayor del mundo.
4. Desemboca en el Atlántico.
5. Caudal ≠ longitud (el más largo es discutido).
**Supuestos:** caudal medio. **Verificación:** datos hidrológicos ✔.

### 144 · ¿Cuál es la montaña más alta del mundo?
**R:** El Everest.
**Razonamiento:**
1. Altitud: 8.848,86 m sobre el nivel del mar.
2. Cordillera del Himalaya, frontera Nepal–China.
3. Escalado por primera vez en 1953 (Hillary y Tenzing).
4. Si se mide desde la base oceánica, el Mauna Kea es más alto.
5. “Más alta” = mayor altitud sobre nivel del mar.
**Supuestos:** altitud sobre nivel del mar. **Verificación:** mediciones geodésicas ✔.

### 145 · ¿Cuántos continentes hay?
**R:** Depende del modelo: 5, 6 o 7.
**Razonamiento:**
1. Modelo de 7: África, Antártida, Asia, Europa, América del Norte, América del Sur, Oceanía.
2. Modelo de 6: América unificada.
3. Modelo de 5: Eurasia unificada, América unificada, Antártida, África, Oceanía.
4. No hay una respuesta universal: depende del país y la tradición educativa.
5. En España se enseña tradicionalmente 6 (con América unificada) o 5.
**Supuestos:** convención geográfica. **Verificación:** manuales escolares de distintos países ✔.

### 146 · ¿Cuál es el océano más pequeño?
**R:** El Ártico.
**Razonamiento:**
1. Superficie ≈ 14 millones km².
2. Rodeado por Eurasia y América del Norte.
3. Cubierto de hielo marino parte del año.
4. El Antártico también es pequeño, pero el Ártico es menor.
5. Se distingue de los demás por su ubicación polar.
**Supuestos:** delimitación estándar. **Verificación:** datos NOAA ✔.

### 147 · ¿Cuál es la capital de Australia?
**R:** Canberra.
**Razonamiento:**
1. Capital federal, sede del gobierno.
2. No es Sídney ni Melbourne (las más conocidas).
3. Se fundó como capital de compromiso entre ambas ciudades.
4. Diseñada por Walter Burley Griffin.
5. Dato institucional verificable.
**Supuestos:** Australia contemporánea. **Verificación:** gobierno australiano ✔.

### 148 · ¿Dónde está el Amazonas?
**R:** América del Sur.
**Razonamiento:**
1. Nace en los Andes peruanos.
2. Atraviesa Perú, Colombia y Brasil.
3. Desemboca en el Atlántico.
4. Cuenca ≈ 7 millones km².
5. Es el río más caudaloso del mundo.
**Supuestos:** geografía física. **Verificación:** mapas ✔.

### 149 · ¿Cuál es el país más poblado del mundo?
**R:** India (desde 2023).
**Razonamiento:**
1. En 2023 India superó a China en población.
2. India ≈ 1.430 millones; China ≈ 1.410 millones.
3. China tuvo políticas de control de natalidad; India tiene población más joven.
4. Dato cambiante con el tiempo.
5. Se debe especificar la fecha.
**Supuestos:** datos recientes. **Verificación:** ONU, Banco Mundial ✔.

### 150 · ¿Qué es la Unión Europea?
**R:** Organización política y económica de países europeos.
**Razonamiento:**
1. Origen: Tratado de Roma (1957).
2. 27 Estados miembros tras el Brexit.
3. Mercado único, libre circulación.
4. Instituciones: Comisión, Parlamento, Consejo.
5. Moneda común: euro en la eurozona.
**Supuestos:** integración europea. **Verificación:** tratados oficiales ✔.

---

## BLOQUE 16 — Lengua y literatura (151–160)

### 151 · ¿Qué es un sustantivo?
**R:** Palabra que nombra personas, cosas, lugares o ideas.
**Razonamiento:**
1. Categoría gramatical con género y número.
2. Puede ser propio o común, concreto o abstracto.
3. Funciona como núcleo del sintagma nominal.
4. Ejemplos: “perro”, “Madrid”, “libertad”.
5. Se combina con artículos y adjetivos.
**Supuestos:** gramática española. **Verificación:** “el perro” funciona ✔.

### 152 · ¿Qué es un verbo?
**R:** Palabra que expresa acción, estado o proceso.
**Razonamiento:**
1. Categoría con conjugación (tiempo, modo, persona, número, aspecto).
2. Formas: simples y compuestas.
3. Puede ser regular o irregular.
4. Núcleo del predicado.
5. Ejemplos: “correr”, “ser”, “llover”.
**Supuestos:** gramática tradicional. **Verificación:** “yo corro” funciona ✔.

### 153 · ¿Qué es un adjetivo?
**R:** Palabra que califica o determina al sustantivo.
**Razonamiento:**
1. Concuerda en género y número con el sustantivo.
2. Puede ser calificativo o determinativo.
3. Ejemplos: “alto”, “este”, “tres”.
4. Puede sustantivarse (“el rico”).
5. Aporta información sobre el sustantivo.
**Supuestos:** gramática española. **Verificación:** “niño alto” concuerda ✔.

### 154 · ¿Qué es un texto narrativo?
**R:** Texto que cuenta una historia con personajes, tiempo y espacio.
**Razonamiento:**
1. Elementos: narrador, personajes, trama, ambiente.
2. Estructura: planteamiento, nudo, desenlace.
3. Puede ser literario o no.
4. Ejemplos: cuento, novela, fábula.
5. Predomina la secuencia temporal.
**Supuestos:** teoría literaria. **Verificación:** análisis de cuentos ✔.

### 155 · ¿Qué es una rima?
**R:** Coincidencia de sonidos al final de los versos.
**Razonamiento:**
1. Consonante: coinciden vocales y consonantes desde la última tónica.
2. Asonante: solo coinciden las vocales.
3. Puede ser regular o irregular.
4. Contribuye al ritmo y musicalidad.
5. Típica en poesía, canciones y refranes.
**Supuestos:** métrica española. **Verificación:** “amor”/“corazón” rima asonante ✔.

### 156 · ¿Qué es una fábula?
**R:** Relato breve con moraleja, a menudo con animales personificados.
**Razonamiento:**
1. Personajes suelen ser animales con rasgos humanos.
2. Termina con una enseñanza (moraleja).
3. Autores clásicos: Esopo, La Fontaine, Samaniego.
4. Se transmite oralmente o por escrito.
5. Género didáctico.
**Supuestos:** literatura universal. **Verificación:** “La liebre y la tortuga” ✔.

### 157 · ¿Qué es un mito?
**R:** Relato tradicional que explica el origen del mundo o fenómenos naturales.
**Razonamiento:**
1. Protagonistas: dioses, héroes, seres sobrenaturales.
2. Función: explicar, legitimar, transmitir valores.
3. Se transmite oralmente y luego por escrito.
4. Ejemplo: mito de Prometeo.
5. Diferente de leyenda (más histórica) y cuento (más lúdico).
**Supuestos:** antropología y literatura. **Verificación:** mitología griega ✔.

### 158 · ¿Qué es una oración?
**R:** Unidad gramatical con sujeto y predicado que expresa un sentido completo.
**Razonamiento:**
1. Sujeto + predicado como estructura prototípica.
2. Puede ser simple o compuesta.
3. Entonación y puntuación la delimitan.
4. Puede ser enunciativa, interrogativa, exclamativa, etc.
5. Tiene sentido completo en el contexto.
**Supuestos:** gramática tradicional. **Verificación:** “El niño come” es oración ✔.

### 159 · ¿Qué es un sinónimo?
**R:** Palabra con significado igual o muy similar a otra.
**Razonamiento:**
1. No son intercambiables en todos los contextos.
2. Ejemplos: “casa”/“hogar”, “rápido”/“veloz”.
3. Grado de sinonimia: total o parcial.
4. Pueden variar en registro o connotación.
5. Importante para la expresión escrita.
**Supuestos:** semántica. **Verificación:** “coche”/“automóvil” ✔.

### 160 · ¿Qué es un diptongo?
**R:** Unión de dos vocales en una misma sílaba.
**Razonamiento:**
1. Combinaciones: vocal abierta + cerrada, cerrada + abierta, cerrada + cerrada.
2. Ejemplos: “aire”, “ciudad”, “cuidado”.
3. Puede ser creciente o decreciente.
4. Distinto de hiato (vocales en sílabas distintas).
5. Afecta a la acentuación.
**Supuestos:** fonética española. **Verificación:** “bue-no” tiene diptongo ✔.

---

## BLOQUE 17 — Tecnología y programación (161–170)

### 161 · ¿Qué es un lenguaje de programación?
**R:** Sistema formal para expresar instrucciones a una computadora.
**Razonamiento:**
1. Tiene sintaxis y semántica definidas.
2. Puede ser compilado o interpretado.
3. Ejemplos: Python, Java, C, JavaScript.
4. Permite automatizar tareas y crear software.
5. Cada lenguaje tiene paradigmas y usos propios.
**Supuestos:** informática. **Verificación:** compilar un programa sencillo ✔.

### 162 · ¿Qué es una función en programación?
**R:** Bloque de código reutilizable que realiza una tarea.
**Razonamiento:**
1. Puede recibir parámetros y devolver un valor.
2. Evita duplicar código.
3. Facilita el mantenimiento y la legibilidad.
4. Puede ser pura (sin efectos secundarios) o no.
5. Ejemplo: “sumar(a, b)”.
**Supuestos:** programación estructurada. **Verificación:** llamar a la función devuelve resultado ✔.

### 163 · ¿Qué es un array o lista?
**R:** Estructura que almacena varios elementos en orden.
**Razonamiento:**
1. Acceso por índice (a menudo desde 0).
2. Puede contener elementos de un mismo tipo o mixtos según el lenguaje.
3. Operaciones: añadir, eliminar, recorrer.
4. Longitud variable o fija según implementación.
5. Base de muchas estructuras más complejas.
**Supuestos:** programación. **Verificación:** lista[0] devuelve primer elemento ✔.

### 164 · ¿Qué es un condicional?
**R:** Estructura que ejecuta código según se cumpla una condición.
**Razonamiento:**
1. Formas: if, else if, else.
2. Evalúa una expresión booleana.
3. Permite ramificar la ejecución.
4. Base de la lógica de control.
5. Puede anidarse.
**Supuestos:** programación. **Verificación:** if (x>0) ejecuta bloque ✔.

### 165 · ¿Qué es una base de datos?
**R:** Conjunto organizado de datos almacenados y accesibles.
**Razonamiento:**
1. Puede ser relacional o no relacional.
2. Permite consultar, insertar, actualizar y eliminar datos.
3. Garantiza integridad y seguridad.
4. Ejemplos: MySQL, PostgreSQL, MongoDB.
5. Base de aplicaciones modernas.
**Supuestos:** informática. **Verificación:** consulta SQL devuelve datos ✔.

### 166 · ¿Qué es la nube (cloud)?
**R:** Servicios informáticos ofrecidos a través de internet.
**Razonamiento:**
1. Incluye almacenamiento, cómputo, bases de datos, IA.
2. Modelos: IaaS, PaaS, SaaS.
3. Ventajas: escalabilidad, pago por uso.
4. Riesgos: dependencia, privacidad, seguridad.
5. Ejemplos: AWS, Azure, Google Cloud.
**Supuestos:** computación moderna. **Verificación:** subir archivo a la nube ✔.

### 167 · ¿Qué es un sistema operativo?
**R:** Software que gestiona hardware y recursos del ordenador.
**Razonamiento:**
1. Intermediario entre usuario y hardware.
2. Funciones: gestión de procesos, memoria, archivos, dispositivos.
3. Ejemplos: Windows, Linux, macOS, Android.
4. Puede ser de escritorio, móvil o servidor.
5. Base para ejecutar aplicaciones.
**Supuestos:** informática. **Verificación:** arrancar un ordenador ✔.

### 168 · ¿Qué es una IP?
**R:** Dirección numérica que identifica un dispositivo en una red.
**Razonamiento:**
1. IPv4: 32 bits (ej. 192.168.1.1).
2. IPv6: 128 bits (mayor espacio).
3. Puede ser pública o privada.
4. Permite enrutar paquetes.
5. Puede ser dinámica o estática.
**Supuestos:** redes. **Verificación:** ping a una IP ✔.

### 169 · ¿Qué es un compilador?
**R:** Programa que traduce código fuente a código máquina.
**Razonamiento:**
1. Analiza sintaxis y semántica.
2. Genera código ejecutable.
3. Distinto de intérprete (ejecuta línea a línea).
4. Ejemplos: gcc, javac.
5. Detecta errores antes de ejecutar.
**Supuestos:** informática. **Verificación:** compilar programa C ✔.

### 170 · ¿Qué es un algoritmo de ordenación?
**R:** Procedimiento para ordenar elementos de una colección.
**Razonamiento:**
1. Ejemplos: burbuja, quicksort, mergesort.
2. Complejidad variable: O(n²) u O(n log n).
3. Se elige según tamaño y estabilidad requerida.
4. Fundamental en informática.
5. Puede ser estable o inestable.
**Supuestos:** algoritmia. **Verificación:** [3,1,2] ordenado a [1,2,3] ✔.

---

## BLOQUE 18 — Economía y empresa (171–180)

### 171 · ¿Qué es el PIB?
**R:** Valor total de bienes y servicios producidos en un país en un periodo.
**Razonamiento:**
1. Mide actividad económica.
2. Puede ser nominal o real (ajustado por inflación).
3. No mide bienestar ni distribución.
4. Se calcula por producción, gasto o renta.
5. Comparación entre países requiere ajustes (PPA).
**Supuestos:** macroeconomía. **Verificación:** datos de institutos estadísticos ✔.

### 172 · ¿Qué es la oferta y la demanda?
**R:** Modelo económico que explica precios y cantidades.
**Razonamiento:**
1. Demanda: cantidad que compradores quieren a cada precio.
2. Oferta: cantidad que vendedores ofrecen a cada precio.
3. Equilibrio: oferta = demanda.
4. Exceso de demanda → sube precio; exceso de oferta → baja.
5. Base de la economía de mercado.
**Supuestos:** mercado competitivo. **Verificación:** gráfico oferta-demanda ✔.

### 173 · ¿Qué es un monopolio?
**R:** Mercado con un único oferente.
**Razonamiento:**
1. El monopolista controla el precio.
2. Barreras de entrada altas.
3. Puede reducir cantidad y subir precio.
4. Regulación frecuente por parte del Estado.
5. Distinto de oligopolio (pocos oferentes).
**Supuestos:** microeconomía. **Verificación:** casos históricos (telecomunicaciones) ✔.

### 174 · ¿Qué es una acción?
**R:** Participación en la propiedad de una empresa.
**Razonamiento:**
1. Otorga derechos económicos y políticos.
2. Se negocia en bolsa.
3. Su precio varía según oferta y demanda.
4. Puede pagar dividendos.
5. Riesgo: el valor puede caer.
**Supuestos:** mercado de valores. **Verificación:** cotización bursátil ✔.

### 175 · ¿Qué es un bono?
**R:** Título de deuda emitido por un gobierno o empresa.
**Razonamiento:**
1. El inversor presta dinero a cambio de intereses.
2. Riesgo depende del emisor.
3. Puede ser a corto o largo plazo.
4. Menor riesgo que acciones (en general).
5. Puede venderse antes del vencimiento.
**Supuestos:** finanzas. **Verificación:** pago de cupones ✔.

### 176 · ¿Qué es el IVA?
**R:** Impuesto sobre el valor añadido.
**Razonamiento:**
1. Impuesto indirecto sobre el consumo.
2. Se aplica en cada fase de la cadena productiva.
3. Lo paga el consumidor final.
4. Tipos variables según el país y el producto.
5. En España: general 21 %, reducido 10 %, superreducido 4 %.
**Supuestos:** fiscalidad. **Verificación:** factura con IVA ✔.

### 177 · ¿Qué es una startup?
**R:** Empresa emergente con modelo de negocio escalable.
**Razonamiento:**
1. Busca crecimiento rápido.
2. Suele operar en tecnología o innovación.
3. Alta incertidumbre y riesgo.
4. Financiación: capital riesgo, business angels.
5. Puede fracasar o escalar rápidamente.
**Supuestos:** emprendimiento. **Verificación:** casos como Airbnb o Spotify ✔.

### 178 · ¿Qué es el marketing?
**R:** Conjunto de actividades para promover y vender productos.
**Razonamiento:**
1. Incluye investigación de mercado, producto, precio, distribución, promoción (4P).
2. Busca satisfacer necesidades del cliente.
3. Puede ser digital o tradicional.
4. Se apoya en datos y segmentación.
5. Ética: evitar publicidad engañosa.
**Supuestos:** empresa. **Verificación:** campaña publicitaria ✔.

### 179 · ¿Qué es un balance?
**R:** Estado financiero que muestra activo, pasivo y patrimonio neto.
**Razonamiento:**
1. Activo = bienes y derechos.
2. Pasivo = obligaciones.
3. Patrimonio neto = activo − pasivo.
4. Refleja la situación en una fecha.
5. Fundamental para analizar solvencia.
**Supuestos:** contabilidad. **Verificación:** activo = pasivo + patrimonio ✔.

### 180 · ¿Qué es el emprendimiento?
**R:** Proceso de crear y desarrollar un negocio.
**Razonamiento:**
1. Requiere idea, recursos, planificación y ejecución.
2. Implica asumir riesgo.
3. Puede ser social, tecnológico o tradicional.
4. Requiere habilidades de gestión y adaptación.
5. Motor de innovación y empleo.
**Supuestos:** economía y empresa. **Verificación:** creación de una empresa ✔.

---

## BLOQUE 19 — Filosofía, lógica y método (181–190)

### 181 · ¿Qué es la filosofía?
**R:** Disciplina que reflexiona sobre cuestiones fundamentales.
**Razonamiento:**
1. Aborda ser, conocimiento, ética, belleza, política.
2. Usa argumentación racional.
3. No se limita a datos empíricos.
4. Se apoya en la historia del pensamiento.
5. Busca claridad conceptual y sentido.
**Supuestos:** tradición filosófica. **Verificación:** textos clásicos ✔.

### 182 · ¿Qué es un silogismo?
**R:** Razonamiento deductivo con dos premisas y una conclusión.
**Razonamiento:**
1. Ejemplo clásico: “Todos los hombres son mortales; Sócrates es hombre; luego Sócrates es mortal”.
2. Válido si la conclusión se sigue necesariamente.
3. Puede ser válido con premisas falsas.
4. Forma típica: Barbara (AAA-1).
5. Base de la lógica aristotélica.
**Supuestos:** lógica clásica. **Verificación:** analizar validez formal ✔.

### 183 · ¿Qué es una falacia?
**R:** Razonamiento inválido que parece correcto.
**Razonamiento:**
1. Tipos: ad hominem, hombre de paja, falsa dicotomía, apelación a la autoridad.
2. Puede ser persuasiva pero no válida.
3. Detectar falacias mejora el pensamiento crítico.
4. No toda falacia es mentira; es un error de razonamiento.
5. Algunas son formales, otras informales.
**Supuestos:** lógica informal. **Verificación:** identificar falacia en un texto ✔.

### 184 · ¿Qué es la ética?
**R:** Reflexión sobre lo moralmente correcto.
**Razonamiento:**
1. Distinta de moral (conjunto de normas) y de derecho (normas legales).
2. Corrientes: utilitarismo, deontología, virtudes.
3. Busca fundamentos racionales del obrar.
4. Aplicada a bioética, ética empresarial, IA.
5. No siempre hay respuestas únicas.
**Supuestos:** filosofía moral. **Verificación:** dilemas éticos ✔.

### 185 · ¿Qué es la epistemología?
**R:** Rama de la filosofía que estudia el conocimiento.
**Razonamiento:**
1. Preguntas: ¿qué es conocer?, ¿cómo justificamos?
2. Distingue creencia, verdad y justificación.
3. Debate entre racionalismo y empirismo.
4. Relevante para ciencia y IA.
5. Analiza límites del conocimiento.
**Supuestos:** filosofía. **Verificación:** textos de Platón, Kant, Popper ✔.

### 186 · ¿Qué es el método científico?
**R:** Procedimiento sistemático para generar conocimiento.
**Razonamiento:**
1. Pasos: observación, hipótesis, experimentación, análisis, conclusión.
2. Debe ser replicable y falsable.
3. No es lineal ni rígido.
4. Se apoya en evidencia y revisión por pares.
5. Base de la ciencia moderna.
**Supuestos:** filosofía de la ciencia. **Verificación:** publicaciones científicas ✔.

### 187 · ¿Qué es la falsabilidad?
**R:** Propiedad de una hipótesis de poder ser refutada por evidencia.
**Razonamiento:**
1. Concepto central en Popper.
2. Una teoría no falsable no es científica (ej. astrología).
3. No significa que sea falsa, sino que puede contrastarse.
4. Ciencia avanza por conjeturas y refutaciones.
5. Complementa verificación y replicación.
**Supuestos:** epistemología. **Verificación:** experimento que puede refutar ✔.

### 188 · ¿Qué es la navaja de Ockham?
**R:** Principio de preferir la explicación más simple.
**Razonamiento:**
1. “No multiplicar los entes sin necesidad”.
2. No dice que lo simple sea verdadero, sino preferible.
3. Se usa en ciencia y razonamiento.
4. Complementa la evidencia empírica.
5. Cuidado: la simplicidad no reemplaza la prueba.
**Supuestos:** filosofía y método. **Verificación:** comparación de hipótesis ✔.

### 189 · ¿Qué es un dilema moral?
**R:** Situación con dos opciones moralmente problemáticas.
**Razonamiento:**
1. Cualquier elección implica un coste moral.
2. Ejemplo: mentira piadosa.
3. Se analiza con principios éticos.
4. No siempre hay solución “correcta”.
5. Relevante en bioética y política.
**Supuestos:** ética aplicada. **Verificación:** análisis de casos ✔.

### 190 · ¿Qué es la libertad?
**R:** Capacidad de actuar según la propia voluntad.
**Razonamiento:**
1. Distintas concepciones: negativa (ausencia de interferencia) y positiva (autodominio).
2. Debate sobre determinismo y libre albedrío.
3. Vinculada a responsabilidad moral.
4. Límites: derechos de otros, leyes.
5. Concepto central en filosofía política.
**Supuestos:** filosofía. **Verificación:** textos de Isaiah Berlin ✔.

---

## BLOQUE 20 — Vida cotidiana y habilidades (191–200)

### 191 · ¿Cómo ahorrar energía en casa?
**R:** Usando eficientemente aparatos y hábitos.
**Razonamiento:**
1. Apagar luces y equipos no usados.
2. Usar bombillas LED.
3. Electrodomésticos eficientes (etiqueta A).
4. Aislar ventanas y puertas.
5. Regular calefacción y aire acondicionado.
6. Aprovechar luz natural.
**Supuestos:** hogar típico. **Verificación:** factura eléctrica ✔.

### 192 · ¿Cómo reciclar correctamente?
**R:** Separando residuos según su material.
**Razonamiento:**
1. Contenedores: amarillo (envases), azul (papel), verde (vidrio), marrón (orgánico), gris (resto).
2. Limpiar envases antes de reciclar.
3. No mezclar residuos peligrosos.
4. Puntos limpios para electrónica, pilas, medicamentos.
5. Normativa local puede variar.
**Supuestos:** sistema de reciclaje español. **Verificación:** guía local de residuos ✔.

### 193 · ¿Cómo planificar un viaje?
**R:** Definiendo destino, fechas, presupuesto y reservas.
**Razonamiento:**
1. Elegir destino y duración.
2. Presupuesto: transporte, alojamiento, comida, actividades.
3. Reservar con antelación.
4. Documentación: DNI, pasaporte, visados.
5. Seguro de viaje si procede.
6. Plan flexible con alternativas.
**Supuestos:** viaje vacacional. **Verificación:** itinerario y reservas ✔.

### 194 · ¿Cómo estudiar eficazmente?
**R:** Con técnicas activas y descansos.
**Razonamiento:**
1. Técnica Pomodoro (25 min + 5 descanso).
2. Práctica recuperativa: autoevaluación.
3. Espaciado: repasar en días distintos.
4. Evitar multitarea.
5. Lugar sin distracciones.
6. Dormir bien.
**Supuestos:** aprendizaje humano. **Verificación:** mejora del rendimiento ✔.

### 195 · ¿Cómo mejorar la comunicación?
**R:** Escuchando activamente y expresándose con claridad.
**Razonamiento:**
1. Escucha activa: prestar atención, no interrumpir.
2. Lenguaje claro y conciso.
3. Empatía y respeto.
4. Lenguaje no verbal coherente.
5. Confirmar comprensión (parafrasear).
6. Feedback constructivo.
**Supuestos:** habilidades sociales. **Verificación:** mejor entendimiento ✔.

### 196 · ¿Cómo gestionar el tiempo?
**R:** Priorizando tareas y planificando.
**Razonamiento:**
1. Matriz de Eisenhower: urgente/importante.
2. Listas de tareas.
3. Bloques de tiempo.
4. Evitar procrastinación.
5. Revisar y ajustar.
6. Delegar cuando sea posible.
**Supuestos:** productividad personal. **Verificación:** tareas completadas ✔.

### 197 · ¿Cómo mantener una alimentación saludable?
**R:** Variada, equilibrada y moderada.
**Razonamiento:**
1. Frutas y verduras diarias.
2. Proteínas variadas.
3. Hidratos integrales.
4. Grasas saludables.
5. Reducir azúcares y ultraprocesados.
6. Hidratación adecuada.
7. Consultar profesional si hay condiciones.
**Supuestos:** adulto sano. **Verificación:** revisión nutricional ✔.

### 198 · ¿Cómo hacer ejercicio de forma segura?
**R:** Progresando gradualmente y escuchando al cuerpo.
**Razonamiento:**
1. Calentamiento previo.
2. Progresión de intensidad.
3. Técnica correcta.
4. Hidratación.
5. Descanso y recuperación.
6. Consultar si hay lesiones o condiciones.
7. Enfriamiento y estiramientos.
**Supuestos:** persona sin patologías. **Verificación:** menor riesgo de lesión ✔.

### 199 · ¿Cómo cuidar la salud mental?
**R:** Con hábitos, apoyo social y ayuda profesional si es necesario.
**Razonamiento:**
1. Dormir bien.
2. Ejercicio regular.
3. Relaciones sociales.
4. Gestión del estrés.
5. Tiempo para el ocio.
6. Buscar ayuda si el malestar persiste.
7. Reducir estigma.
**Supuestos:** persona adulta. **Verificación:** bienestar general ✔.

### 200 · ¿Cómo tomar decisiones?
**R:** Evaluando opciones, riesgos y valores.
**Razonamiento:**
1. Definir el problema.
2. Identificar opciones.
3. Evaluar pros y contras.
4. Considerar consecuencias y valores.
5. Consultar cuando sea necesario.
6. Decidir y revisar.
7. Aprender del resultado.
**Supuestos:** decisiones personales. **Verificación:** decisión informada ✔.

---


---

## BLOQUE 21 — Matemáticas (201–210)

### 201 · Resuelve 3x − 7 = 11.
**R:** x = 6.
**Razonamiento:**
1. Sumar 7 a ambos lados da 3x = 18
2. dividir por 3 da x = 6
3. sustituir devuelve 18−7=11.
**Supuestos:** Ecuación lineal real con coeficiente no nulo. **Verificación:** 3·6−7=11 ✔.

### 202 · ¿Cuáles son las raíces de x² − 5x + 6 = 0?
**R:** x = 2 y x = 3.
**Razonamiento:**
1. Factorizar como (x−2)(x−3)
2. igualar cada factor a cero
3. obtener 2 y 3.
**Supuestos:** Coeficientes reales y factorización exacta. **Verificación:** Ambas sustituciones producen cero ✔.

### 203 · Si 4 cuadernos cuestan 10 €, ¿cuánto cuestan 7 al mismo precio unitario?
**R:** 17,50 €.
**Razonamiento:**
1. El precio unitario es 10/4=2,50 €
2. multiplicar por 7
3. obtener 17,50 €.
**Supuestos:** Precio unitario constante y sin descuentos. **Verificación:** 17,50/7=2,50 € ✔.

### 204 · ¿Qué resto deja 137 al dividirlo entre 9?
**R:** 2.
**Razonamiento:**
1. 9·15=135
2. 137−135=2
3. el resto está entre 0 y 8.
**Supuestos:** División euclídea en enteros no negativos. **Verificación:** 137=9·15+2 ✔.

### 205 · En una bolsa hay 3 bolas rojas y 2 azules. ¿Probabilidad de extraer una azul?
**R:** 2/5 = 40 %.
**Razonamiento:**
1. Hay 5 bolas
2. 2 son azules
3. casos favorables sobre posibles es 2/5.
**Supuestos:** Extracción uniforme de una sola bola. **Verificación:** 2/5+3/5=1 ✔.

### 206 · Dados u=(2,−1) y v=(3,4), ¿cuál es u·v?
**R:** 2.
**Razonamiento:**
1. El producto escalar es 2·3+(−1)·4
2. calcular 6−4
3. el resultado es el escalar 2.
**Supuestos:** Vectores en el plano con producto escalar usual. **Verificación:** 2·3−4=2 ✔.

### 207 · Deriva f(x)=3x²−4x+7.
**R:** f'(x)=6x−4.
**Razonamiento:**
1. La derivada de 3x² es 6x
2. la de −4x es −4
3. la constante deriva a cero.
**Supuestos:** Derivación respecto de x en los reales. **Verificación:** En x=2 la pendiente es 8 ✔.

### 208 · Calcula la integral definida de 2x entre 0 y 3.
**R:** 9.
**Razonamiento:**
1. Una primitiva es x²
2. evaluar x² entre 0 y 3
3. restar 9−0.
**Supuestos:** Integral ordinaria de una función continua. **Verificación:** El triángulo de base 3 y altura 6 tiene área 9 ✔.

### 209 · Convierte 101101₂ a decimal.
**R:** 45.
**Razonamiento:**
1. Los pesos activos son 32, 8, 4 y 1
2. sumarlos da 45
3. la base es dos.
**Supuestos:** Entero binario sin signo. **Verificación:** 45=32+8+4+1 ✔.

### 210 · Calcula el determinante de [[2,1],[5,3]].
**R:** 1.
**Razonamiento:**
1. Para 2×2 se calcula ad−bc
2. sustituir 2·3−1·5
3. obtener 1.
**Supuestos:** Matriz cuadrada sobre los reales. **Verificación:** 6−5=1 y el determinante no es cero ✔.


## BLOQUE 22 — Programación y estructuras de datos (211–220)

### 211 · ¿Qué imprime sum(i for i in range(4)) en Python 3?
**R:** 6.
**Razonamiento:**
1. range(4) produce 0,1,2,3
2. sum agrega los cuatro valores
3. el total es 6.
**Supuestos:** Python 3 y range estándar. **Verificación:** 0+1+2+3=6 ✔.

### 212 · ¿Qué caso base evita una recursión infinita al calcular factorial?
**R:** n=0 o n=1 devuelve 1.
**Razonamiento:**
1. Cada llamada reduce n
2. el caso base devuelve sin recursión
3. sin caso alcanzable la pila sigue creciendo.
**Supuestos:** Entrada entera no negativa. **Verificación:** 4·3·2·1=24 y factorial(0)=1 ✔.

### 213 · ¿Por qué una tabla hash debe gestionar colisiones?
**R:** Claves distintas pueden producir el mismo índice.
**Razonamiento:**
1. El espacio de posiciones es finito
2. una función hash no tiene por qué ser inyectiva
3. encadenamiento o direccionamiento abierto conserva ambas claves.
**Supuestos:** Tabla hash finita. **Verificación:** Dos claves con el mismo hash deben poder recuperarse ✔.

### 214 · ¿Qué estructura LIFO permite deshacer primero la última operación?
**R:** Una pila.
**Razonamiento:**
1. LIFO significa último en entrar, primero en salir
2. push añade arriba
3. pop retira el elemento más reciente.
**Supuestos:** Pila con operaciones push y pop. **Verificación:** push(A), push(B), pop() devuelve B ✔.

### 215 · ¿Qué diferencia hay entre INNER JOIN y LEFT JOIN en SQL?
**R:** INNER conserva coincidencias; LEFT conserva todas las filas izquierdas.
**Razonamiento:**
1. INNER exige coincidencia en ambas tablas
2. LEFT mantiene cada fila izquierda
3. si no hay pareja, las columnas derechas quedan NULL.
**Supuestos:** Unión con condición explícita. **Verificación:** Una fila izquierda sin pareja aparece solo en LEFT JOIN ✔.

### 216 · ¿Cuál es la complejidad peor caso de buscar en una lista enlazada no ordenada de n nodos?
**R:** O(n).
**Razonamiento:**
1. El elemento puede estar al final o no existir
2. hay que recorrer hasta n nodos
3. cada enlace se visita en tiempo constante.
**Supuestos:** Lista enlazada y comparación de coste constante. **Verificación:** Duplicar n puede duplicar comparaciones ✔.

### 217 · ¿Qué puede ocurrir al incrementar un contador compartido sin sincronización?
**R:** Actualizaciones perdidas.
**Razonamiento:**
1. Dos hilos pueden leer el mismo valor
2. ambos calculan el mismo siguiente valor
3. una escritura pisa la otra.
**Supuestos:** Acceso concurrente no atómico. **Verificación:** Dos incrementos simultáneos desde cero pueden dejar uno ✔.

### 218 · ¿Qué ventaja aporta la inmutabilidad en concurrencia?
**R:** Reduce conflictos por modificaciones compartidas.
**Razonamiento:**
1. El objeto no cambia tras crearse
2. varios lectores comparten un estado estable
3. se reducen carreras asociadas a escrituras.
**Supuestos:** Datos realmente inmutables. **Verificación:** Dos lectores observan el mismo valor ✔.

### 219 · ¿Qué comprueba una prueba unitaria?
**R:** El comportamiento de una unidad pequeña y aislada.
**Razonamiento:**
1. Se fijan entradas
2. se compara la salida con lo esperado
3. el aislamiento ayuda a localizar errores.
**Supuestos:** Entorno controlado y dependencias simuladas cuando convenga. **Verificación:** sumar(2,3) debe devolver 5 ✔.

### 220 · ¿Qué representa ^ en una expresión regular con modo multilínea?
**R:** El inicio de cada línea.
**Razonamiento:**
1. El ancla marca el comienzo
2. con modo multilínea se aplica a cada línea
3. sin él suele referirse al comienzo de la cadena.
**Supuestos:** Motor regex con modo multilínea activado. **Verificación:** ^Hola coincide con Hola al inicio de una línea ✔.


## BLOQUE 23 — Lógica y razonamiento (221–230)

### 221 · Si P implica Q y Q es falsa, ¿qué se concluye sobre P?
**R:** P es falsa.
**Razonamiento:**
1. Si P fuera verdadera y Q falsa, la implicación sería falsa
2. para mantener la premisa P no puede ser verdadera
3. es modus tollens.
**Supuestos:** Lógica proposicional clásica. **Verificación:** P→Q, ¬Q implica ¬P ✔.

### 222 · ¿Es válida la inferencia «si llueve, la calle se moja; la calle está mojada; luego llovió»?
**R:** No; es afirmación del consecuente.
**Razonamiento:**
1. La lluvia basta para mojar la calle
2. no es la única causa posible
3. una manguera ofrece un contraejemplo.
**Supuestos:** No hay premisa que excluya otras causas. **Verificación:** Puede no llover y la calle estar mojada ✔.

### 223 · ¿Qué diferencia hay entre condición necesaria y suficiente?
**R:** La necesaria debe cumplirse; la suficiente garantiza el resultado.
**Razonamiento:**
1. A necesaria para B significa B→A
2. A suficiente para B significa A→B
3. las direcciones no se intercambian.
**Supuestos:** Implicaciones clásicas. **Verificación:** Ser múltiplo de 4 basta para ser par; ser par es necesario ✔.

### 224 · ¿Cuál es la negación de «todos los registros son válidos»?
**R:** Existe al menos un registro no válido.
**Razonamiento:**
1. La forma universal es para todo x, V(x)
2. al negar el universal aparece existe x
3. la propiedad pasa a no V(x).
**Supuestos:** Dominio de registros definido. **Verificación:** Un único registro inválido refuta la universal ✔.

### 225 · Si A={1,2,3} y B={3,4}, ¿cuál es A∩B?
**R:** {3}.
**Razonamiento:**
1. La intersección contiene elementos comunes
2. 1 y 2 solo están en A
3. 4 solo está en B
4. 3 pertenece a ambos.
**Supuestos:** Conjuntos finitos. **Verificación:** 3∈A y 3∈B ✔.

### 226 · ¿Qué es un argumento válido con premisas falsas?
**R:** Uno cuya forma preservaría la verdad de la conclusión si las premisas fueran verdaderas.
**Razonamiento:**
1. La validez depende de la estructura
2. no permite premisas verdaderas y conclusión falsa
3. la solidez añade premisas verdaderas.
**Supuestos:** Lógica deductiva clásica. **Verificación:** Un silogismo formalmente válido puede partir de una premisa falsa ✔.

### 227 · ¿Qué es un contraejemplo a una afirmación universal?
**R:** Un caso que incumple la propiedad afirmada.
**Razonamiento:**
1. La afirmación pretende abarcar todo el dominio
2. un solo elemento que no cumple la propiedad la refuta
3. no se requieren varios casos.
**Supuestos:** Dominio y propiedad bien definidos. **Verificación:** El número 2 refuta «todos los primos son impares» ✔.

### 228 · ¿Cómo se llama una proposición verdadera bajo toda asignación de valores?
**R:** Tautología.
**Razonamiento:**
1. Su forma garantiza verdad
2. P o no P es verdadera con P verdadera y también con P falsa
3. no depende de datos empíricos.
**Supuestos:** Lógica clásica bivalente. **Verificación:** P∨¬P siempre vale verdadero ✔.

### 229 · ¿Qué diferencia hay entre correlación y causalidad?
**R:** Correlación es asociación; causalidad afirma producción de un efecto.
**Razonamiento:**
1. La correlación describe variación conjunta
2. puede haber causas comunes o causalidad inversa
3. inferir causalidad exige descartar alternativas.
**Supuestos:** Inferencia científica con posibles confusores. **Verificación:** Helados y ahogamientos pueden crecer juntos por el verano ✔.

### 230 · ¿Qué expresa la navaja de Ockham al comparar modelos?
**R:** Evitar complejidad innecesaria si otra explicación explica igual la evidencia.
**Razonamiento:**
1. La simplicidad reduce supuestos gratuitos
2. entre modelos comparables se prefiere el menos complejo
3. evidencia nueva puede justificar más complejidad.
**Supuestos:** Principio metodológico, no prueba de verdad. **Verificación:** Un parámetro inútil no mejora un modelo ✔.


## BLOQUE 24 — Ciencias naturales (231–240)

### 231 · ¿Por qué el hielo flota sobre el agua líquida?
**R:** Porque su densidad suele ser menor.
**Razonamiento:**
1. La estructura cristalina del hielo ocupa más volumen
2. la masa comparable queda distribuida en mayor volumen
3. menor densidad favorece la flotación.
**Supuestos:** Agua dulce cerca de presión atmosférica. **Verificación:** El hielo desplaza agua cuyo peso iguala al suyo ✔.

### 232 · ¿Qué ocurre con la presión de un gas ideal si se duplica la temperatura absoluta a volumen constante?
**R:** Se duplica.
**Razonamiento:**
1. PV=nRT
2. con n y V fijos P/T es constante
3. duplicar T en kelvin duplica P.
**Supuestos:** Gas ideal y volumen constante. **Verificación:** P₂/P₁=T₂/T₁=2 ✔.

### 233 · ¿Qué corriente circula por una resistencia de 6 Ω conectada a 12 V?
**R:** 2 A.
**Razonamiento:**
1. La ley de Ohm es V=IR
2. despejar I=V/R
3. 12/6=2 amperios.
**Supuestos:** Resistencia óhmica ideal. **Verificación:** 2 A·6 Ω=12 V ✔.

### 234 · ¿Qué relación hay entre pH 3 y pH 5 respecto a la actividad de H⁺?
**R:** pH 3 tiene cien veces más actividad de H⁺.
**Razonamiento:**
1. pH es −log₁₀ de actividad
2. dos unidades representan factor 10²
3. menor pH significa mayor actividad.
**Supuestos:** Comparación en condiciones acuosas compatibles. **Verificación:** 10⁻³/10⁻⁵=100 ✔.

### 235 · ¿Qué proceso permite el paso neto de agua por una membrana semipermeable hacia una disolución más concentrada?
**R:** Ósmosis.
**Razonamiento:**
1. La membrana deja pasar disolvente
2. el potencial químico impulsa el flujo neto
3. el equilibrio depende también de presión y composición.
**Supuestos:** Membrana semipermeable y soluciones acuosas diluidas. **Verificación:** Un gradiente osmótico puede cambiar el volumen a ambos lados ✔.

### 236 · ¿Cuántas divisiones celulares ocurren en la meiosis?
**R:** Dos divisiones sucesivas.
**Razonamiento:**
1. Meiosis I separa homólogos
2. meiosis II separa cromátidas hermanas
3. el proceso suele producir cuatro células haploides.
**Supuestos:** Eucariotas con reproducción sexual. **Verificación:** Una célula diploide puede originar cuatro productos haploides ✔.

### 237 · ¿Qué hacen las enzimas en una reacción bioquímica?
**R:** Aceleran la reacción al reducir la energía de activación.
**Razonamiento:**
1. Estabilizan el estado de transición
2. aumentan la velocidad
3. no cambian la energía libre global ni el equilibrio final.
**Supuestos:** Enzima funcional y condiciones compatibles. **Verificación:** El equilibrio se alcanza más rápido, no cambia ✔.

### 238 · ¿Por qué la resistencia de un metal suele aumentar al calentarlo?
**R:** Aumenta la dispersión de electrones por vibraciones de la red.
**Razonamiento:**
1. La temperatura eleva vibraciones atómicas
2. los electrones se dispersan más
3. baja la movilidad y sube la resistividad.
**Supuestos:** Metal común y rango sin cambio de fase. **Verificación:** La resistencia medida suele tener pendiente positiva ✔.

### 239 · ¿Qué mecanismos generan diversidad genética en la meiosis?
**R:** Entrecruzamiento y distribución independiente de cromosomas.
**Razonamiento:**
1. Cromátidas no hermanas intercambian segmentos
2. pares homólogos se orientan independientemente
3. aparecen nuevas combinaciones alélicas.
**Supuestos:** Meiosis con cromosomas homólogos. **Verificación:** La descendencia puede combinar alelos de formas nuevas ✔.

### 240 · ¿Qué distingue una energía renovable de una no renovable?
**R:** La renovable se repone a escala humana; la no renovable tarda mucho más en formarse.
**Razonamiento:**
1. La clasificación depende de la tasa de reposición
2. sol y viento se renuevan continuamente
3. combustibles fósiles requieren escalas geológicas.
**Supuestos:** Definición por escala temporal. **Verificación:** Un yacimiento fósil no se repone en décadas ✔.


## BLOQUE 25 — Lengua española (241–250)

### 241 · ¿Por qué «Espero que vienes mañana» no es la forma normativa habitual?
**R:** Se dice «Espero que vengas mañana».
**Razonamiento:**
1. La subordinada expresa expectativa
2. este patrón rige normalmente subjuntivo
3. venir en segunda persona subjuntiva es vengas.
**Supuestos:** Español estándar y sentido de expectativa. **Verificación:** «Espero que vengas» es la forma normativa ✔.

### 242 · ¿Qué función tiene «se» en «Se venden pisos»?
**R:** Marca una pasiva refleja.
**Razonamiento:**
1. Pisos es sujeto paciente
2. el verbo concuerda en plural
3. el agente no se expresa.
**Supuestos:** Análisis sintáctico tradicional. **Verificación:** «Se vende un piso» y «Se venden pisos» concuerdan ✔.

### 243 · ¿Qué diferencia hay entre «él» y «el»?
**R:** «Él» es pronombre; «el» es artículo.
**Razonamiento:**
1. La tilde diacrítica distingue categorías
2. «Él llegó» usa pronombre
3. «el libro» usa artículo.
**Supuestos:** Ortografía normativa española. **Verificación:** «Él compró el libro» usa ambos correctamente ✔.

### 244 · ¿Qué es una subordinada sustantiva?
**R:** Una subordinada que desempeña función propia de un sintagma nominal.
**Razonamiento:**
1. Puede ser sujeto o complemento
2. suele introducirse con que o infinitivo
3. a veces se sustituye por eso para identificarla.
**Supuestos:** Análisis sintáctico del español. **Verificación:** «Me alegra que vengas» equivale funcionalmente a «Me alegra eso» ✔.

### 245 · ¿Por qué «solo» se escribe normalmente sin tilde?
**R:** La norma actual recomienda «solo» sin tilde incluso con valor adverbial.
**Razonamiento:**
1. La recomendación general evita tilde diacrítica
2. el contexto suele resolver la interpretación
3. solo se admite excepcionalmente si se aprecia ambigüedad real.
**Supuestos:** Ortografía académica vigente. **Verificación:** «Trabajo solo los lunes» se interpreta por contexto ✔.

### 246 · ¿Qué relación semántica hay entre «roble» y «árbol»?
**R:** Roble es hipónimo de árbol.
**Razonamiento:**
1. Árbol es categoría general
2. roble es clase particular
3. todo roble es árbol pero no todo árbol es roble.
**Supuestos:** Relaciones léxicas jerárquicas. **Verificación:** «Un roble es un árbol» ✔.

### 247 · ¿Qué es un anacoluto?
**R:** Una ruptura de la construcción sintáctica esperada.
**Razonamiento:**
1. Se inicia una estructura y se continúa con otra incompatible
2. aparece a menudo en habla espontánea
3. puede corregirse reformulando.
**Supuestos:** Terminología gramatical y retórica. **Verificación:** «Yo, no me parece bien» muestra ruptura sintáctica ✔.

### 248 · ¿Qué diferencia hay entre denotación y connotación?
**R:** Denotación es significado referencial; connotación añade asociaciones culturales o valorativas.
**Razonamiento:**
1. La denotación identifica el concepto
2. la connotación incorpora matices
3. el contexto puede modificar esos matices.
**Supuestos:** Análisis semántico contextual. **Verificación:** «Casa» y «hogar» comparten referencia aproximada y distinta carga ✔.

### 249 · ¿Qué es una perífrasis verbal?
**R:** Un conjunto de auxiliar y forma no personal que funciona como núcleo verbal complejo.
**Razonamiento:**
1. El auxiliar aporta matiz modal o aspectual
2. el verbo principal va en infinitivo, gerundio o participio
3. no toda secuencia de dos verbos es perífrasis.
**Supuestos:** Gramática del español. **Verificación:** «Voy a salir» expresa futuro próximo ✔.

### 250 · ¿Por qué se dice «hubo muchas quejas» y no «hubieron muchas quejas» en uso existencial estándar?
**R:** Porque «haber» existencial es impersonal y permanece en singular.
**Razonamiento:**
1. No tiene sujeto gramatical plural
2. el grupo nominal no fuerza concordancia
3. el auxiliar haber sí puede conjugarse en plural en otros usos.
**Supuestos:** Construcción existencial del español estándar. **Verificación:** «Hubo tres llamadas» ✔.


## BLOQUE 26 — Historia, geografía y ciudadanía (251–260)

### 251 · ¿Qué tratado formalizó la paz entre Alemania y los aliados tras la Primera Guerra Mundial?
**R:** El Tratado de Versalles de 1919.
**Razonamiento:**
1. El armisticio de 1918 detuvo los combates
2. el tratado se firmó el 28 de junio de 1919
3. no son el mismo acto.
**Supuestos:** Cronología histórica convencional. **Verificación:** La firma tuvo lugar el 28-06-1919 ✔.

### 252 · ¿Qué diferencia hay entre latitud y longitud?
**R:** Latitud mide norte o sur del ecuador; longitud mide este u oeste de Greenwich.
**Razonamiento:**
1. Latitud parte de 0° en el ecuador
2. longitud parte del meridiano de referencia
3. ambas localizan posiciones terrestres.
**Supuestos:** Sistema geográfico convencional. **Verificación:** Madrid está aproximadamente a 40,4° N y 3,7° O ✔.

### 253 · ¿Qué institución de la UE representa directamente a la ciudadanía mediante elecciones?
**R:** El Parlamento Europeo.
**Razonamiento:**
1. Sus miembros son elegidos por sufragio directo
2. participa en legislación y presupuesto
3. no debe confundirse con la Comisión ni con el Consejo Europeo.
**Supuestos:** Instituciones de la Unión Europea. **Verificación:** Las elecciones europeas eligen eurodiputados ✔.

### 254 · ¿Qué es una constitución en un Estado moderno?
**R:** La norma fundamental que organiza el poder y reconoce derechos básicos.
**Razonamiento:**
1. Define instituciones y competencias
2. limita el ejercicio del poder
3. reconoce derechos
4. las normas inferiores deben respetarla.
**Supuestos:** Constitucionalismo democrático. **Verificación:** Una norma incompatible puede ser anulada por el órgano competente ✔.

### 255 · ¿Por qué existen husos horarios?
**R:** Porque la rotación terrestre hace que distintas longitudes reciban la luz solar en momentos distintos.
**Razonamiento:**
1. La Tierra gira aproximadamente 360° en 24 horas
2. 15° equivalen a una hora
3. los husos civiles se adaptan a fronteras políticas.
**Supuestos:** Rotación terrestre y hora civil convencional. **Verificación:** 30° de longitud representan unas dos horas solares ✔.

### 256 · ¿Qué designa la descolonización del siglo XX?
**R:** La independencia política de territorios sometidos a potencias coloniales.
**Razonamiento:**
1. Tras la Segunda Guerra Mundial se debilitaron imperios europeos
2. crecieron movimientos nacionalistas
3. hubo procesos negociados y conflictos diversos.
**Supuestos:** Historia global contemporánea. **Verificación:** India obtuvo independencia en 1947 ✔.

### 257 · ¿Qué diferencia hay entre tiempo meteorológico y clima?
**R:** Tiempo es estado atmosférico a corto plazo; clima resume patrones de largo plazo.
**Razonamiento:**
1. El tiempo describe días concretos
2. el clima usa distribuciones de observaciones prolongadas
3. un día frío no refuta una tendencia climática.
**Supuestos:** Meteorología y climatología. **Verificación:** Un día lluvioso es tiempo; frecuencia de lluvia durante décadas es clima ✔.

### 258 · ¿Qué diferencia hay entre frontera política y frontera física?
**R:** La política es una delimitación jurídica; la física se apoya en rasgos naturales.
**Razonamiento:**
1. Una frontera física puede seguir ríos o montañas
2. una política deriva de tratados y procesos históricos
3. ambas pueden coincidir o no.
**Supuestos:** Geografía política general. **Verificación:** Los Pirineos son rasgo físico y la frontera franco-española es política ✔.

### 259 · ¿Qué significa sufragio universal?
**R:** Reconocimiento general del derecho al voto en igualdad política, con requisitos legales comunes.
**Razonamiento:**
1. Supera restricciones históricas por riqueza o sexo
2. puede exigir edad y ciudadanía
3. no significa que cualquier persona de cualquier edad vote.
**Supuestos:** Democracia constitucional y legislación nacional. **Verificación:** La extensión del voto a las mujeres fue un hito ✔.

### 260 · En escala 1:100.000, ¿qué distancia real representa 1 cm?
**R:** 1 km.
**Razonamiento:**
1. Un centímetro equivale a 100.000 cm
2. eso son 1.000 metros
3. convertir a kilómetros da uno.
**Supuestos:** Escala numérica uniforme. **Verificación:** 2 cm representan 2 km ✔.


## BLOQUE 27 — Economía y empresa (261–270)

### 261 · Una empresa vende 80 unidades a 15 € cada una. ¿Cuál es el ingreso bruto?
**R:** 1.200 €.
**Razonamiento:**
1. Ingreso es precio por cantidad
2. 80·15=1.200
3. las unidades se cancelan y queda moneda.
**Supuestos:** Mismo precio y sin devoluciones. **Verificación:** 1.200/80=15 € por unidad ✔.

### 262 · Un producto pasa de 50 € a 60 €. ¿Cuál es el aumento porcentual?
**R:** 20 %.
**Razonamiento:**
1. El aumento absoluto es 10 €
2. dividir por el valor inicial 50 da 0,2
3. multiplicar por cien da 20 %.
**Supuestos:** Comparación simple sin otros ajustes. **Verificación:** 50·1,20=60 ✔.

### 263 · Costes fijos 300 €, precio 20 € y coste variable 8 € por unidad: ¿punto de equilibrio?
**R:** 25 unidades.
**Razonamiento:**
1. Margen por unidad 20−8=12 €
2. dividir costes fijos entre margen
3. 300/12=25 unidades.
**Supuestos:** Precio y coste variable constantes; se vende toda la producción. **Verificación:** Ingresos 500 € y costes 300+200=500 € ✔.

### 264 · ¿Qué interés simple genera 1.000 € al 5 % anual durante dos años?
**R:** 100 €.
**Razonamiento:**
1. I=C·r·t
2. sustituir 1.000·0,05·2
3. resultado 100 €.
**Supuestos:** Tasa constante y tiempo expresado en años. **Verificación:** Capital final 1.100 € ✔.

### 265 · Una cesta de 200 € sube de precio un 3 %. ¿Cuánto cuesta?
**R:** 206 €.
**Razonamiento:**
1. El 3 % de 200 es 6
2. sumar 6 al precio inicial
3. total 206 €.
**Supuestos:** Aumento exacto del 3 % en esa cesta. **Verificación:** 206/200−1=3 % ✔.

### 266 · ¿Qué es el coste de oportunidad?
**R:** El valor de la mejor alternativa sacrificada al elegir.
**Razonamiento:**
1. Los recursos son limitados
2. elegir excluye alternativas
3. el coste relevante es el beneficio de la mejor opción descartada.
**Supuestos:** Alternativas incompatibles y valor definido. **Verificación:** Si estudiar impide ganar 12 €, ese ingreso puede ser el coste ✔.

### 267 · ¿Qué diferencia hay entre liquidez y solvencia?
**R:** Liquidez es capacidad de pago inmediato; solvencia es capacidad financiera global y sostenida.
**Razonamiento:**
1. Liquidez depende de efectivo y activos líquidos
2. solvencia considera activos, pasivos y flujos futuros
3. puede haber solvencia sin caja inmediata.
**Supuestos:** Análisis financiero de entidades. **Verificación:** Patrimonio positivo puede coexistir con falta de efectivo ✔.

### 268 · ¿Qué representa el valor añadido?
**R:** Producción menos consumos intermedios utilizados.
**Razonamiento:**
1. La producción mide bienes y servicios generados
2. los consumos intermedios son insumos comprados
3. restarlos evita doble contabilización.
**Supuestos:** Contabilidad nacional con valoraciones comparables. **Verificación:** Pan vendido por 5 € con harina de 2 € aporta 3 € ✔.

### 269 · ¿Por qué diversificar una cartera puede reducir el riesgo?
**R:** Porque activos no perfectamente correlacionados pueden compensar variaciones.
**Razonamiento:**
1. El riesgo agregado depende de volatilidad y covarianza
2. correlación menor que uno puede reducir variabilidad
3. riesgo sistemático no desaparece.
**Supuestos:** Modelo de cartera y relaciones no constantes. **Verificación:** La cartera puede tener volatilidad inferior a la media ponderada ✔.

### 270 · ¿Qué es una externalidad negativa?
**R:** Un coste impuesto a terceros y no reflejado plenamente en el precio.
**Razonamiento:**
1. La actividad afecta a personas ajenas al intercambio
2. el coste social supera el privado
3. regulación o impuestos pueden corregirlo.
**Supuestos:** Economía del bienestar. **Verificación:** Contaminación que perjudica vecinos sin precio asociado ✔.


## BLOQUE 28 — Sistemas e ingeniería informática (271–280)

### 271 · ¿Por qué un sistema operativo planifica procesos?
**R:** Para repartir CPU y coordinar tareas ejecutables.
**Razonamiento:**
1. Varios procesos compiten por procesador
2. el planificador decide turno y duración
3. la política afecta latencia y equidad.
**Supuestos:** Sistema multitarea convencional. **Verificación:** La planificación por turnos asigna porciones de CPU ✔.

### 272 · ¿Qué diferencia hay entre RAM y SSD?
**R:** RAM es memoria de trabajo volátil; SSD almacena datos de forma no volátil.
**Razonamiento:**
1. RAM contiene datos activos y se pierde al apagar
2. SSD conserva archivos
3. difieren en función, latencia y persistencia.
**Supuestos:** Ordenador personal actual. **Verificación:** Un archivo en SSD permanece tras apagar ✔.

### 273 · ¿Qué aporta comparar el SHA-256 de un archivo descargado?
**R:** Detecta con alta probabilidad cambios o corrupción, si el hash esperado es confiable.
**Razonamiento:**
1. SHA-256 genera un resumen de 256 bits
2. cambios suelen alterar el hash
3. comparar detecta discrepancias
4. autenticidad requiere confiar en la fuente del hash.
**Supuestos:** Hash criptográfico y referencia publicada por canal confiable. **Verificación:** Coincidencia con hash auténtico respalda integridad ✔.

### 274 · ¿Para qué sirven los certificados digitales en TLS?
**R:** Vinculan identidad declarada del servidor con una clave pública.
**Razonamiento:**
1. El servidor presenta certificado
2. el cliente valida cadena y nombre
3. la clave ayuda a autenticar el extremo y establecer claves de sesión.
**Supuestos:** TLS correctamente configurado y autoridad confiable. **Verificación:** Un certificado válido para el dominio reduce suplantación ✔.

### 275 · ¿Qué significa idempotencia en una API?
**R:** Repetir una petición produce el mismo efecto final que ejecutarla una vez.
**Razonamiento:**
1. Una operación idempotente no acumula cambios al repetirse
2. fijar un valor puede serlo
3. incrementar una cantidad normalmente no lo es
4. facilita reintentos.
**Supuestos:** Semántica de API y estado final. **Verificación:** Establecer cantidad=5 dos veces deja 5 ✔.

### 276 · ¿Qué propiedades resume ACID en bases de datos?
**R:** Atomicidad, consistencia, aislamiento y durabilidad.
**Razonamiento:**
1. Atomicidad evita operaciones parciales
2. consistencia preserva restricciones
3. aislamiento controla concurrencia
4. durabilidad conserva cambios confirmados.
**Supuestos:** Base de datos transaccional. **Verificación:** Una transferencia no debe debitar sin acreditar ✔.

### 277 · ¿Por qué un índice B-tree acelera consultas por rango?
**R:** Mantiene claves ordenadas y permite localizar el inicio y recorrer el intervalo.
**Razonamiento:**
1. El árbol equilibrado limita altura
2. la búsqueda desciende por comparaciones
3. luego se recorren claves vecinas
4. no hace falta escanear toda la tabla.
**Supuestos:** Índice B-tree o B+ tree. **Verificación:** Una consulta entre 100 y 120 evita filas ajenas al rango ✔.

### 278 · ¿Qué es una dirección MAC en Ethernet?
**R:** Un identificador de capa de enlace asociado a una interfaz.
**Razonamiento:**
1. Las tramas incluyen MAC origen y destino
2. la dirección clásica tiene 48 bits
3. no equivale a IP ni identifica necesariamente a una persona.
**Supuestos:** Ethernet convencional. **Verificación:** Una trama Ethernet contiene direcciones MAC de origen y destino ✔.

### 279 · ¿Qué diferencia hay entre cifrado simétrico y asimétrico?
**R:** El simétrico usa una clave compartida; el asimétrico usa un par pública/privada.
**Razonamiento:**
1. El simétrico requiere secreto compartido
2. el asimétrico permite distribuir clave pública
3. suele ser más costoso
4. protocolos combinan ambos.
**Supuestos:** Criptografía moderna y gestión segura de claves. **Verificación:** TLS negocia con mecanismos asimétricos y cifra sesión simétricamente ✔.

### 280 · ¿Por qué un contenedor no equivale exactamente a una máquina virtual?
**R:** El contenedor suele compartir kernel del host; la máquina virtual ejecuta un sistema operativo invitado.
**Razonamiento:**
1. Contenedores aíslan procesos mediante el kernel
2. VM virtualiza hardware
3. cada VM puede arrancar kernel propio
4. cambian consumo y aislamiento.
**Supuestos:** Contenedores Linux y virtualización convencional. **Verificación:** Varios contenedores comparten kernel del host ✔.


## BLOQUE 29 — Estadística y método científico (281–290)

### 281 · ¿Cuál es la media de 2, 3, 3, 6 y 11?
**R:** 5.
**Razonamiento:**
1. La suma es 25
2. hay cinco observaciones
3. dividir 25 entre 5 da 5.
**Supuestos:** Datos con igual ponderación. **Verificación:** 5·5=25 ✔.

### 282 · ¿Cuál es la mediana de 1, 4, 7, 9, 20, 30?
**R:** 8.
**Razonamiento:**
1. Hay seis datos ordenados
2. los centrales son 7 y 9
3. su media es 8.
**Supuestos:** Muestra finita ordenada. **Verificación:** La mediana es (7+9)/2=8 ✔.

### 283 · Un test tiene sensibilidad del 90 %. ¿Qué significa?
**R:** Detecta el 90 % de los casos que realmente presentan la condición.
**Razonamiento:**
1. Sensibilidad=verdaderos positivos/(verdaderos positivos+falsos negativos)
2. un 90 % deja 10 % de falsos negativos entre positivos reales
3. no es valor predictivo positivo.
**Supuestos:** Estado real conocido y definición diagnóstica estándar. **Verificación:** De 100 casos positivos reales detecta unos 90 ✔.

### 284 · ¿Qué significa un intervalo de confianza frecuentista del 95 %?
**R:** Que el procedimiento produce intervalos que contienen el parámetro verdadero en aproximadamente el 95 % de repeticiones.
**Razonamiento:**
1. El parámetro se trata como fijo
2. la muestra cambia
3. el intervalo cambia
4. la cobertura describe el procedimiento a largo plazo, no una probabilidad posterior del intervalo observado.
**Supuestos:** Inferencia frecuentista y supuestos del modelo. **Verificación:** En simulaciones repetidas cerca del 95 % de intervalos cubren el valor real ✔.

### 285 · ¿Qué problema introduce el sesgo de selección en una encuesta?
**R:** La muestra puede no representar a la población objetivo.
**Razonamiento:**
1. La participación depende de características relacionadas con la respuesta
2. la muestra queda sistemáticamente distinta
3. aumentar su tamaño no elimina el sesgo.
**Supuestos:** Población objetivo y mecanismo de selección definidos. **Verificación:** Una encuesta solo online puede infrarrepresentar a quienes no tienen internet ✔.

### 286 · ¿Por qué separar entrenamiento, validación y prueba en aprendizaje automático?
**R:** Para ajustar parámetros, seleccionar decisiones y estimar rendimiento final en datos no usados.
**Razonamiento:**
1. Entrenamiento actualiza pesos
2. validación ayuda a elegir hiperparámetros
3. prueba se reserva para evaluación final
4. reutilizar test induce sobreajuste de evaluación.
**Supuestos:** Particiones independientes y ausencia de fuga de datos. **Verificación:** Un test sellado estima mejor la generalización que el entrenamiento ✔.

### 287 · ¿Qué significa que un estimador sea insesgado?
**R:** Que su esperanza matemática coincide con el parámetro estimado.
**Razonamiento:**
1. El estimador varía entre muestras
2. se calcula su esperanza bajo el muestreo
3. si coincide con el parámetro el sesgo es cero
4. puede seguir teniendo varianza alta.
**Supuestos:** Modelo de muestreo especificado. **Verificación:** La media muestral es insesgada bajo muestreo aleatorio apropiado ✔.

### 288 · ¿Qué relación hay entre varianza y desviación típica?
**R:** La desviación típica es la raíz cuadrada de la varianza.
**Razonamiento:**
1. La varianza promedia desviaciones al cuadrado
2. sus unidades también quedan al cuadrado
3. la raíz devuelve unidades originales.
**Supuestos:** Definiciones poblacional o muestral consistentes. **Verificación:** Varianza 25 unidades² implica desviación típica 5 unidades ✔.

### 289 · ¿Qué es una variable de confusión?
**R:** Una variable asociada a exposición y resultado que distorsiona la relación observada.
**Razonamiento:**
1. Puede influir en quién recibe exposición
2. también afecta al resultado
3. si no se controla puede crear o esconder asociación.
**Supuestos:** Modelo causal con una causa común relevante. **Verificación:** La edad puede asociarse al tratamiento y al pronóstico ✔.

### 290 · ¿Por qué correlación de Pearson cero no descarta toda dependencia?
**R:** Porque puede existir una relación no lineal.
**Razonamiento:**
1. Pearson mide asociación lineal
2. relaciones curvas pueden tener covarianza cero
3. dependencia no equivale a correlación lineal.
**Supuestos:** Variables con momentos finitos y modelo apropiado. **Verificación:** Si X es simétrica e Y=X², la correlación puede ser cero aunque Y dependa de X ✔.


## BLOQUE 30 — Problemas interdisciplinarios (291–300)

### 291 · Un depósito contiene 120 litros y pierde 3 litros por minuto. ¿Cuánto queda tras 15 minutos?
**R:** 75 litros.
**Razonamiento:**
1. Pérdida=3·15=45 litros
2. restar 45 a 120
3. quedan 75 litros.
**Supuestos:** Caudal constante y sin entradas. **Verificación:** 75+45=120 litros ✔.

### 292 · En un mapa a escala 1:50.000 hay 4 cm entre dos puntos. ¿Distancia real?
**R:** 2 km.
**Razonamiento:**
1. 4 cm representan 200.000 cm
2. convertir da 2.000 m
3. son 2 km.
**Supuestos:** Escala uniforme y medición correcta. **Verificación:** 2 km equivalen a 200.000 cm ✔.

### 293 · Una máquina produce 12 piezas por hora. ¿Cuánto tarda en producir 90 piezas?
**R:** 7,5 horas.
**Razonamiento:**
1. Tiempo=cantidad/tasa
2. 90/12=7,5
3. equivale a 7 horas y 30 minutos.
**Supuestos:** Ritmo constante, sin paradas ni merma. **Verificación:** 12·7,5=90 ✔.

### 294 · Una solución tiene 10 g de sal en 250 mL. ¿Concentración en g/L?
**R:** 40 g/L.
**Razonamiento:**
1. 250 mL son 0,25 L
2. concentración=10/0,25
3. resultado 40 g/L.
**Supuestos:** Volumen final de solución 250 mL. **Verificación:** 40·0,25=10 g ✔.

### 295 · Una población de 1.000 aumenta 10 % y luego disminuye 10 %. ¿Valor final?
**R:** 990.
**Razonamiento:**
1. Aumentar multiplica por 1,10 y da 1.100
2. reducir ese nuevo valor multiplica por 0,90
3. resultado 990.
**Supuestos:** Porcentajes sucesivos aplicados a bases distintas. **Verificación:** 1,10·0,90=0,99 ✔.

### 296 · Un objeto de 2 kg acelera a 3 m/s². ¿Fuerza neta?
**R:** 6 N.
**Razonamiento:**
1. Segunda ley F=ma
2. multiplicar 2 por 3
3. unidad kg·m/s² equivale a newton.
**Supuestos:** Masa constante y marco inercial. **Verificación:** 6 N/2 kg=3 m/s² ✔.

### 297 · ¿Cuántos bits hay en 3 bytes?
**R:** 24 bits.
**Razonamiento:**
1. Un byte contiene 8 bits
2. 3·8=24
3. se cancelan las unidades byte.
**Supuestos:** Byte definido como octeto. **Verificación:** 24/8=3 ✔.

### 298 · Una receta para 4 personas usa 300 g de arroz. ¿Cuánto para 10?
**R:** 750 g.
**Razonamiento:**
1. 300/4=75 g por persona
2. 75·10=750 g
3. la proporción se mantiene.
**Supuestos:** Raciones iguales y escalado lineal. **Verificación:** 750/10=75 g ✔.

### 299 · Un tren recorre 180 km en 2,5 horas. ¿Velocidad media?
**R:** 72 km/h.
**Razonamiento:**
1. Velocidad media=distancia/tiempo
2. 180/2,5=72
3. no implica velocidad constante en cada instante.
**Supuestos:** Tiempo total de viaje definido. **Verificación:** 72·2,5=180 ✔.

### 300 · Un sistema recibe 500 solicitudes y responde correctamente a 485. ¿Tasa de éxito?
**R:** 97 %.
**Razonamiento:**
1. Dividir 485 entre 500 da 0,97
2. multiplicar por 100 da 97 %
3. quedan 15 fallos.
**Supuestos:** Cada solicitud tiene resultado binario y se cuentan todas. **Verificación:** 485+15=500 ✔.


---

**Dataset Drosophila · ítems 001–300 completados.**
