import os
import csv
import subprocess
from itertools import combinations

def find_files(input_path, samples, extension="_variants.hdf5"):
    """Find the HDF5 files for the given samples in the input path."""
    sample_files = {}
    for sample in samples:
        file_path = os.path.join(input_path, sample + extension)
        if os.path.isfile(file_path):
            sample_files[sample] = file_path
        else:
            print(f"File not found for sample: {sample}")
    return sample_files

def compare_strains(input_path, output_path, csv_file):
    strains = {}
    
    # Read the CSV file and group samples by strain
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            strain = row['strain']
            sample = row['filename']  # Adjust 'filename' to match your column name
            if strain not in strains:
                strains[strain] = []
            strains[strain].append(sample)
    
    # Loop over strains and compare samples
    for strain, samples in strains.items():
        if len(samples) < 2:
            print(f"Not enough samples for strain {strain} to compare.")
            continue

        # Find corresponding HDF5 files
        sample_files = find_files(input_path, samples)
        
        # Get all pairwise combinations of samples
        sample_pairs = combinations(sample_files.items(), 2)
        
        # Combine results for the same strain into one summary and details output
        summary_output = os.path.join(output_path, f"{strain}_summary.tsv")
        details_output = os.path.join(output_path, f"{strain}_details.tsv")
        
        for (sample1, file1), (sample2, file2) in sample_pairs:
            print(f"Comparing {sample1} and {sample2} for strain {strain}...")
            summary_file = f"{sample1}.vs.{sample2}.summary.tsv"
            details_file = f"{sample1}.vs.{sample2}.details.tsv"
            
            # Run straingr compare command
            subprocess.run([
                "straingr", "compare", file1, file2, 
                "-o", summary_file, "-d", details_file
            ])
            
            # Append the result of each pairwise comparison into the combined files
            with open(summary_file, 'r') as sf, open(summary_output, 'a') as combined_summary:
                combined_summary.write(sf.read())
            with open(details_file, 'r') as df, open(details_output, 'a') as combined_details:
                combined_details.write(df.read())
            
            # Optionally remove individual summary and details files
            os.remove(summary_file)
            os.remove(details_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Compare strains using straingr.')
    parser.add_argument('-i', '--input_path', required=True, help='Input directory containing HDF5 files.')
    parser.add_argument('-o', '--output_path', required=True, help='Output directory for comparison results.')
    parser.add_argument('-c', '--csv_file', required=True, help='CSV file containing strain and sample information.')
    
    args = parser.parse_args()
    
    compare_strains(args.input_path, args.output_path, args.csv_file)