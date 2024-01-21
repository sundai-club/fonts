# init 
export REPLICATE_API_TOKEN=<>
source <your_venv or conda>

# download model .zip files 



# run model - together 
model=lucataco/sdxl-lcm
zip_or_folder=fonts-2.zip
python tune_folder_any_replicate_model.py $zip_or_folder $model
# you will be prompted for model name - give - ltejedor/sundai-fonts-letters-together

# run model - separate
model=lucataco/sdxl-lcm
zip_or_folder=fonts-3.zip
python tune_folder_any_replicate_model.py $zip_or_folder $model
# you will be prompted for model name - give - ltejedor/sundai-fonts-letters-separate
