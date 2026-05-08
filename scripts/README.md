# Scripts

This folder contains the Python and Neo4j/Cypher scripts used to transform the cleaned TCGA Glioblastoma datasets and prepare files for the final MySQL and Neo4j databases.

The scripts are numbered in the order they should be used.

## Files in this folder

### `02_Converting Matrix to Long Format.py`

This script converts the mRNA expression and copy-number alteration matrix files into long format.

The original mRNA and CNA files were structured as matrices, with genes as rows and TCGA samples as columns. Since the final MySQL database stores expression and copy-number values as one row per sample-gene pair, these files had to be reshaped before loading.

Expected outputs:

- `long_tcga_gbm_mrna_expression.csv`
- `long_tcga_gbm_copy_number.csv`

These long-format files are used to populate:

- `mrna_expression`
- `copy_number`

---

### `03_Create SQL Table Population File.py`

This script reads the cleaned datasets and generates the large SQL population script used to insert data into the final MySQL database.

The generated SQL file is:

- `04_populate_tcga_gbm_tables.sql`

This file was too large to upload directly to GitHub, so it is stored externally and linked in the `sql/README.md` file.

This script prepares insert statements for the final database tables, including:

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

### `06_neo4j_cypher_visualization.txt`

This file contains the Neo4j/Cypher code used to load SQL-derived differentially expressed genes into Neo4j.

The Neo4j graph represents:

```text
(:Gene)-[:HIGHER_IN]->(:Subtype)

## Neo4j Graph Details

Each `Gene` node represents a candidate differentially expressed gene identified from the MySQL database. Each `Subtype` node represents a GBM expression subtype, either Classical or Proneural. The `HIGHER_IN` relationship connects each gene to the subtype where it had higher mean expression.

The CSV loaded into Neo4j is stored in the `neo4j/` folder:

- `differentially_expressed_genes.csv`

## Notes

The raw and cleaned datasets are not stored directly in GitHub because several files exceed GitHub upload limits. Links to the external data files are provided in the `data/raw/README.md` and `data/cleaned/README.md` files.

The full SQL population file is also stored externally.
