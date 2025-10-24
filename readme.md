**Idea del Proyecto:**

GreenFrost es un proyecto de programación diseñado para el aprendizaje universitario, inspirado en la idea de negocio de Amazon. El proyecto se enfoca en la creación de una aplicación web que permita a los usuarios registrados comprar productos de diversas categorías, así como a los vendedores publicar productos y gestionar sus ventas.

---
**Colaboradores:**
- [Christian Pin](https://github.com/Crisblue1324) 
- [Roger Cornejo](https://github.com/Rcornejom06/)
---
**Tecnologias Utilizadas:**
- Python
- Django
- HTML
- Tailwind CSS
- JavaScript
---
**Instalacion:**
1. Clonar el repositorio
```bash
git clone https://github.com/aterana3/greenfrost.git
```
2. Instalar las dependencias
```bash
pip install -r dependencias.txt
```
3. Crear database en postgres
4. Crear el archivo .env con lo siguiente
```python
POSTGRES_HOST=[host]
POSTGRES_PORT=[port]
POSTGRES_DB=[database name]
POSTGRES_USER=[user]
POSTGRES_PASSWORD=[password]
```
5. Descargar el modelo
```bash
python manage.py download_model --model_name [model_name]
```
Modelos disponibles:
- **Meta-Llama-3-8B-Instruct.Q4_0.gguf**:
  - **Filesize**: 4.66 GB
  - **RAM Required**: 8 GB
  - **Parameters**: 8 Billion

- **Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf**:
  - **Filesize**: 4.11 GB
  - **RAM Required**: 8 GB
  - **Parameters**: 7 Billion
- **Phi-3-mini-4k-instruct.Q4_0.gguf**:
  - **Filesize**: 2.18 GB
  - **RAM Required**: 4 GB
  - **Parameters**: 3.8 Billion
- **orca-mini-3b-gguf2-q4_0.gguf**:
  - **Filesize**: 1.98 GB
  - **RAM Required**: 4 GB
  - **Parameters**: 3 Billion
- **gpt4all-13b-snoozy-q4_0.gguf**:
  - **Filesize**: 7.37 GB
  - **RAM Required**: 16 GB
  - **Parameters**: 13 Billion

Una vez descargado ir a settings.py y cambiar la variable MODEL_USAGE con el nombre del modelo descargado

6. Crear migraciones
```bash
python manage.py makemigrations / python manage.py makemigrations <app_name>
python manage.py migrate
```
7. Crear superusuario
```bash
python manage.py createsuperuser
```
8. Correr el servidor
```bash
python manage.py runserver 0.0.0.0:8000
```
