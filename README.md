# IBM SkillsBuild · AI Learning Portfolio

**Pablo Monserrat Sastre** · IA, prompt engineering y ciberseguridad

Portfolio de aprendizaje asociado al plan **IA y software development 2026** de IBM SkillsBuild, completado el **9 de octubre de 2026**, según el [certificado de finalización](certificate.pdf). Identificador del plan: `PLAN-F54A44FC16C3`.

## Origen y alcance

Los trabajos originales del curso no se conservan. Estos ejemplos se han reconstruido después de completar el plan, con ayuda de IA (Codex), a partir de los temas trabajados: clasificación, resúmenes, contexto, formato y fundamentos de ciberseguridad. No son entregas originales recuperadas ni proyectos oficiales de IBM. El certificado acredita la finalización del plan; no acredita estos ejemplos ni una certificación profesional independiente.

El código, los prompts y los datos se han preparado para este portfolio. No se han copiado proyectos de terceros. Las referencias oficiales sirven de consulta conceptual. IBM SkillsBuild e IBM Granite pertenecen a IBM; este repositorio no está afiliado a IBM.

## Proyectos

| Proyecto | Problema | Resultado de referencia |
|---|---|---|
| [Reseñas](projects/reviews) | Identificar sentimiento y aspectos sin confundir batería y envío | JSON con una clasificación por ID |
| [Reuniones](projects/meeting) | Resumir decisiones y extraer tres acciones | Responsables, fechas y preguntas abiertas |
| [Seguridad](projects/security) | Resumir un registro de autenticación | Hechos, incógnitas y recomendaciones separadas |

## Ejecutar localmente

Python 3.10 o superior. Solo biblioteca estándar: sin instalación de paquetes, credenciales o conexiones externas.

```bash
python portfolio.py build reviews
python portfolio.py build meeting
python portfolio.py build security
python portfolio.py demo reviews
python portfolio.py validate reviews projects/reviews/reference.json
python -m unittest discover -s tests -v
```

`build` genera un archivo de texto en `generated/` con las instrucciones y la entrada. Puedes pegarlo en un entorno de inferencia de tu elección, por ejemplo uno que permita usar IBM Granite. Selecciona un modelo disponible en ese entorno. Este programa **no ejecuta ningún modelo**.

`demo` muestra el resultado de referencia incluido y lo identifica explícitamente como tal. `validate` comprueba el JSON de una respuesta guardada y termina con código 1 si no cumple las reglas. Un resultado válido estructuralmente puede seguir siendo incorrecto en su contenido.

## Resultados y evaluación

Los archivos `reference.json` son ejemplos preparados con ayuda de IA, no salidas obtenidas de IBM Granite. No se han medido precisión, latencia ni mejoras entre modelos. Las pruebas verifican que el validador rechaza IDs omitidos, categorías inválidas, acciones incompletas y formatos incorrectos.

Para documentar una ejecución real, guarda el modelo y su versión, fecha, parámetros disponibles, prompt, respuesta y observaciones utilizando [la plantilla de evaluación](docs/evaluation.md). Compara cada afirmación con la entrada; no uses solo la validación del JSON como criterio de éxito.

## Conocimientos representados

- Definir tarea, público y contexto en una indicación.
- Especificar etiquetas y formatos de salida consistentes.
- Identificar temas recurrentes y preservar detalles relevantes.
- Separar decisiones, acciones e información no confirmada.
- Tratar instrucciones dentro de los datos como contenido no confiable.
- Validar resultados estructurados y documentar límites de evaluación.

## Referencias

- [IBM SkillsBuild](https://skillsbuild.org/): plataforma de aprendizaje.
- [IBM Granite: Prompt Engineering Guide](https://www.ibm.com/granite/docs/use-cases/prompt-engineering): guía conceptual de indicaciones (dirigida a Granite 4.0; no prueba qué versión se usó en el curso).
- [Guía oficial de Granite en GitHub](https://github.com/ibm-granite/granite-4.0-language-models/blob/main/Granite%204.0%20Prompt%20engineering%20guide%20v2.md): referencia; no se ha copiado su código ni sus ejemplos.

## Autor y licencia

Portfolio de **Pablo Monserrat Sastre**, preparado con asistencia de Codex. [LinkedIn](https://www.linkedin.com/in/pablo-monserrat-9a197b289/) · [GitHub](https://github.com/PabloMonserratSastre)

El código, los prompts y los datos ficticios originales de este repositorio se distribuyen bajo licencia MIT. El certificado y las marcas de terceros quedan excluidos de esa licencia.
