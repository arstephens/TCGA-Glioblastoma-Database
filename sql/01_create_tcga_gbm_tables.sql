SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE patient (
    patient_id VARCHAR(20) NOT NULL,
    sex VARCHAR(10),

    PRIMARY KEY (patient_id)
);


CREATE TABLE cancer_type (
    cancer_type_id INT NOT NULL AUTO_INCREMENT,
    cancer_type VARCHAR(20),
    cancer_type_detailed VARCHAR(100),

    PRIMARY KEY (cancer_type_id)
);


CREATE TABLE sample (
    sample_id VARCHAR(20) NOT NULL,
    patient_id VARCHAR(20) NOT NULL,
    cancer_type_id INT,
    patient_age DECIMAL(4,1),
    sample_type VARCHAR(30),
    expression_subtype VARCHAR(30),
    mgmt_status VARCHAR(20),
    methylation_status VARCHAR(20),
    g_cimp_methylation VARCHAR(20),
    idh1_mutation VARCHAR(20),
    tmb_non_syn DECIMAL(6,2),
    oncotree_code VARCHAR(20),
    os_status VARCHAR(20),
    os_months DECIMAL(6,1),
    dfs_status VARCHAR(30),
    dfs_months DECIMAL(6,1),

    PRIMARY KEY (sample_id),

    FOREIGN KEY (patient_id)
        REFERENCES patient(patient_id),

    FOREIGN KEY (cancer_type_id)
        REFERENCES cancer_type(cancer_type_id)
);


CREATE TABLE gene (
    gene_id INT NOT NULL AUTO_INCREMENT,
    hugo_symbol VARCHAR(30),
    entrez_gene_id INT,
    chromosome VARCHAR(5),
    gene_start_position BIGINT,
    gene_end_position BIGINT,
    cytoband VARCHAR(30),

    PRIMARY KEY (gene_id)
);


CREATE TABLE mutation (
    mutation_id INT NOT NULL AUTO_INCREMENT,
    mutation_start_position BIGINT,
    mutation_end_position BIGINT,
    variant_classification VARCHAR(50),
    variant_type VARCHAR(20),
    reference_allele VARCHAR(255),
    tumor_seq_allele2 VARCHAR(255),
    hgvsc VARCHAR(255),
    hgvsp VARCHAR(255),

    PRIMARY KEY (mutation_id)
);


CREATE TABLE mutation_sample (
    mutation_sample_id BIGINT NOT NULL AUTO_INCREMENT,
    mutation_id INT NOT NULL,
    sample_id VARCHAR(20) NOT NULL,

    PRIMARY KEY (mutation_sample_id),

    FOREIGN KEY (mutation_id)
        REFERENCES mutation(mutation_id),

    FOREIGN KEY (sample_id)
        REFERENCES sample(sample_id)
);


CREATE TABLE mutation_gene (
    mutation_gene_id BIGINT NOT NULL AUTO_INCREMENT,
    mutation_id INT NOT NULL,
    gene_id INT NOT NULL,

    PRIMARY KEY (mutation_gene_id),

    FOREIGN KEY (mutation_id)
        REFERENCES mutation(mutation_id),

    FOREIGN KEY (gene_id)
        REFERENCES gene(gene_id)
);


CREATE TABLE copy_number (
    cna_id BIGINT NOT NULL AUTO_INCREMENT,
    sample_id VARCHAR(20) NOT NULL,
    gene_id INT NOT NULL,
    copy_number_value INT,

    PRIMARY KEY (cna_id),

    FOREIGN KEY (sample_id)
        REFERENCES sample(sample_id),

    FOREIGN KEY (gene_id)
        REFERENCES gene(gene_id)
);


CREATE TABLE mrna_expression (
    expression_id BIGINT NOT NULL AUTO_INCREMENT,
    sample_id VARCHAR(20) NOT NULL,
    gene_id INT NOT NULL,
    expression_value_mrna DECIMAL(12,4),

    PRIMARY KEY (expression_id),

    FOREIGN KEY (sample_id)
        REFERENCES sample(sample_id),

    FOREIGN KEY (gene_id)
        REFERENCES gene(gene_id)
);


CREATE TABLE protein (
    protein_id INT NOT NULL AUTO_INCREMENT,
    gene_id INT NOT NULL,
    protein_label VARCHAR(100),

    PRIMARY KEY (protein_id),

    FOREIGN KEY (gene_id)
        REFERENCES gene(gene_id)
);


CREATE TABLE protein_quant (
    protein_quant_id BIGINT NOT NULL AUTO_INCREMENT,
    sample_id VARCHAR(20) NOT NULL,
    protein_id INT NOT NULL,
    expression_value_quant DECIMAL(12,4),

    PRIMARY KEY (protein_quant_id),

    FOREIGN KEY (sample_id)
        REFERENCES sample(sample_id),

    FOREIGN KEY (protein_id)
        REFERENCES protein(protein_id)
);


CREATE TABLE protein_mutation (
    protein_mutation_id BIGINT NOT NULL AUTO_INCREMENT,
    protein_id INT NOT NULL,
    mutation_id INT NOT NULL,
    protein_change VARCHAR(255),

    PRIMARY KEY (protein_mutation_id),

    FOREIGN KEY (protein_id)
        REFERENCES protein(protein_id),

    FOREIGN KEY (mutation_id)
        REFERENCES mutation(mutation_id)
);


CREATE TABLE sequencing_panel (
    sample_id VARCHAR(20) NOT NULL,
    mutation_panel VARCHAR(10),
    gistic_panel VARCHAR(10),

    PRIMARY KEY (sample_id),

    FOREIGN KEY (sample_id)
        REFERENCES sample(sample_id)
);