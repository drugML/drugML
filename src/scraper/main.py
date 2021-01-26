from scraper import Scraper
from pathlib import Path
import csv

scraper_dir = Path("files/")

def read_file(file_path, names_list):
    f = open(file_path, mode='r', encoding='utf-8')
    try:
        for line in f:
            drug_name, CID = line.split(',')
            names_list.append([drug_name.lower().strip(), CID.lower().strip()])
    except Exception:
        print(Exception)


def get_drug_names_from_file(drugs_list):
    file = scraper_dir / "scrape_targets.txt";
    read_file(file, drugs_list)
    print(drugs_list)


def scrape_drugs_list_property(drugs_list):
    # for each drug, instantiate a scraper instance
    for index, (drug_name, CID) in enumerate(drugs_list):
        drug = Scraper(drug_name, CID, True)
        raw_properties = drug.get_properties()
        drug.format_properties(raw_properties)
        # replace name with scraper instance
        drugs_list[index] = drug


def write_to_csv(file_path, drugs):
    field_names = [
        'name',
        'cid',
        'weight',
        'hydro_bond_donor_count',
        'hydro_bond_acceptor_count',
        'topo_polar_surface_area',
        'heavy_atom_count',
        'formal_charge',
        'complexity',
        'melting_pt',
        'boiling_pt',
        'solubility',
        'logP',
        'density',
        'pH',
        'pKa',
        'dissociation_const',
        'collision_cross_sec',
        'work'
    ]

    result_data = []
    for drug in drugs:
        result_data.append(drug.properties)

    with open(file_path, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(result_data)


def main():
    
    drugs_list = []
    # get all names from file to list
    get_drug_names_from_file(drugs_list)
    # for all names, scrape its properties
    scrape_drugs_list_property(drugs_list)
    # write all scraped data to csv
    out_file = scraper_dir / "scraped_data.csv"
    write_to_csv(out_file, drugs_list)


if __name__ == "__main__":
    main()
