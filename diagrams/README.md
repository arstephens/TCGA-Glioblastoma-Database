# Diagrams

This folder contains the diagrams and visual outputs used to document the TCGA Glioblastoma database project. These figures help explain the final database design, the relational table structure in MySQL/phpMyAdmin, and the Neo4j graph visualization.

## Files in this folder

### `5_NF_Diagram.png`

This diagram shows the normalized database design used for the final MySQL database.

It includes the main entities/tables, primary keys, foreign keys, and relationships between tables. The model separates patient, sample, gene, mutation, expression, copy number, protein, and sequencing panel information into related tables.

---

### `SQL Table Structure.png`

This image shows the final table structure as displayed in phpMyAdmin Designer after the tables were created and populated.

It is included to show how the schema was implemented in MySQL, including the final table names, fields, primary keys, and foreign key connections. This view provides a database level confirmation that the SQL schema matches the intended relational design.

---

### `Neo4j_diff_expressed_genes.png`

This image shows the Neo4j graph visualization created from SQL gotten candidate differentially expressed genes.

The graph structure is:

```text
(:Gene)-[:HIGHER_IN]->(:Subtype)
```
