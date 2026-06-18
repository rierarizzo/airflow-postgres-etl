# Ejercicio 1: ETL Local (NYC Green Taxi)

**Repositorio:** `airflow-postgres-etl`  
**Nivel:** Básico  
**Tecnologías:** Apache Airflow, Docker, PostgreSQL, Pandas, Python.

## Objetivo General
Construir un Grafo Acíclico Dirigido (DAG) en Apache Airflow que orqueste la extracción, transformación (limpieza) y persistencia de datos públicos de viajes de taxis en una base de datos local.

---

## Requerimientos del Pipeline

### 1. Configuración del DAG
- **Frecuencia:** Programado para ejecutarse diariamente (`@daily`).
- **Comportamiento Histórico:** La ejecución retroactiva (`catchup`) debe estar desactivada para evitar sobrecargar el entorno local.
- **Tolerancia a Fallos:** Configurar un reintento automático (`retries`) con un tiempo de espera de entre 2 y 5 minutos entre intentos.

### 2. Tarea de Extracción (Download)
- **Objetivo:** Obtener el conjunto de datos crudo.
- **Acción:** Descargar el archivo Parquet de viajes de *Green Taxi* (ej. enero de 2024) desde el sitio web oficial de NYC TLC.
- **Destino:** Guardar el archivo en el directorio local mapeado en Docker (usualmente `/opt/airflow/`) para que las tareas posteriores puedan consumirlo.

### 3. Tarea de Transformación (Clean)
- **Objetivo:** Aplicar reglas de calidad de datos mediante código nativo de Python usando `pandas`.
- **Reglas de Negocio:**
  1. Filtrar el dataset para mantener únicamente los registros donde la cantidad de pasajeros (`passenger_count`) sea mayor a cero.
  2. Descartar cualquier registro que contenga valores nulos en las columnas de facturación: `total_amount` y `fare_amount`.
- **Salida:** Exportar el dataframe resultante a un nuevo archivo Parquet temporal.

### 4. Tarea de Preparación de Infraestructura (Create Table)
- **Objetivo:** Garantizar que la tabla destino exista en la base de datos antes de la carga.
- **Acción:** Ejecutar una sentencia SQL DDL (`CREATE TABLE IF NOT EXISTS`) en PostgreSQL utilizando la conexión preconfigurada en Airflow.
- **Esquema:** Las columnas de la tabla deben coincidir con la estructura del archivo Parquet procesado.

### 5. Tarea de Carga (Load)
- **Objetivo:** Persistir los datos limpios en la base de datos relacional.
- **Acción:** Leer el archivo Parquet temporal e insertar todos sus registros en la tabla creada en el paso anterior.
- **Comportamiento:** La operación de inserción debe ser de tipo *append* (agregar datos, no sobrescribir).

### 6. Orquestación y Dependencias
El flujo debe respetar una secuencia lógica y estricta. Ninguna tarea puede iniciar si la anterior no ha finalizado exitosamente.
> **Secuencia obligatoria:** Descarga ➔ Limpieza ➔ Creación de Tabla ➔ Carga.