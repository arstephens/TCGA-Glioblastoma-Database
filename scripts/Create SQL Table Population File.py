import pandas as pd
from pathlib import Path

# ============================================================
# TCGA GBM DATABASE PROJECT
# Generate SQL INSERT statements from cleaned files
#
# Updated version:
# 1. copy_number is gene-based, not mutation-based
# 2. protein table includes proteins from both mutation and RPPA files
# ============================================================

DATA_DIR = Path(
    r"C:\Users\avast\Downloads\Georgetown\2nd Semester\Databases\Project\data for sql"
)

OUTPUT_SQL = DATA_DIR / "02_populate_tcga_gbm_tables.sql"


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def find_file(file_stem):
    """
    Finds a file in DATA_DIR even if the extension is .xlsx, .xls, or .csv.
    """
    possible_extensions = [".xlsx", ".xls", ".csv"]

    for ext in possible_extensions:
        file_path = DATA_DIR / f"{file_stem}{ext}"
        if file_path.exists():
            return file_path

    raise FileNotFoundError(
        f"Could not find {file_stem} with .xlsx, .xls, or .csv extension in:\n{DATA_DIR}"
    )


def clean_column_names(df):
    """
    Standardizes column names so they match the SQL table fields.
    """
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace(".", "_", regex=False)
    )
    return df


def read_excel_sheet(file_stem, sheet_name):
    """
    Reads a specific sheet from an Excel workbook.
    """
    file_path = find_file(file_stem)

    if file_path.suffix.lower() == ".csv":
        return clean_column_names(pd.read_csv(file_path, low_memory=False))

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except ValueError:
        excel_file = pd.ExcelFile(file_path)
        raise ValueError(
            f"\nSheet '{sheet_name}' was not found in {file_path.name}.\n"
            f"Available sheets are: {excel_file.sheet_names}\n"
        )

    return clean_column_names(df)


def read_csv_or_excel_first_sheet(file_stem):
    """
    Reads a CSV file or the first sheet of an Excel file.
    Used for long-format mRNA and CNA files.
    """
    file_path = find_file(file_stem)

    if file_path.suffix.lower() == ".csv":
        return clean_column_names(pd.read_csv(file_path, low_memory=False))

    return clean_column_names(pd.read_excel(file_path))


def keep_existing_columns(df, columns, table_name):
    """
    Keeps only the columns needed for a SQL table.
    Gives a clear error if a needed column is missing.
    """
    missing = [col for col in columns if col not in df.columns]

    if missing:
        raise KeyError(
            f"\nMissing columns for {table_name}: {missing}\n"
            f"Available columns are:\n{list(df.columns)}\n"
        )

    return df[columns].copy()


def sql_value(value):
    """
    Converts Python/pandas values into SQL-safe values.
    """
    if pd.isna(value):
        return "NULL"

    if isinstance(value, str):
        value = value.strip()

        if value == "":
            return "NULL"

        # Escape single quotes for SQL
        value = value.replace("'", "''")
        return f"'{value}'"

    return str(value)


def write_insert_batches(sql_file, table_name, df, batch_size=500):
    """
    Writes INSERT INTO statements in batches.
    This keeps the basic INSERT INTO ... VALUES format from class,
    but makes the SQL file smaller and faster to run.
    """
    df = df.drop_duplicates().copy()

    if df.empty:
        sql_file.write(f"-- No rows to insert into {table_name}\n\n")
        return

    columns = list(df.columns)
    col_text = ", ".join(columns)

    for start in range(0, len(df), batch_size):
        batch = df.iloc[start:start + batch_size]

        sql_file.write(f"INSERT INTO {table_name} ({col_text}) VALUES\n")

        value_lines = []
        for _, row in batch.iterrows():
            values = [sql_value(row[col]) for col in columns]
            value_lines.append(f"({', '.join(values)})")

        sql_file.write(",\n".join(value_lines))
        sql_file.write(";\n\n")


# ------------------------------------------------------------
# Read cleaned Excel sheets and long CSV files
# ------------------------------------------------------------

print("Reading cleaned files...")

patient = read_excel_sheet(
    "cleaned_tcga_gbm_clinical_patient",
    "patient_clean"
)

clinical_patient = read_excel_sheet(
    "cleaned_tcga_gbm_clinical_patient",
    "clinical_patient_clean"
)

cancer_type = read_excel_sheet(
    "cleaned_tcga_gbm_clinical_sample",
    "cancer_type_clean"
)

sample = read_excel_sheet(
    "cleaned_tcga_gbm_clinical_sample",
    "sample_clean"
)

