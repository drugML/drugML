from scraper import Scraper
import csv


def read_file(file_path, names_list):
    f = open(file_path, mode='r', encoding='utf-8')
    try:
        for line in f:
            drug_name, CID = line.split(',')
            names_list.append([drug_name.lower().strip(), CID.lower().strip()])
    except Exception:
        print(Exception)


def get_drug_names_from_file(drugs_dont_work):
    read_file("files/drugs_that_dont_work.txt", drugs_dont_work)
    print(drugs_dont_work)


def scrape_drugs_work_property(drugs_work):
    # for each drug, instantiate a scraper instance
    for index, (drug_name, CID) in enumerate(drugs_work):
        drug = Scraper(drug_name, CID, True)
        raw_properties = drug.get_properties()
        drug.format_properties(raw_properties)
        # replace name with scraper instance
        drugs_work[index] = drug


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
    drugs_work = []
    drugs_dont_work = []
    # get all names from file to list
    get_drug_names_from_file(drugs_dont_work)
    # for all names, scrape its properties
    scrape_drugs_work_property(drugs_dont_work)
    # write all scraped data to csv
    write_to_csv(r'.\files\sample_data.csv', drugs_dont_work)


if __name__ == "__main__":
    main()
