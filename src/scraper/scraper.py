from requests import get
import json


PUBG_CHEM_URL = "https://pubchem.ncbi.nlm.nih.gov"
PUBG_CHEM_JSON_URL = f"{PUBG_CHEM_URL}/rest/pug_view/data/compound"


class Scraper:
    def __init__(self, drug_name, CID, is_good):
        self.name = drug_name
        self.cid = CID
        self.URL = f"{PUBG_CHEM_JSON_URL}/{self.cid}/JSON/?response_type=save&response_basename=compound_CID_{self.cid}"
        self.properties = {
            'name': self.name,
            'cid': self.cid,
            'weight': None,
            'hydro_bond_donor_count': None,
            'hydro_bond_acceptor_count': None,
            'topo_polar_surface_area': None,
            'heavy_atom_count': None,
            'formal_charge': None,
            'complexity': None,
            'melting_pt': None,
            'boiling_pt': None,
            'solubility': None,
            'logP': None,
            'density': None,
            'pH': None,
            'pKa': None,
            'dissociation_const': None,
            'collision_cross_sec': None,
            'work': is_good
        }

    def get_properties(self):
        response = get(self.URL)
        properties = json.loads(response.text)

        computed_properties = {}
        exp_properties = {}

        sections = properties.get("Record").get("Section")
        for section in sections:
            if section.get("TOCHeading") == "Chemical and Physical Properties":

                try:
                    if section['Section'][0]['TOCHeading'] == 'Computed Properties':
                        computed_properties = section['Section'][0]['Section']

                    if section['Section'][1]['TOCHeading'] == 'Experimental Properties':
                        exp_properties = section['Section'][1]['Section']
                except IndexError:
                    print(self.URL)

        properties = [computed_properties, exp_properties]

        return properties

    def format_properties(self, properties):
        # computed properties
        for property_obj in properties[0]:
            if property_obj['TOCHeading'] == 'Molecular Weight':
                try:
                    self.properties['weight'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'Hydrogen Bond Donor Count':
                try:
                    self.properties['hydro_bond_donor_count'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'Hydrogen Bond Acceptor Count':
                try:
                    self.properties['hydro_bond_acceptor_count'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'Topological Polar Surface Area':
                try:
                    self.properties['topo_polar_surface_area'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'Heavy Atom Count':
                try:
                    self.properties['heavy_atom_count'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'Formal Charge':
                try:
                    self.properties['formal_charge'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'Complexity':
                try:
                    self.properties['complexity'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

        # experimental properties
        for property_obj in properties[1]:
            print(property_obj)
            if property_obj.get('TOCHeading') == 'LogP':
                try:
                    self.properties['logP'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'pKa':
                try:
                    self.properties['pKa'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj['TOCHeading'] == 'Melting Point':
                try:
                    self.properties['melting_pt'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj['TOCHeading'] == 'Melting Point':
                try:
                    self.properties['melting_pt'] = property_obj['Information'][0]['Value']['StringWithMarkup'][0]['String']
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'Solubility':
                try:
                    self.properties['solubility'] = property_obj['Information'][0]['Value']['Number'][0]
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'Solubility':
                try:
                    self.properties['solubility'] = property_obj['Information'][0]['Value']['StringWithMarkup'][0]['String']
                except (KeyError, IndexError):
                    print(self.URL)

            if property_obj.get('TOCHeading') == 'Collision Cross Section':
                try:
                    self.properties['collision_cross_sec'] = property_obj['Information'][0]['Value']['StringWithMarkup'][0]['String']
                except (KeyError, IndexError):
                    print(self.URL)
