python := env_var_or_default("PYTHON", "python")
pip := env_var_or_default("PIP", "python -m pip")

if os() == "windows" {
    set shell := "cmd"
}

install:
    {{pip}} install -r requirements.txt 

convert OUTPUT_DIR='.' SEED='0':
    {{python}} screenies.py {{OUTPUT_DIR}} 
