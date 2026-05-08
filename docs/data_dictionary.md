# Data Dictionary

This data dictionary describes the final MySQL tables created for the TCGA Glioblastoma database project. It includes each table, column name, data type, key status, and a short description of what the field represents.

## Table Overview

| Table | Description |
|---|---|
| `patient` | Stores patient-level demographic information. |
| `cancer_type` | Stores broad and detailed cancer type information. |
| `sample` | Stores sample-level clinical and molecular subtype information. |
| `gene` | Stores gene identifiers and gene annotation fields. |
| `mutation` | Stores mutation-level information. |
| `mutation_sample` | Bridge table connecting mutations to samples. |
| `mutation_gene` | Bridge table connecting mutations to genes. |
| `mrna_expression` | Stores long-format mRNA expression values by sample and gene. |
| `copy_number` | Stores long-format copy-number alteration values by sample and gene. |
| `protein` | Stores protein identifiers and their associated genes. |
| `protein_quant` | Stores RPPA protein expression values by sample and protein. |
| `protein_mutation` | Connects protein records to mutations and stores protein-change annotations. |
| `sequencing_panel` | Stores mutation and GISTIC/CNA panel information for each sample. |

---

# `patient`

The `patient` table stores one row per TCGA patient.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `patient_id` | `VARCHAR(20)` | Primary Key | Unique TCGA patient identifier. |
| `sex` | `VARCHAR(10)` |  | Patient sex. |

---

# `cancer_type`

The `cancer_type` table stores the cancer type information used to classify samples.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `cancer_type_id` | `INT` | Primary Key | Internal numeric identifier for the cancer type. |
| `cancer_type` | `VARCHAR(20)` |  | Broad cancer type label. |
| `cancer_type_detailed` | `VARCHAR(100)` |  | More detailed cancer type label. |

---

# `sample`

The `sample` table stores one row per TCGA sample and connects each sample to a patient and cancer type.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `sample_id` | `VARCHAR(20)` | Primary Key | Unique TCGA sample identifier. |
| `patient_id` | `VARCHAR(20)` | Foreign Key | Links each sample to the `patient` table. |
| `cancer_type_id` | `INT` | Foreign Key | Links each sample to the `cancer_type` table. |
| `patient_age` | `DECIMAL(4,1)` |  | Patient age associated with the sample. |
| `sample_type` | `VARCHAR(30)` |  | Type of sample, such as primary tumor. |
| `expression_subtype` | `VARCHAR(30)` |  | GBM expression subtype, such as Classical, Proneural, Mesenchymal, or G-CIMP. |
| `mgmt_status` | `VARCHAR(20)` |  | MGMT methylation status. |
| `methylation_status` | `VARCHAR(20)` |  | Methylation cluster/status annotation. |
| `g_cimp_methylation` | `VARCHAR(20)` |  | G-CIMP methylation status. |
| `idh1_mutation` | `VARCHAR(20)` |  | IDH1 mutation status. |
| `tmb_non_syn` | `DECIMAL(6,2)` |  | Tumor mutational burden based on nonsynonymous mutations. |
| `oncotree_code` | `VARCHAR(20)` |  | OncoTree cancer type code. |
| `os_status` | `VARCHAR(20)` |  | Overall survival status. |
| `os_months` | `DECIMAL(6,1)` |  | Overall survival time in months. |
| `dfs_status` | `VARCHAR(30)` |  | Disease-free survival status. |
| `dfs_months` | `DECIMAL(6,1)` |  | Disease-free survival time in months. |

---

# `gene`

The `gene` table stores gene-level identifiers and annotation fields.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `gene_id` | `INT` | Primary Key | Internal numeric identifier for each gene. |
| `hugo_symbol` | `VARCHAR(30)` |  | HUGO gene symbol. |
| `entrez_gene_id` | `INT` |  | Entrez Gene identifier, when available. |
| `chromosome` | `VARCHAR(5)` |  | Chromosome where the gene is located. |
| `gene_start_position` | `BIGINT` |  | Gene start position, when available. |
| `gene_end_position` | `BIGINT` |  | Gene end position, when available. |
| `cytoband` | `VARCHAR(30)` |  | Cytoband annotation, when available. |

---

# `mutation`

The `mutation` table stores mutation-level details. Sample and gene relationships are stored separately in bridge tables.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `mutation_id` | `INT` | Primary Key | Internal numeric identifier for each mutation. |
| `mutation_start_position` | `BIGINT` |  | Genomic start position of the mutation. |
| `mutation_end_position` | `BIGINT` |  | Genomic end position of the mutation. |
| `variant_classification` | `VARCHAR(50)` |  | Functional mutation classification, such as missense mutation or nonsense mutation. |
| `variant_type` | `VARCHAR(20)` |  | Variant type, such as SNP, INS, or DEL. |
| `reference_allele` | `VARCHAR(255)` |  | Reference allele. |
| `tumor_seq_allele2` | `VARCHAR(255)` |  | Tumor alternate allele. |
| `hgvsc` | `VARCHAR(255)` |  | Coding DNA HGVS annotation. |
| `hgvsp` | `VARCHAR(255)` |  | Protein HGVS annotation. |

