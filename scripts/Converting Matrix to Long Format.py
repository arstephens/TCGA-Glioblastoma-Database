import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# File paths
# ------------------------------------------------------------

# Input files: cleaned wide-format datasets
MRNA_INPUT = "C:\\Users\\avast\\Downloads\\Georgetown\\2nd Semester\\Databases\\Project\\data after cleaning\\cleaned_tcga_gbm_mrna_seq_v2_rsem.csv"
CNA_INPUT = "C:\\Users\\avast\\Downloads\\Georgetown\\2nd Semester\\Databases\\Project\\data after cleaning\\cleaned_tcga_gbm_cna.csv"

# Output files: SQL-ready long-format datasets
MRNA_OUTPUT = "long_tcga_gbm_mrna_expression.csv"
CNA_OUTPUT = "long_tcga_gbm_copy_number.csv"


# ------------------------------------------------------------
# Helper function to clean column names
# ------------------------------------------------------------

def clean_column_names(df):
    """
    Standardizes column names by stripping extra spaces.
    This avoids problems caused by accidental leading/trailing spaces.
    """
    df.columns = [str(col).strip() for col in df.columns]
    return df


# ------------------------------------------------------------
# Convert mRNA expression dataset to long format
# ------------------------------------------------------------

def convert_mrna_to_long(input_file, output_file):
    print("Reading mRNA dataset...")

    mrna = pd.read_csv(input_file)
    mrna = clean_column_names(mrna)

    # These columns describe the gene and should stay fixed
    gene_id_cols = ["hugo_symbol", "entrez_gene_id"]

    # Check that the required columns exist
    missing_cols = [col for col in gene_id_cols if col not in mrna.columns]
    if missing_cols:
        raise ValueError(f"Missing required mRNA columns: {missing_cols}")

    # All other columns are sample IDs
    sample_cols = [col for col in mrna.columns if col not in gene_id_cols]

    print(f"mRNA genes: {mrna.shape[0]}")
    print(f"mRNA samples: {len(sample_cols)}")

    # Convert from wide format to long format
    mrna_long = mrna.melt(
        id_vars=gene_id_cols,
        value_vars=sample_cols,
        var_name="sample_id",
        value_name="expression_value_mrna"
    )

    # Remove rows where the expression value is missing
    mrna_long = mrna_long.dropna(subset=["expression_value_mrna"])

    # Make sure expression values are numeric
    mrna_long["expression_value_mrna"] = pd.to_numeric(
        mrna_long["expression_value_mrna"],
        errors="coerce"
    )

    # Drop any rows that could not be converted to numeric
    mrna_long = mrna_long.dropna(subset=["expression_value_mrna"])

    # Reorder columns for SQL staging table
    mrna_long = mrna_long[
        ["sample_id", "hugo_symbol", "entrez_gene_id", "expression_value_mrna"]
    ]

    print(f"Long mRNA rows: {mrna_long.shape[0]}")

    # Save long-format file
    mrna_long.to_csv(output_file, index=False)

    print(f"Saved long mRNA file to: {output_file}")


# ------------------------------------------------------------
# Convert CNA dataset to long format
# ------------------------------------------------------------

def convert_cna_to_long(input_file, output_file):
    print("Reading CNA dataset...")

    cna = pd.read_csv(input_file)
    cna = clean_column_names(cna)

    # These columns describe the gene and should stay fixed
    gene_id_cols = ["hugo_symbol", "entrez_gene_id", "cytoband"]

    # Check that the required columns exist
    missing_cols = [col for col in gene_id_cols if col not in cna.columns]
    if missing_cols:
        raise ValueError(f"Missing required CNA columns: {missing_cols}")

    # All other columns are sample IDs
    sample_cols = [col for col in cna.columns if col not in gene_id_cols]

    print(f"CNA genes: {cna.shape[0]}")
    print(f"CNA samples: {len(sample_cols)}")

    # Convert from wide format to long format
    cna_long = cna.melt(
        id_vars=gene_id_cols,
        value_vars=sample_cols,
        var_name="sample_id",
        value_name="copy_number_value"
    )

    # Remove rows where the CNA value is missing
    cna_long = cna_long.dropna(subset=["copy_number_value"])

    # Make sure CNA values are integers
    cna_long["copy_number_value"] = pd.to_numeric(
        cna_long["copy_number_value"],
        errors="coerce"
    )

    # Drop any rows that could not be converted to numeric
    cna_long = cna_long.dropna(subset=["copy_number_value"])

    # Convert to integer because copy number calls are whole-number values
    cna_long["copy_number_value"] = cna_long["copy_number_value"].astype(int)

    # Reorder columns for SQL staging table
    cna_long = cna_long[
        ["sample_id", "hugo_symbol", "entrez_gene_id", "cytoband", "copy_number_value"]
    ]

    print(f"Long CNA rows: {cna_long.shape[0]}")

    # Save long-format file
    cna_long.to_csv(output_file, index=False)

    print(f"Saved long CNA file to: {output_file}")


# ------------------------------------------------------------
# Run both conversions
# ------------------------------------------------------------

def main():
    # Make sure the input files exist before running
    for file in [MRNA_INPUT, CNA_INPUT]:
        if not Path(file).exists():
            raise FileNotFoundError(f"Could not find input file: {file}")

    convert_mrna_to_long(MRNA_INPUT, MRNA_OUTPUT)
    print("-" * 60)
    convert_cna_to_long(CNA_INPUT, CNA_OUTPUT)

    print("-" * 60)
    print("Done! Both files were converted to long format.")


if __name__ == "__main__":
    main()