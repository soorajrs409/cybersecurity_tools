new_encrypt is an updated version of simple_encrypt script. new_encrypt can encrypt all the files in the directory and sub directories automatically

# clone the script 

# install the modules

pip install -r requirements.txt

# generate keys and store it in some safe location. 

python3 generate_key.py

# encrypt files

python3 encrypt.py <key.key / path to key> <directory / path to file>

# decrypt files

python3 decrypt.py <key.key / path to key> <directory / path to file>