gene = read_excel_sheet(
    "cleaned_tcga_gbm_mutations",
    "gene_clean"
)

mutation = read_excel_sheet(
    "cleaned_tcga_gbm_mutations",
    "mutation_clean"
)

mutation_sample = read_excel_sheet(
    "cleaned_tcga_gbm_mutations",
    "mutation_sample_clean"
)

mutation_gene = read_excel_sheet(
    "cleaned_tcga_gbm_mutations",
    "mutation_gene_clean"
)

# Protein records can come from both the mutation file and the RPPA file.
# This is important because protein_quant uses RPPA protein IDs.
protein_mutation_source = read_excel_sheet(
    "cleaned_tcga_gbm_mutations",
    "protein_clean"
)

protein_rppa_source = read_excel_sheet(
    "cleaned_tcga_gbm_rppa",
    "protein_clean"
)

protein = pd.concat(
    [protein_mutation_source, protein_rppa_source],
    ignore_index=True
)

protein_mutation = read_excel_sheet(
    "cleaned_tcga_gbm_mutations",
    "protein_mutation_clean"
)

rppa = read_excel_sheet(
    "cleaned_tcga_gbm_rppa",
    "rppa_expression_clean"
)

gene_panel = read_excel_sheet(
    "cleaned_tcga_gbm_gene_panel_matrix",
    "sample_gene_panel_clean"
)

mrna_long = read_csv_or_excel_first_sheet(
    "long_tcga_gbm_mrna_expression"
)

cna_long = read_csv_or_excel_first_sheet(
    "long_tcga_gbm_copy_number"
)


# ------------------------------------------------------------
# Prepare final table data
# These columns must match your MySQL tables.
# ------------------------------------------------------------

print("Preparing final table data...")

# -----------------------------
# patient
# -----------------------------

patient_final = keep_existing_columns(
    patient,
    ["patient_id", "sex"],
    "patient"
).drop_duplicates()


# -----------------------------
# cancer_type
# -----------------------------

cancer_type_final = keep_existing_columns(
    cancer_type,
    ["cancer_type_id", "cancer_type", "cancer_type_detailed"],
    "cancer_type"
).drop_duplicates()


# -----------------------------
# sample
# -----------------------------
# The sample table includes patient age and survival columns.
# Those are merged in from clinical_patient_clean using patient_id.

sample_final = sample.merge(
    clinical_patient[
        [
            "patient_id",
            "patient_age",
            "os_status",
            "os_months",
            "dfs_status",
            "dfs_months"
        ]
    ],
    on="patient_id",
    how="left"
)

sample_final = keep_existing_columns(
    sample_final,
    [
        "sample_id",
        "patient_id",
        "cancer_type_id",
        "patient_age",
        "sample_type",
        "expression_subtype",
        "mgmt_status",
        "methylation_status",
        "g_cimp_methylation",
        "idh1_mutation",
        "tmb_non_syn",
        "oncotree_code",
        "os_status",
        "os_months",
        "dfs_status",
        "dfs_months"
    ],
    "sample"
).drop_duplicates()


# -----------------------------
# gene
# -----------------------------

gene_final = keep_existing_columns(
    gene,
    [
        "gene_id",
        "hugo_symbol",
        "entrez_gene_id",
        "chromosome",
        "gene_start_position",
        "gene_end_position",
        "cytoband"
    ],
    "gene"
).drop_duplicates(subset=["gene_id"])


# -----------------------------
# mutation
# -----------------------------

mutation_final = keep_existing_columns(
    mutation,
    [
        "mutation_id",
        "mutation_start_position",
        "mutation_end_position",
        "variant_classification",
        "variant_type",
        "reference_allele",
        "tumor_seq_allele2",
        "hgvsc",
        "hgvsp"
    ],
    "mutation"
).drop_duplicates(subset=["mutation_id"])


# -----------------------------
# mutation_sample
# -----------------------------

mutation_sample_final = keep_existing_columns(
    mutation_sample,
    [
        "mutation_sample_id",
        "mutation_id",
        "sample_id"
    ],
    "mutation_sample"
).drop_duplicates(subset=["mutation_sample_id"])


# -----------------------------
# mutation_gene
# -----------------------------

mutation_gene_final = keep_existing_columns(
    mutation_gene,
    [
        "mutation_gene_id",
        "mutation_id",
        "gene_id"
    ],
    "mutation_gene"
).drop_duplicates(subset=["mutation_gene_id"])


