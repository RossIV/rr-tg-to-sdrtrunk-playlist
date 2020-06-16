import argparse
from pandas import read_csv
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring
from xml.dom import minidom

parser = argparse.ArgumentParser(description='RadioReference Talkgroup CSV to Playlist Aliases')
parser.add_argument('file')
parser.add_argument('list_name')
args = parser.parse_args()

csv = None
try:
    csv = read_csv(args.file)
except FileNotFoundError:
    print("File not found, check argument and try again")

tag_icon_map = {
    'Public Works': 'Van',
    'Law': 'Police',
    'Security': 'Police',
    'Fire': 'Fire Truck',
    'Transportation': 'Transport Bus',
    'Interop': 'No Icon',
    'Other': 'No Icon',
    'Schools': 'School Bus',
    'EMS': 'Ambulance',
    'Hospital': 'Ambulance',
    'Corrections': 'Police',
    'Multi-Tac': 'No Icon',
    'Emergency': 'No Icon',
    'Business': 'No Icon'
}
aliases = {}
top = Element('playlist')
for index, row in csv.iterrows():
    alias_data = {
        'color': '-16777216',
        'group': row['Category'],
        'list': args.list_name,
        'name': row['Description'],
        'iconName': [tag_icon_map[key] for key in tag_icon_map if key in row['Tag']][0],
    }
    alias = SubElement(top, 'alias', alias_data)
    id_data = {
        'type': 'talkgroup',
        'protocol': 'APCO25',
        'value': "{}".format(row['Decimal']),
    }
    id = SubElement(alias, 'id', id_data)

print(minidom.parseString(tostring(top)).toprettyxml(indent="   "))