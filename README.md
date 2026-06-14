### What I Learned

#### ETL Pipeline Concepts

Through this project, I gained a better understanding of how a modern ETL pipeline is structured:

* Data is extracted from a source system
* Data is transformed into a format suitable for analytics
* Processed data is loaded into a storage layer such as a data lake

#### Apache Airflow

Although Airflow was not fully implemented in this project, I researched and learned its role within a data engineering architecture.

Key concepts I learned include:

* Airflow is used to orchestrate workflows rather than perform heavy data processing
* Workflows are defined as DAGs (Directed Acyclic Graphs)
* Airflow can schedule and monitor ETL jobs
* Airflow commonly triggers external processing jobs such as Spark applications

#### PySpark

Through this project, I learned:

* Working with Spark DataFrames
* Reading and transforming CSV data
* Aggregating and filtering datasets
* Basic concepts of distributed data processing

One interesting insight was that Spark DataFrames initially felt similar to an ORM because of their API. However, Spark's main purpose is distributed computation, where data is partitioned and processed in parallel across multiple workers.

#### Amazon S3

Through this project, I learned:

* Uploading files to S3
* Using S3 as a simple data lake
* Organizing raw and processed datasets
* Separating storage from processing
