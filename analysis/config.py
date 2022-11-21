jargon_entries = ["1st Jargon", "2nd Jargon", "3rd Jargon", "4th Jargon"] # the fields which will create our tree
root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data'
raw_data_root = '/Users/michal/Documents/thesis/etymologies_of_jargon/thesis_data/raw_data'
paths = [
            'Thesis_data - programming_languages.csv', # programming languages
            'Thesis_data - additives.csv' # all additives (entries not originating from scrapes)
        ]
additives = [] # here will be all the new name additives that have not been added just yet
ety_depth = "Etymology Depth"
clean_name = "Cleaned Name"
consts = None
debug = False


def find_field_position(headers, field):
    for i in range(0, len(headers)):
        if headers[i] == field:
            return i
    raise f"Cannot find '{field}' column"

def prepare_virtual_fields(dataa, cs):
    cs['ety_depth_pos'] = find_field_position(dataa[1], cs['ety_depth'])
    cs['clean_name_pos'] = find_field_position(dataa[1], cs['clean_name'])
    cs['scrape_name_pos'] = find_field_position(dataa[1], cs['scrape_name'])

def find_jargon_entry_positions(headers, jargons):
    entry_positions = []
    for h in range(0, len(headers)):
        for j in jargons:
            if j == headers[h]:
                entry_positions.append(h)
                break

    if len(entry_positions) != len(jargons):
        print("Can't find jargons. Exiting...")
        exit()
    return entry_positions

def fill_clean_names(dataa, cs):
    for i in range(0, len(dataa[0])):
        if dataa[0][i][cs['clean_name_pos']] == '':
            if i == 670:
                print(dataa[0][i])
            dataa[0][i][cs['clean_name_pos']] = dataa[0][i][cs['scrape_name_pos']]
            if i == 670:
                print(dataa[0][i]) 
    
    
def prepare_globals(dataa):
    global consts
    
    consts = {
        'jargon_entries': jargon_entries, # the fields which will create our tree
        'jargon_entry_positions': None,
        'root': root,
        'raw_data_root': raw_data_root,
        'paths': paths,
        'additives': [], # here will be all the new name additives that have not been added just ye
        'virtual_fields': ["ety.depth"],
        'vf_default_values': ['-1'],
        'clean_name': "Cleaned Name",
        'clean_name_pos': None,
        'scrape_name': 'Scrape Name', 
        'ety_depth': "Etymology Depth",
        'ety_depth_pos': None,
    }

    # lets find the jargon entry positions
    consts['jargon_entry_positions'] = find_jargon_entry_positions(dataa[1], consts['jargon_entries'])

    prepare_virtual_fields(dataa, consts)

    return consts
    

def get_run_options(args):
    options = {
        "v": False,
        "c": False
    }
    clean_args = args[1].replace('-', '', 1)

    if "v" in clean_args:
        options['v'] = True
    if "c" in clean_args:
        options['c'] = True
        
    return options