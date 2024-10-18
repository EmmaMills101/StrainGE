# StrainGE
This Python script facilitates the pairwise comparison of genomic strains using the straingr tool. It automates the process of comparing samples from different strains, consolidating the results into summary and detailed reports for each strain. The script identifies input files based on sample names and performs comparisons between all combinations of samples within each strain group.

**Features**
Automated Strain Comparison: Finds corresponding HDF5 files for samples and runs pairwise comparisons between samples of the same reference strain.
Batch Processing: Supports multiple strains and samples from a CSV file, and processes all comparisons in a single execution.
Consolidated Output: Produces combined summary and detailed result files for each strain, aggregating all pairwise comparisons.

**Usage:**
python straingr_compare.py -i <input_path> -o <output_path> -c <csv_file>
-i, --input_path: Directory containing the all HDF5 files from your analysis these sound be labeled as sample_variants.hdf5.
-o, --output_path: Directory for storing comparison results.
-c, --csv_file: CSV file specifying reference strains and their associated samples.

**Requirements:**
Python 3.x
strainge installed and available in the system path. This script assumes you have run all the strainge commands, until straingr compare
CSV file format: Must contain columns for "strain" and "filename". "filename" are the input sample names. "strain" are the references identified by straingst in each sample.
The value in "filename" must match that of the sample_variants.hdf5 input file. 
For example, value of DVT1015 in "filename" will pull the DVT1015_variant.hdf5 file from input directory containing all the HDF5 files 


