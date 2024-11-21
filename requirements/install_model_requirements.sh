git clone https://github.com/facebookresearch/audiocraft.git
cd audiocraft
python -m venv ./venv

if [ -f "./venv/bin/activate" ]; then
    source ./venv/bin/activate
elif [ -f "./venv/Scripts/activate" ]; then
    source ./venv/Scripts/activate
else
    echo "Não foi possível encontrar o script de ativação do ambiente virtual."
    exit 1
fi

pip install --upgrade pip
python.exe -m pip install --upgrade pip
pip install pesq
pip install -r requirements.txt
pip install -e .