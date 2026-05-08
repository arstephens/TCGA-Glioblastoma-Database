# Script Execution Order

This document explains the order used to recreate the TCGA Glioblastoma MySQL database and Neo4j graph component.

The goal is for another person to be able to follow the workflow from the downloaded data files to the final populated database without guessing the order of scripts or SQL files.

---

## Step 1: Download the Data

Download the raw and cleaned datasets from the external links provided in:

- `data/raw/README.md`
- `data/cleaned/README.md`

Place the files into the expected local project folders before running the Python scripts.

The raw datasets are the original TCGA GBM files, while the cleaned datasets are the project-specific versions used for database loading.

---

## Step 2: Create the MySQL Schema

Open phpMyAdmin, create or select the project database, and run:

```text
sql/01_create_tcga_gbm_tables.sql
```

This creates the final database schema, including all tables, primary keys, foreign keys, and relationships.

The schema creates 13 tables:

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

---

## Step 3: Convert Matrix Files to Long Format

Run:

```bash
python "scripts/02_Converting Matrix to Long Format.py"
```

This converts the cleaned mRNA expression and copy-number alteration matrix files into long format.

The original mRNA and CNA files are matrix-style files, where genes are rows and samples are columns. The final MySQL database stores these values as one row per sample-gene pair, so the files need to be reshaped before loading.

Expected outputs:

- `long_tcga_gbm_mrna_expression.csv`
- `long_tcga_gbm_copy_number.csv`

These files are used to populate:

- `mrna_expression`
- `copy_number`

---

## Step 4: Generate the SQL Population File

Run:

```bash
python "scripts/03_Create SQL Table Population File.py"
```

This creates the large SQL population file:

```text
04_populate_tcga_gbm_tables.sql
```

This file contains the insert statements needed to populate the MySQL database tables.

Because the file is very large, it is stored externally and linked in:

```text
sql/README.md
```

The population script reads the cleaned datasets and generates insert statements for:

- `patient`
- `cancer_type`
- `sample`
- `gene`
- `mutation`
- `mutation_sample`
- `mutation_gene`
- `mrna_expression`
- `copy_number`
- `protein`
- `protein_quant`
- `protein_mutation`
- `sequencing_panel`

---

## Step 5: Populate the Database

Download the large population SQL file linked in:

```text
sql/README.md
```

Then import it into phpMyAdmin after the schema has been created.

The population file is:

```text
04_populate_tcga_gbm_tables.sql
```

After the import finishes, the database should contain all final tables and records.

---

## Step 6: Validate the Final Row Counts

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

A successful load should match these counts.

---

## Step 7: Load the Neo4j Component

The Neo4j portion of this project uses SQL-derived differential expression results from the MySQL database.

Each `Gene` node represents a candidate differentially expressed gene. Each `Subtype` node represents a GBM expression subtype, either Classical or Proneural. Each `HIGHER_IN` relationship connects a gene to the subtype where it had higher mean expression.

The graph structure is:

```text
(:Gene)-[:HIGHER_IN]->(:Subtype)
```

The CSV used for Neo4j loading is stored in the `neo4j/` folder:

```text
differentially_expressed_genes.csv
```

The Neo4j/Cypher script is stored in the `scripts/` folder:

```text
06_neo4j_cypher_visualization.txt
```

Run the Cypher script in Neo4j Browser to create the graph.

The graph visualization is stored in the `diagrams/` folder:

```text
Neo4j_diff_expressed_genes.png
```

---

## Summary of Run Order

1. Download raw and cleaned data from the linked external files.
2. Run `sql/01_create_tcga_gbm_tables.sql` in phpMyAdmin to create the schema.
3. Run `scripts/02_Converting Matrix to Long Format.py`.
4. Run `scripts/03_Create SQL Table Population File.py`.
5. Import `04_populate_tcga_gbm_tables.sql` into phpMyAdmin.
6. Validate the final row counts.
7. Run `scripts/06_neo4j_cypher_visualization.txt` in Neo4j Browser.

---
