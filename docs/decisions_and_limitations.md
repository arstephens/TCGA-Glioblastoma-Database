# Decisions and Limitations

This file summarizes the main design decisions, cleaning decisions, assumptions, and limitations for the TCGA Glioblastoma database project.

---

## Major Design Decisions

### 1. Separating patient and sample data

The database separates patient level and sample level data into two tables:

- `patient`
- `sample`

This was done because a patient and a tumor sample are related, but they are not the same entity. Patient level information, such as `patient_id` and `sex`, belong in the `patient` table. Sample level information, such as `sample_id`, expression subtype, cancer type, methylation status, IDH1 mutation status, and survival related annotations, belongs in the `sample` table.

This makes the database easier to expand if a patient has more than one sample.

---

### 2. Creating a separate cancer type table

Cancer type information was moved into a separate `cancer_type` table.

Even though this project only uses TCGA Glioblastoma data, separating cancer type decreases repeated text in the `sample` table and makes the design more normalized. It also makes the schema easier to add to if more cancer types are added in the future.

The relationship is:

```text
cancer_type → sample
```

---

### 3. Using a central gene table

A central `gene` table was created because gene information appears in several datasets, including:

- mutation data
- mRNA expression data
- copy number alteration data
- RPPA/protein data

The `gene` table stores identifiers and annotations such as HUGO symbol, Entrez gene ID, chromosome, start position, end position, and cytoband.

This avoids repeating gene information across every molecular table.

---

### 4. Removing `sample_id` from the mutation table

The final `mutation` table does not directly store `sample_id`.

Instead, the database uses a bridge table:

```text
mutation_sample
```

This was an important design change. If `sample_id` stayed directly in the `mutation` table, the same mutation appearing in two samples could be treated as two unrelated mutation records. The bridge table makes the relationship between mutations and samples more flexible and better normalized.

The relationship is:

```text
mutation → mutation_sample → sample
```

---

### 5. Creating a mutation gene bridge table

The final database includes:

```text
mutation_gene
```

This bridge table connects mutations to genes.

This was added because mutation and gene information should not be forced into one table. A mutation is its own event or record, and a gene is a separate biological thing. The bridge table keeps those concepts connected without mixing them together.

The relationship is:

```text
mutation → mutation_gene → gene
```

---

### 6. Making the copy number table gene based

The `copy_number` table originally included `mutation_id`, but this was changed to `gene_id`.

This was one of the most important corrections in the project. The copy number alteration file is gene based, not mutation based. Each copy number value is associated with a sample and gene. It is not tied to one specific mutation.

The final relationship is:

```text
sample → copy_number ← gene
```

This better matches the original CNA dataset and avoids creating a relationship that does not really exist in the source data.

---

### 7. Converting mRNA and CNA files to long format

The mRNA expression and copy number files were originally matrix style files. Genes were rows, and samples were columns.

That format works for data analysis, but it is not ideal for a relational database. The final database stores one measurement per row.

The long format structure is:

```text
sample_id | gene_id | value
```

This was used for:

- `mrna_expression`
- `copy_number`

This makes SQL queries much easier and avoids creating hundreds of sample columns.

---

### 8. Separating protein expression from protein mutation information

Protein related data were split into:

- `protein`
- `protein_quant`
- `protein_mutation`

This was done because protein expression values and protein mutation annotations describe different things.

The `protein` table defines the protein. The `protein_quant` table stores RPPA protein expression values by sample and protein. The `protein_mutation` table connects proteins to mutations and stores protein change annotations.

---

### 9. Keeping sequencing panel information separate

The `sequencing_panel` table stores mutation and GISTIC/CNA panel information for each sample.

This information is connected to `sample` using `sample_id`.

The relationship is one to one because each sample has one row of panel information.

---

## Cleaning Decisions

### Column standardization

Column names were cleaned and standardized so they could be used more easily in Python and SQL. This helped avoid problems with spaces, inconsistent capitalization, and special characters.

### Missing values

Missing values were kept as `NULL` where appropriate. I did not try to fill in missing biological or clinical values because that could introduce incorrect information.

