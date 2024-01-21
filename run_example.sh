# init 
export REPLICATE_API_TOKEN=<>
source <your_venv or conda>

# run model 
model=lucataco/sdxl-lcm
zip_or_folder=fonts-1.zip
python tune_folder_any_replicate_model.py $zip_or_folder $model
