# Cleaned Data

The cleaned TCGA GBM datasets used for this project are too large to upload directly to GitHub. They are stored externally in a Google Doc/Drive file.

Access the cleaned dataset files here:
https://docs.google.com/document/d/1UmlQnHtHhn24xLaU92spzt-SlTrk_7da/edit?usp=drive_link&ouid=108918527268617875724&rtpof=true&sd=true

The cleaned data includes:
- cleaned clinical patient data
- cleaned clinical sample data
- cleaned mutation data
- cleaned mRNA expression data
- cleaned copy-number alteration data
- cleaned RPPA protein expression data
- cleaned gene panel matrix data
- long-format mRNA expression file
- long-format copy-number file

These cleaned files were generated from the raw TCGA GBM datasets using the cleaning and transformation scripts in the `scripts/` folder. They were used to create the final MySQL database tables.

The long-format mRNA and copy-number files were used to populate the normalized `mrna_expression` and `copy_number` tables in the final relational database.