For example, some gene annotation fields such as cytoband or genomic start/end positions were missing for some genes. These were left as `NULL`.

### Removing unnecessary fields

Fields that were not used in the final database design were removed from the cleaned files. For example, therapy related information was not included because therapy can vary over time and was not standardized enough for this project.

### Keeping source identifiers

TCGA patient IDs, TCGA sample IDs, HUGO symbols, and Entrez gene IDs were kept because they are important for connecting tables and tracing records back to the source files.

---

## Normalization Decisions

The final database was designed to reduce repeated data and separate entities logically.

Examples of normalization choices include:

- patient information is separate from sample information
- cancer type information is separated from sample records
- gene information is stored once in the `gene` table
- mutation sample relationships are stored in `mutation_sample`
- mutation gene relationships are stored in `mutation_gene`
- expression and copy number data are stored in long format
- protein definitions are separated from protein expression values

This design makes the database easier to query and reduces unnecessary repeated information.

---

## Deviations or Practical Compromises

### Surrogate keys in large molecular tables

Some large molecular tables use surrogate primary keys, such as:

- `expression_id`
- `cna_id`
- `protein_quant_id`

For some of these tables, a composite key such as `(sample_id, gene_id)` or `(sample_id, protein_id)` could also identify a row. However, surrogate keys made the SQL creation and loading process more consistent across the database.

### Sample table contains several annotation fields

The `sample` table includes multiple clinical and molecular annotation information, such as expression subtype, methylation status, IDH1 mutation status, TMB, and survival fields.

These could theoretically be separated into more lookup or reference tables, but they were kept in `sample` because they directly describe the sample and are easier to query together for this project.

### Large files stored externally

Several raw, cleaned, and SQL files were too large to upload directly to GitHub. These files are stored externally using Google Docs and linked in the repository.

This is not ideal compared to storing everything in one place, but it keeps the GitHub repository readable and avoids file size problems.

---

## Neo4j Decisions

The Neo4j part of the project used SQL gotten differential expression results.

The graph structure is:

```text
(:Gene)-[:HIGHER_IN]->(:Subtype)
```

Each `Gene` node represents a candidate differentially expressed gene. Each `Subtype` node represents either Classical or Proneural GBM. The `HIGHER_IN` relationship connects a gene to the subtype where it had higher mean expression.

The Neo4j graph was kept simple on purpose. It was meant to show how SQL results from the relational database could be represented as a graph.

---

## Limitations

### SQL based differential expression is exploratory

The differential expression step was based on SQL calculated mean expression differences and log2 fold change between Classical and Proneural GBM samples.

This is useful for exploring the database and creating the Neo4j graph, but it is not the same as formal RNA seq differential expression analysis. A more complete analysis would use a tool like DESeq2 and include statistical testing, dispersion estimation, and multiple testing correction.

### External file links need to stay active

The raw data, cleaned data, SQL population file, and database dump are stored externally because they are too large for GitHub. This means the Google Drive/Google Doc links need to remain active for the project to stay fully reproducible.

### Some source data were incomplete

Some records had missing annotation values. These were kept as `NULL` instead of being guessed or filled in manually.

### Database performance was not heavily optimized

The project focused mainly on correct design and reproducibility. Additional indexing could improve query performance, especially for the large `copy_number` and `mrna_expression` tables.

---

## Future Improvements

Possible future improvements include:

- adding formal RNA-seq differential expression analysis with DESeq2
- adding more indexes for faster queries
- creating SQL views for common analysis questions
- expanding the Neo4j graph to include mutations, proteins, and copy number alterations
- adding example SQL queries to show how the database can be used
- creating a smaller test dataset so the full workflow can be run quickly without using the large files

---

## Summary

The final database design balances normalization, biology, and practical usability. The main goal was to make the TCGA GBM data easier to query and reproduce while keeping the relationships between patients, samples, genes, mutations, expression values, copy number values, and protein measurements clear.

The biggest design changes were creating bridge tables for mutation relationships, making the copy number table gene based, converting matrix files to long format, and separating protein definitions from protein measurements and mutation related protein changes.
