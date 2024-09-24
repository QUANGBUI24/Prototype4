"""
Author : Quang Bui
Created: September 24, 2024

Description:
    This shell will manage the storages for all the data
    of the UML program including saving/loading

List of last date modified:


"""

###################################################################################################

# IMPORTED MODULES #
import json
import os
from typing import List, Dict

###################################################################################################

# UML Class Storage Manager Constructor #
class UMLStorageManager:
    @staticmethod
    def load_name():
        file_path = "UML_UTILITY/SAVED_FILES/NAME_LIST.json"
        try:
            # Check if the file is empty
            if os.stat(file_path).st_size == 0:
                return []
            # Load data from the JSON file
            with open(file_path, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            # Handle the case where the file is not found
            print(f"\nFile {file_path} not found.")
            return None
        except json.JSONDecodeError:
            # Handle JSON decoding errors (e.g., if the file is not in proper JSON format)
            print(f"\nError decoding JSON from {file_path}.")
            return None
        
    
    #################################################################
    
     # UML class storage manager constructor #
    def __init__(self):
        self.__saved_file_name_list: List[Dict] = self.load_name()
        
    def _get_saved_list(self) -> List[Dict]:
        return self.__saved_file_name_list
        
    #################################################################
    ### MEMBER FUNCTIONS ###
    
    ## SAVE/LOAD RELATED ##
    
    # Save the current data to a JSON file #
    def _save_data_to_json(self, file_name: str, class_data_list: List[Dict], relationship_data_list: List[Dict]):
        file_path = f"UML_UTILITY/SAVED_FILES/{file_name}.json"
        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                # If the file doesn't exist, create it and write the data list
                with open(file_path, "w") as json_file:
                    new_structure = {"classes":[], "relationships":[]}
                    new_structure["classes"] = class_data_list
                    new_structure["relationships"] = relationship_data_list
                    json.dump(new_structure, json_file, indent=4)
                    return
            # If the file exists and the file name is in the saved list, update the data
            for dictionary in self.__saved_file_name_list:
                if file_name in dictionary:
                    # Open the file and load its current data
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        # Overwrite the loaded data with the current data list
                        data["classes"] = class_data_list
                        data["relationships"] = relationship_data_list
                    # Save the updated data to the file
                    with open(file_path, "w") as json_file:
                        json.dump(data, json_file, indent=4)
        except json.JSONDecodeError:
            # Handle JSON decoding errors (e.g., if the file is not in proper JSON format)
            print(f"\nError decoding JSON from {file_path}.")
            return None
        
    # Load data from the specified JSON file
    def _load_data_from_json(self, file_name: str):
        file_path = f"UML_UTILITY/SAVED_FILES/{file_name}.json"
        try:
            # Open the file and load the data from JSON
            with open(file_path, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            # Handle the case where the file is not found
            print(f"File {file_path} not found.")
            return None
        except json.JSONDecodeError:
            # Handle JSON decoding errors (e.g., if the file is not in proper JSON format)
            print(f"\nError decoding JSON from {file_path}.")
            return None
        
    # Save the new file name to the saved file list #
    def _add_name_to_saved_file(self, saved_list: List[Dict]):
        file_path = "UML_UTILITY/SAVED_FILES/NAME_LIST.json"
        try:
            # Open the file and save the name list in JSON format
            with open(saved_list, "w") as file:
                json.dump(saved_list, file, indent=4)
        except FileNotFoundError:
                # Handle the case where the file is not found
            print(f"\nFile {file_path} not found.")
            return None
        except json.JSONDecodeError:
            # Handle JSON decoding errors (e.g., if the file is not in proper JSON format)
            print(f"\nError decoding JSON from {file_path}.")
            return None
                
###################################################################################################