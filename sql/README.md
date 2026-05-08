# SQL Files

This folder contains the SQL-related files used for the TCGA Glioblastoma database project.

## Files included in this folder

### `01_create_tcga_gbm_tables.sql`

This script creates the final MySQL database schema. It includes the table definitions, primary keys, foreign keys, and relationships for the relational database.

The script creates the following tables:

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

### `05_neo4j_diff_exp.sql`

This file contains the Neo4j/Cypher code used to load the SQL-derived differentially expressed genes into Neo4j. The graph represents genes as `Gene` nodes and GBM expression subtypes as `Subtype` nodes. Genes are connected to the subtype where they show higher mean expression using a `HIGHER_IN` relationship.

## Large SQL file stored externally

The population SQL file was too large to upload directly to GitHub because it contains millions of insert rows.

The file is:

- `04_populate_tcga_gbm_tables.sql`

This script populates the MySQL database using the cleaned datasets and long-format mRNA/CNA files.

Access the large population SQL file here:

https://drive.google.com/file/d/1g_XJOyMmzJsOU5L8GDXTW5Ra1TGARh03/view?usp=drive_link

## Expected final row counts

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
