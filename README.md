# TCGA Glioblastoma Database Project

## Project Summary

This project builds a reproducible MySQL database using TCGA Glioblastoma Multiforme data from cBioPortal. The database integrates clinical patient data, clinical sample data, mutation data, mRNA expression, copy-number alteration data, RPPA protein expression data, and sequencing panel information. The goal of this project was to organize the original multi-file cancer genomics dataset into a cleaner relational database that can be queried across patients, samples, genes, mutations, expression values, copy-number values, and protein measurements.

The project also includes a small Neo4j component. SQL was used to identify candidate differentially expressed genes between Classical and Proneural GBM samples, and those results were loaded into Neo4j so the relationship between genes and GBM subtype could be visualized as a graph.

## Repository Link

[TCGA-Glioblastoma-Database](https://github.com/arstephens/TCGA-Glioblastoma-Database)

## Tools and Technologies

- MySQL
- phpMyAdmin
- Python
- pandas
- openpyxl
- Neo4j
- Cypher
- GitHub
- Google Drive for large external files
- ER diagramming / phpMyAdmin Designer

## Repository Structure

```text
TCGA-Glioblastoma-Database/
├── README.md
├── data/
│   ├── raw/
│   └── cleaned/
├── diagrams/
├── docs/
├── neo4j/
├── scripts/
└── sql/
```

## Folder Descriptions

### `data/`

The `data/` folder contains links to the raw and cleaned datasets used in this project.

Because several data files were too large to upload directly to GitHub, the actual raw and cleaned files are stored externally and linked through README files.

- [`data/raw/`](data/raw/) contains the link to the raw TCGA GBM datasets.
- [`data/cleaned/`](data/cleaned/) contains the link to the cleaned datasets and long-format files used for database loading.

### `diagrams/`

The `diagrams/` folder contains the visual documentation for the database and graph components.

Files included:

- [`5_NF_Diagram.png`](diagrams/5_NF_Diagram.png): normalized database design/ER diagram
- [`SQL Table Structure.png`](diagrams/SQL%20Table%20Structure.png): phpMyAdmin table structure view
- [`Neo4j_diff_expressed_genes.png`](diagrams/Neo4j_diff_expressed_genes.png): Neo4j graph visualization of differentially expressed genes
- [`README.md`](diagrams/README.md): explanation of each diagram

### `docs/`

The `docs/` folder contains the main project documentation.

Files included:

- `project_writeup.pdf`: full project write-up
- `data_dictionary.md`: table and column definitions
- `script_execution_order.md`: order for running scripts and SQL files
- `decisions_and_limitations.md`: major design decisions, assumptions, and limitations

These documents explain the data cleaning process, database model, design decisions, relationships, constraints, reproducibility steps, and limitations of the project.

### `neo4j/`

The `neo4j/` folder contains the CSV file used for the Neo4j graph component.

File included:

- [`differentially_expressed_genes.csv`](neo4j/differentially_expressed_genes.csv)

This file was created from a SQL query that compared mean mRNA expression between Classical and Proneural GBM samples.

### `scripts/`

The `scripts/` folder contains the Python and Neo4j/Cypher scripts used in the workflow.

Files included:

- [`02_Converting Matrix to Long Format.py`](scripts/02_Converting%20Matrix%20to%20Long%20Format.py)
- [`03_Create SQL Table Population File.py`](scripts/03_Create%20SQL%20Table%20Population%20File.py)
- [`06_neo4j_cypher_visualization.txt`](scripts/06_neo4j_cypher_visualization.txt)
- [`README.md`](scripts/README.md)

These scripts convert the matrix-style mRNA and CNA files into long format, generate the SQL population file, and load the differential expression results into Neo4j.

### `sql/`

The `sql/` folder contains the SQL and Cypher-related files used to create and support the database.

Files included:

- [`01_create_tcga_gbm_tables.sql`](sql/01_create_tcga_gbm_tables.sql)
- [`05_neo4j_diff_exp.sql`](sql/05_neo4j_diff_exp.sql)
- [`README.md`](sql/README.md)

The large SQL population file, `04_populate_tcga_gbm_tables.sql`, was too large to upload directly to GitHub because it contains millions of insert rows. It is stored externally and linked in [`sql/README.md`](sql/README.md).

## Data Sources

The data used in this project come from the TCGA Glioblastoma Multiforme study available through cBioPortal.

The project uses seven main data sources:

- clinical patient data
- clinical sample data
- mutation data
- mRNA expression data
- copy-number alteration data
- RPPA protein expression data
- gene panel matrix data

The raw and cleaned data files are linked externally because several files exceed GitHub upload limits.

- Raw data access: [`data/raw/README.md`](data/raw/README.md)
- Cleaned data access: [`data/cleaned/README.md`](data/cleaned/README.md)

## Database Design Overview

The final MySQL database contains 13 tables:

- `patient`
- `cancer_type`
- `sample`
- `gene`
- `mutation`
- `mutation_sample`
- `mutation_gene`
- `copy_number`
- `mrna_expression`
- `protein`
- `protein_quant`
- `protein_mutation`
- `sequencing_panel`

The database was designed to separate major biological and clinical entities into related tables. Patient-level information is stored separately from sample-level information, and molecular measurements are stored in separate expression, copy-number, mutation, and protein tables.

Bridge tables were used where the data had many-to-many relationships. For example, `mutation_sample` connects mutations to samples, and `mutation_gene` connects mutations to genes.

## MySQL Database Tables

| Table | Description |
|---|---|
| `patient` | Stores patient-level identifiers and sex |
| `cancer_type` | Stores cancer type and detailed cancer type information |
| `sample` | Stores sample-level clinical and molecular subtype information |
| `gene` | Stores gene identifiers and gene annotation fields |
| `mutation` | Stores mutation-level information |
| `mutation_sample` | Bridge table connecting mutations to samples |
| `mutation_gene` | Bridge table connecting mutations to genes |
| `mrna_expression` | Stores long-format mRNA expression values by sample and gene |
| `copy_number` | Stores long-format copy-number values by sample and gene |
| `protein` | Stores protein identifiers and linked gene IDs |
| `protein_quant` | Stores RPPA protein expression values by sample and protein |
| `protein_mutation` | Connects protein records to mutations and stores protein-change annotations |
| `sequencing_panel` | Stores mutation and GISTIC/CNA panel information for each sample |

## How to Recreate the MySQL Database

### Software Requirements

To recreate the database, install or use:

- Python 3
- pandas
- openpyxl
- MySQL
- phpMyAdmin or another MySQL client
- Neo4j, if recreating the graph component

Python packages:

```bash
pip install pandas openpyxl
```

### Step 1: Download the data

Download the raw and cleaned datasets from the external links provided in:

- [`data/raw/README.md`](data/raw/README.md)
- [`data/cleaned/README.md`](data/cleaned/README.md)

Place the files into the expected local project folders before running the Python scripts.

### Step 2: Create the MySQL schema

Open phpMyAdmin, create or select the project database, and run:

```text
sql/01_create_tcga_gbm_tables.sql
```

This creates the final database schema, including all tables, primary keys, foreign keys, and relationships.

### Step 3: Convert matrix files to long format

Run:

```bash
python "scripts/02_Converting Matrix to Long Format.py"
```

This converts the cleaned mRNA expression and copy-number alteration matrix files into long format.

Expected outputs:

- `long_tcga_gbm_mrna_expression.csv`
- `long_tcga_gbm_copy_number.csv`

### Step 4: Generate the SQL population file

Run:

```bash
python "scripts/03_Create SQL Table Population File.py"
```

This creates the large SQL population file:

```text
04_populate_tcga_gbm_tables.sql
```

This file contains the insert statements needed to populate the MySQL database tables. Because the file is very large, it is stored externally and linked in [`sql/README.md`](sql/README.md).

### Step 5: Populate the database

Download the large population SQL file linked in [`sql/README.md`](sql/README.md), then import it into phpMyAdmin after the schema has been created.

The population file is:

```text
04_populate_tcga_gbm_tables.sql
```

### Step 6: Validate the final row counts

After importing the population SQL file, the final database should contain the following row counts.

| Table | Expected rows |
|---|---:|
| `cancer_type` | 1 |
| `copy_number` | 2,499,863 |
| `gene` | 8,237 |
| `mrna_expression` | 727,725 |
| `mutation` | 16,090 |
| `mutation_gene` | 16,090 |
| `mutation_sample` | 16,325 |
| `patient` | 577 |
| `protein` | 7,667 |
| `protein_mutation` | 13,771 |
| `protein_quant` | 33,003 |
| `sample` | 577 |
| `sequencing_panel` | 577 |

The expected total is 3,340,503 rows across 13 tables.

## Neo4j Component

The Neo4j portion of this project uses SQL-derived differential expression results from the MySQL database.

Each `Gene` node represents a candidate differentially expressed gene. Each `Subtype` node represents a GBM expression subtype, either `Classical` or `Proneural`. Each `HIGHER_IN` relationship connects a gene to the subtype where it had higher mean expression.

The graph structure is:

```text
(:Gene)-[:HIGHER_IN]->(:Subtype)
```

The CSV used for Neo4j loading is stored in the `neo4j/` folder:

- [`differentially_expressed_genes.csv`](neo4j/differentially_expressed_genes.csv)

The Neo4j/Cypher script is stored in the `scripts/` folder:

- [`06_neo4j_cypher_visualization.txt`](scripts/06_neo4j_cypher_visualization.txt)

The graph visualization is stored in the `diagrams/` folder:

- [`Neo4j_diff_expressed_genes.png`](diagrams/Neo4j_diff_expressed_genes.png)

## Documentation and Diagrams

Project documentation is stored in the `docs/` folder.

Documentation files:

- `project_writeup.pdf`
- `data_dictionary.md`
- `script_execution_order.md`
- `decisions_and_limitations.md`

Diagram files are stored in the `diagrams/` folder:

- [`5_NF_Diagram.png`](diagrams/5_NF_Diagram.png)
- [`SQL Table Structure.png`](diagrams/SQL%20Table%20Structure.png)
- [`Neo4j_diff_expressed_genes.png`](diagrams/Neo4j_diff_expressed_genes.png)

## Large File Notes

Several raw, cleaned, and generated SQL files exceed GitHub upload limits. To keep the repository clean and usable, large files are stored externally through linked Google Drive/Google Doc resources.

The repository still includes:

- schema creation SQL
- Python transformation scripts
- Neo4j/Cypher script
- diagram files
- documentation files
- links to external raw and cleaned data
- instructions to recreate the database from scratch

This structure keeps the project reproducible without making the GitHub repository difficult to use.

## Use of AI Assistance

ChatGPT was used as a support tool during parts of the dataset cleaning, database design, SQL generation, and documentation process. All final decisions about the database structure, cleaned files, SQL scripts, and project documentation were reviewed and implemented as part of this project.

A link to the ChatGPT conversation used during development is included in `docs/project_writeup.pdf`.

## Project Status

The MySQL database was successfully created and populated in phpMyAdmin. The final populated database contains 13 tables and 3,340,503 total rows. The Neo4j graph component was also created successfully using SQL-derived differential expression results.

## Author

Ava Stephens  
Master of Science in Bioinformatics  
Georgetown University
