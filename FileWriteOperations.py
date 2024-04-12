import json
import shutil
from os.path import exists
from pathlib import Path
import FileReadOperations as reader

class FileWriteOperations():
   
   def copy_selected_file_and_rename_copy(self, copy_file_name, new_file_name):
      print("     inside: copy_selected_file_and_rename_copy")
      home_path = self.r.get_configs_home_path("user-config-path") 
      old_path = '{}\\{}'.format(home_path, copy_file_name)
      new_path = '{}\\{}'.format(home_path, new_file_name)
      shutil.copy(old_path, new_path)
      print("     leaving: copy_selected_file_and_rename_copy")

   def write_list_to_file(self, user_config_path, file_name, file_list):
      print("     inside: write_list_to_file")
      self.r = reader.FileReadOperations()
      home_path = self.r.get_configs_home_path(user_config_path)
      file_path = '{}\\{}'.format(home_path, file_name)
      with open(file_path, 'w') as f:
         for line in file_list:
            line = line.replace('""', '"')
            f.write(line+"\n")
      print("     leaving: write_list_to_file")

   def delete_unwanted_file(self, file_name, config_name):
      print("     inside: delete_unwanted_file")
      self.r = reader.FileReadOperations()
      home_path = self.r.get_configs_home_path(config_name)
      file_path = '{}\\{}'.format(home_path, str(file_name))
      file_to_remove = Path(str(file_path))
      results = True
      try:
         file_to_remove.unlink()
      except IsADirectoryError :
         results = False
      except FileNotFoundError :
         results = False
      except PermissionError :
         results = False
      if results is True:
         print("results from delete: "+str(results))
      else:
         print("could not delete file: "+file_name)
      print("     leaving: delete_unwanted_file")
      return results
  
   def create_new_configuration_file(self, file_name):
      print("     inside: create_new_configuration_file")
      self.r = reader.FileReadOperations()
      home_path = self.r.get_configs_home_path("user-config-path")
      file_path = '{}\\{}'.format(home_path, str(file_name))
      Path(file_path).touch()
      results = exists(file_path)
      print("     leaving: create_new_configuration_file")
      return results
  
   def create_and_append_to_output_data_file(self, line_list, file_name, file_format):
      print("     inside : create_and_append_to_output_data_file")
      self.r = reader.FileReadOperations()
      file_name = self.replace_file_name_extension(file_name, file_format)
      home_path = self.r.get_configs_home_path("output-data")
      file_path = '{}\\{}'.format(home_path, str(file_name))
      with open(file_path, 'w') as f:
         for line in line_list:
            f.write(line+"\n")
      print("     leaving : create_and_append_to_output_data_file")

   def replace_file_name_extension(self, file_name, file_format):
      print("     inside : replace_file_name_extension")
      file_format = '.{}'.format(file_format)
      file_name = file_name.replace('.cfg', file_format)
      print("     leaving : replace_file_name_extension")
      return file_name