# -----------------------------
# protein
# -----------------------------
# Updated:
# protein_final now combines protein_clean from the mutations workbook
# and protein_clean from the RPPA workbook. This prevents protein_quant
# rows from pointing to protein IDs that do not exist.

protein_final = keep_existing_columns(
    protein,
    [
        "protein_id",
        "gene_id",
        "protein_label"
    ],
    "protein"
).drop_duplicates(subset=["protein_id"])


# -----------------------------
# protein_mutation
# -----------------------------

protein_mutation_final = keep_existing_columns(
    protein_mutation,
    [
        "protein_mutation_id",
        "protein_id",
        "mutation_id",
        "protein_change"
    ],
    "protein_mutation"
).drop_duplicates(subset=["protein_mutation_id"])


# -----------------------------
# protein_quant
# -----------------------------
# Your cleaned RPPA file may use rppa_id and rppa_value.
# Rename those columns to match the MySQL protein_quant table.

rppa = rppa.rename(
    columns={
        "rppa_id": "protein_quant_id",
        "rppa_value": "expression_value_quant"
    }
)

protein_quant_final = keep_existing_columns(
    rppa,
    [
        "protein_quant_id",
        "sample_id",
        "protein_id",
        "expression_value_quant"
    ],
    "protein_quant"
).drop_duplicates(subset=["protein_quant_id"])


# -----------------------------
# sequencing_panel
# -----------------------------
# Your cleaned gene panel file may use mutation_profiled and gistic_profiled.
# Rename those columns to match the MySQL sequencing_panel table.

gene_panel = gene_panel.rename(
    columns={
        "mutation_profiled": "mutation_panel",
        "gistic_profiled": "gistic_panel"
    }
)

sequencing_panel_final = keep_existing_columns(
    gene_panel,
    [
        "sample_id",
        "mutation_panel",
        "gistic_panel"
    ],
    "sequencing_panel"
).drop_duplicates(subset=["sample_id"])


# -----------------------------
# mrna_expression
# -----------------------------
# The long mRNA file has entrez_gene_id.
# The SQL table uses gene_id, so we merge to get gene_id.

mrna_long = mrna_long.rename(
    columns={
        "expression_value": "expression_value_mrna",
        "mrna_value": "expression_value_mrna"
    }
)

# Make IDs numeric so the merge works consistently.
mrna_long["entrez_gene_id"] = pd.to_numeric(
    mrna_long["entrez_gene_id"],
    errors="coerce"
)

gene_final["entrez_gene_id"] = pd.to_numeric(
    gene_final["entrez_gene_id"],
    errors="coerce"
)

# Make a unique lookup so the merge does not accidentally duplicate rows.
gene_lookup = gene_final[
    [
        "gene_id",
        "entrez_gene_id"
    ]
].dropna(subset=["entrez_gene_id"])

gene_lookup = gene_lookup.drop_duplicates(subset=["entrez_gene_id"])

mrna_final = mrna_long.merge(
    gene_lookup,
    on="entrez_gene_id",
    how="left"
)

mrna_final = keep_existing_columns(
    mrna_final,
    [
        "sample_id",
        "gene_id",
        "expression_value_mrna"
    ],
    "mrna_expression"
)

mrna_final = mrna_final.dropna(
    subset=[
        "sample_id",
        "gene_id",
        "expression_value_mrna"
    ]
).drop_duplicates()

mrna_final["gene_id"] = mrna_final["gene_id"].astype(int)


# -----------------------------
# copy_number
# -----------------------------
# Updated:
# The copy_number table is now gene-based.
#
# Long CNA file:
# sample_id, hugo_symbol, entrez_gene_id, cytoband, copy_number_value
#
# SQL copy_number table:
# cna_id AUTO_INCREMENT
# sample_id
# gene_id
# copy_number_value
#
# We do NOT insert cna_id because MySQL auto-generates it.

cna_long = cna_long.rename(
    columns={
        "expression_value": "copy_number_value",
        "cna_value": "copy_number_value"
    }
)

cna_long["entrez_gene_id"] = pd.to_numeric(
    cna_long["entrez_gene_id"],
    errors="coerce"
)

# Use the same unique lookup created above.
copy_number_final = cna_long.merge(
    gene_lookup,
    on="entrez_gene_id",
    how="left"
)

copy_number_final = keep_existing_columns(
    copy_number_final,
    [
        "sample_id",
        "gene_id",
        "copy_number_value"
    ],
    "copy_number"
)

copy_number_final = copy_number_final.dropna(
    subset=[
        "sample_id",
        "gene_id",
        "copy_number_value"
    ]
).drop_duplicates()

