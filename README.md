# Template

## Como rodar

### Requisitos
- Python 3.9+

### Instalar dependencias
```bash
pip install .
```

### Iniciar em desenvolvimento
```bash
python -m flask --app main run --debug
```

Abra `http://127.0.0.1:5000/` no navegador.

### Rodar em producao
```bash
gunicorn -w 2 -b 0.0.0.0:8000 main:app
```

Abra `http://127.0.0.1:8000/` no navegador.
