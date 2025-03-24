**Informe: Ejercicio de RAG básico**

Implementé un RAG básico que cumple con los siguientes requisitos:
- Chunking del documento `boe.md` usando la función `chunker`.
- Generación de embeddings con la API de OpenAI (`get_embedding`).
- Almacenamiento de chunks y embeddings en una base de datos SQLite (`populate_embeddings`).
- Búsqueda de chunks relevantes con embeddings (`query_embeddings`).
- Creación de un prompt con contexto, pregunta e instrucción.
- Respuesta al usuario mediante argumentos de línea de comandos.
- Extras: tamaño de chunks y solapamiento modificables, cacheo de embeddings, ingesta de múltiples documentos.

**Pruebas con diferentes tamaños de chunk:**

1. **Consulta**: "Qué dice el anuncio de licitación sobre el Suministro de Gases Medicinales?"
   - `chunk-size 500, overlap 200`: "El anuncio de licitación sobre el Suministro de Gases Medicinales indica que es realizado por la Jefatura de Asuntos Económicos del Mando de Apoyo Logístico y que el objeto de la licitación es el Suministro de Gases Medicinales."
   - `chunk-size 1000, overlap 400`: "El anuncio de licitación sobre el Suministro de Gases Medicinales indica que es para la Jefatura de Asuntos Económicos del Mando de Apoyo Logístico y tiene el expediente 2024/ETSAE0906/00004351E."
   - `chunk-size 2000, overlap 800`: "El anuncio de licitación sobre el Suministro de Gases Medicinales indica que es para la Jefatura de Asuntos Económicos del Mando de Apoyo Logístico y el expediente es 2024/ETSAE0906/00004351E."
   - **Conclusión**: El `chunk-size` de 1000 con un `overlap` de 400 dio los mejores resultados, ya que incluye toda la información relevante (entidad, objeto, y expediente) sin perder contexto.

2. **Consulta**: "Qué dice el anuncio de licitación sobre el Acuerdo Marco para el Mantenimiento Integral de las Instalaciones para los Centros Deportivos y Residencias de la DIAPER?"
   - `chunk-size 2000, overlap 800`: "El anuncio de licitación menciona que se está llevando a cabo un Acuerdo Marco para el Mantenimiento Integral de las instalaciones para los Centros Deportivos y Residencias de la DIAPER."
   - **Nota**: No se realizaron pruebas con otros tamaños de chunk para esta consulta.

3. **Consulta**: "Cuáles son los nuevos precios de los gases licuados del petróleo?"
   - `chunk-size 2000, overlap 800`: "Los nuevos precios de los gases licuados del petróleo por canalización se publicaron en la Resolución de 11 de marzo de 2025 de la Dirección General de Política Energética y Minas. No está disponible información específica sobre los precios en este fragmento."
   - **Conclusión**: La respuesta identifica la resolución, pero no proporciona los precios específicos, posiblemente porque no están en el documento o no se extrajeron correctamente.

**Notas**:
- No encontré "Artículo 1" en el BOE `BOE-S-2025-65.pdf`, ya que parece estar compuesto principalmente por anuncios de licitación y formalización de contratos (sección "BOE-B").
- El script funcionó correctamente para consultas relevantes al contenido del documento.
- Subí el trabajo a mi repositorio personal en GitHub: `https://github.com/Maurosg78/AI-generativa`.