copy_number_final["gene_id"] = copy_number_final["gene_id"].astype(int)


# ------------------------------------------------------------
# Optional relationship checks before writing SQL
# These print warnings if a child table contains IDs missing from parent tables.
# ------------------------------------------------------------

print("Checking relationships before writing SQL...")

protein_ids = set(protein_final["protein_id"])
bad_protein_quant = protein_quant_final[
    ~protein_quant_final["protein_id"].isin(protein_ids)
]

if len(bad_protein_quant) > 0:
    print(
        f"WARNING: {len(bad_protein_quant)} protein_quant rows have protein_id values "
        f"that are not in the protein table."
    )
else:
    print("protein_quant protein_id check passed.")


gene_ids = set(gene_final["gene_id"])
bad_mrna = mrna_final[
    ~mrna_final["gene_id"].isin(gene_ids)
]

bad_cna = copy_number_final[
    ~copy_number_final["gene_id"].isin(gene_ids)
]

if len(bad_mrna) > 0:
    print(f"WARNING: {len(bad_mrna)} mrna_expression rows have gene_id values missing from gene.")
else:
    print("mrna_expression gene_id check passed.")

if len(bad_cna) > 0:
    print(f"WARNING: {len(bad_cna)} copy_number rows have gene_id values missing from gene.")
else:
    print("copy_number gene_id check passed.")


sample_ids = set(sample_final["sample_id"])

for table_name, df in [
    ("mutation_sample", mutation_sample_final),
    ("mrna_expression", mrna_final),
    ("copy_number", copy_number_final),
    ("protein_quant", protein_quant_final),
    ("sequencing_panel", sequencing_panel_final)
]:
    if "sample_id" in df.columns:
        bad_rows = df[~df["sample_id"].isin(sample_ids)]
        if len(bad_rows) > 0:
            print(f"WARNING: {len(bad_rows)} rows in {table_name} have sample_id values missing from sample.")
        else:
            print(f"{table_name} sample_id check passed.")


# ------------------------------------------------------------
# Write SQL file
# ------------------------------------------------------------

print("Writing SQL file...")

with open(OUTPUT_SQL, "w", encoding="utf-8") as sql_file:
    sql_file.write("-- TCGA GBM Database Project\n")
    sql_file.write("-- Populate tables using cleaned data\n")
    sql_file.write("-- Run after the table creation SQL script\n")
    sql_file.write("-- Updated version: copy_number uses gene_id, not mutation_id\n")
    sql_file.write("-- Updated version: protein table includes RPPA proteins\n\n")

    sql_file.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

    # Parent tables first
    write_insert_batches(sql_file, "patient", patient_final)
    write_insert_batches(sql_file, "cancer_type", cancer_type_final)
    write_insert_batches(sql_file, "sample", sample_final)
    write_insert_batches(sql_file, "gene", gene_final)
    write_insert_batches(sql_file, "mutation", mutation_final)
    write_insert_batches(sql_file, "protein", protein_final)

    # Bridge / child tables
    write_insert_batches(sql_file, "mutation_sample", mutation_sample_final)
    write_insert_batches(sql_file, "mutation_gene", mutation_gene_final)
    write_insert_batches(sql_file, "mrna_expression", mrna_final)
    write_insert_batches(sql_file, "copy_number", copy_number_final)
    write_insert_batches(sql_file, "protein_quant", protein_quant_final)
    write_insert_batches(sql_file, "protein_mutation", protein_mutation_final)
    write_insert_batches(sql_file, "sequencing_panel", sequencing_panel_final)

    sql_file.write("SET FOREIGN_KEY_CHECKS = 1;\n")


# ------------------------------------------------------------
# Print counts so you can check before importing into phpMyAdmin
# ------------------------------------------------------------

print("Done!")
print(f"Created SQL file: {OUTPUT_SQL}")

print("\nRows written by table:")
print(f"patient: {len(patient_final)}")
print(f"cancer_type: {len(cancer_type_final)}")
print(f"sample: {len(sample_final)}")
print(f"gene: {len(gene_final)}")
print(f"mutation: {len(mutation_final)}")
print(f"protein: {len(protein_final)}")
print(f"mutation_sample: {len(mutation_sample_final)}")
print(f"mutation_gene: {len(mutation_gene_final)}")
print(f"mrna_expression: {len(mrna_final)}")
print(f"copy_number: {len(copy_number_final)}")
print(f"protein_quant: {len(protein_quant_final)}")
print(f"protein_mutation: {len(protein_mutation_final)}")
print(f"sequencing_panel: {len(sequencing_panel_final)}")