---

# `mutation_sample`

The `mutation_sample` table is a bridge table connecting mutations to samples. This was used because the same mutation record may need to be connected to sample-level information without storing `sample_id` directly in the `mutation` table.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `mutation_sample_id` | `BIGINT` | Primary Key | Internal identifier for each mutation-sample relationship. |
| `mutation_id` | `INT` | Foreign Key | Links to the `mutation` table. |
| `sample_id` | `VARCHAR(20)` | Foreign Key | Links to the `sample` table. |

---

# `mutation_gene`

The `mutation_gene` table is a bridge table connecting mutations to genes.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `mutation_gene_id` | `BIGINT` | Primary Key | Internal identifier for each mutation-gene relationship. |
| `mutation_id` | `INT` | Foreign Key | Links to the `mutation` table. |
| `gene_id` | `INT` | Foreign Key | Links to the `gene` table. |

---

# `mrna_expression`

The `mrna_expression` table stores long-format mRNA expression data. Each row represents one expression value for one sample-gene pair.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `expression_id` | `BIGINT` | Primary Key | Internal identifier for each mRNA expression record. |
| `sample_id` | `VARCHAR(20)` | Foreign Key | Links the expression value to a sample. |
| `gene_id` | `INT` | Foreign Key | Links the expression value to a gene. |
| `expression_value_mrna` | `DECIMAL(12,4)` |  | mRNA expression value. |

---

# `copy_number`

The `copy_number` table stores long-format copy-number alteration data. Each row represents one copy-number value for one sample-gene pair.

The final design uses `gene_id` instead of `mutation_id` because the CNA dataset is gene-based, not mutation-based.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `cna_id` | `BIGINT` | Primary Key | Internal identifier for each copy-number record. |
| `sample_id` | `VARCHAR(20)` | Foreign Key | Links the copy-number value to a sample. |
| `gene_id` | `INT` | Foreign Key | Links the copy-number value to a gene. |
| `copy_number_value` | `INT` |  | Copy-number alteration value. |

---

# `protein`

The `protein` table stores protein records and links each protein to a gene.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `protein_id` | `INT` | Primary Key | Internal numeric identifier for each protein. |
| `gene_id` | `INT` | Foreign Key | Links the protein to the `gene` table. |
| `protein_label` | `VARCHAR(100)` |  | Protein or antibody label. |

---

# `protein_quant`

The `protein_quant` table stores RPPA protein expression values. Each row represents one protein expression value for one sample-protein pair.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `protein_quant_id` | `BIGINT` | Primary Key | Internal identifier for each protein expression record. |
| `sample_id` | `VARCHAR(20)` | Foreign Key | Links the protein expression value to a sample. |
| `protein_id` | `INT` | Foreign Key | Links the protein expression value to a protein. |
| `expression_value_quant` | `DECIMAL(12,4)` |  | RPPA protein expression value. |

---

# `protein_mutation`

The `protein_mutation` table connects proteins to mutations and stores protein-level change information.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `protein_mutation_id` | `BIGINT` | Primary Key | Internal identifier for each protein-mutation relationship. |
| `protein_id` | `INT` | Foreign Key | Links to the `protein` table. |
| `mutation_id` | `INT` | Foreign Key | Links to the `mutation` table. |
| `protein_change` | `VARCHAR(255)` |  | Protein-level mutation/change annotation. |

---

# `sequencing_panel`

The `sequencing_panel` table stores whether each sample was profiled for mutation and GISTIC/CNA data.

| Column | Data Type | Key | Description |
|---|---|---|---|
| `sample_id` | `VARCHAR(20)` | Primary Key / Foreign Key | Links sequencing panel information to the `sample` table. |
| `mutation_panel` | `VARCHAR(10)` |  | Indicates whether mutation data were profiled for the sample. |
| `gistic_panel` | `VARCHAR(10)` |  | Indicates whether GISTIC/CNA data were profiled for the sample. |

---

# Neo4j Graph Data

The Neo4j component uses the file:

- `neo4j/differentially_expressed_genes.csv`

This file contains SQL-derived candidate differentially expressed genes comparing Classical and Proneural GBM samples.

## Neo4j Node and Relationship Types

| Type | Name | Description |
|---|---|---|
| Node | `Gene` | Candidate differentially expressed gene. |
| Node | `Subtype` | GBM expression subtype, either Classical or Proneural. |
| Relationship | `HIGHER_IN` | Connects a gene to the subtype where it had higher mean expression. |

## Neo4j Graph Structure

```text
(:Gene)-[:HIGHER_IN]->(:Subtype)
```
