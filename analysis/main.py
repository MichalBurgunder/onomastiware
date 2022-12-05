import os
from os.path import exists
import sys

from analysis_max_depth import populate_ety_depths, prepare_depth_data
from preparatory import get_headers_hashmap, get_element_hashmap, prepare_data, add_virtual_columns
from file_management import save_as_csv
from config import prepare_globals, fill_clean_names, root, paths, ety_depth
from utils import get_run_options
from analysis_by_year import prepare_ety_by_year_data
from analysis_number_morphemes import prepare_ety_type_2

os.system('clear')

# lines, element_hashmap, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3] !!OBS!!
# lines, headers, header_hms = dataa[0], dataa[1], dataa[2], dataa[3]

def __main__():
    options = get_run_options(sys.argv)

    # takes from temp_debug.csv, if exists
    dataa = prepare_data(root, paths, options)
    
    new_headers = add_virtual_columns(dataa, [ety_depth], ["-1"])
    
    cs = prepare_globals(dataa)
    fill_clean_names(dataa, cs)
    # exit()
    header_hashmap, headers = get_headers_hashmap(root, paths, new_headers)

    element_hash_map = get_element_hashmap(dataa[0], headers)
    
    ready_dataa = [dataa[0], element_hash_map, headers, header_hashmap]


    populate_ety_depths(ready_dataa, cs, options)

    
    # deduplication of list, for better use
    new_additives = list(set(cs['additives']))

    if len(new_additives):
        print("Additives: \n")
        print(new_additives)
        save_as_csv(new_additives, "new_additives", True, options)
        print("\nAdd new additives to proceed with analysis\n")
        exit()
    print("No new additives. Proceeding to analysis...")
    # exit() cs['root'], new_additives, "new_additives"

    # writes data to final_ety_depths.csv
    prepare_depth_data(dataa[0], cs)
    prepare_ety_by_year_data(dataa[0], headers, cs)
    prepare_ety_type_2(dataa[0], headers, cs)
    print("All done!")

__main__()