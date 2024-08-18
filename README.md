# Gemma-2 2B fine-tuned for Structured Data Extraction

This project is a collection of notebook and a simple flask web server to serve 
**Gemma-2** using **llama-cpp**.

The goal of this project is to fine-tune a model to get a better result on the task of
to the task of extracting data into a structured format (JSON).

You will need to provide the **output schema** in openapi format and the **text** (context).

## ⛩️ Project Architecture

The project is divided between notebook for the fine-tuning, quantization and evaluation and python files.

| **Source**                       | **Description**                                                                                                       |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| [➡️ Gemma-2 Finetuning](https://github.com/bastienpo/llm-finetune/blob/main/src/notebook/gemma_2_finetuning.ipynb)           | A notebook that shows how tofine-tune and quantize  gemma2-2b-it using the unsloth and hugging-face libraries.        |
| [➡️ Server](https://github.com/bastienpo/llm-finetune/blob/main/src/web/app.py)                       | A simple flask REST server using llama-cpp with a 4 bit quantized model.                                              |
| [➡️ CI/CD](https://github.com/bastienpo/llm-finetune/blob/main/.github/workflows/cicd.yml)                        | A github action consisting of a formatting/linting step with ruff, testing with pytest and building the docker image. |
| [➡️ Dockerfile](https://github.com/bastienpo/llm-finetune/blob/main/Dockerfile)                   | A mutlistage dockerfile to build the server with gunicorn.                                                            |


## 📊 Details about the Dataset

The different finetuned models can be found in safetensors and GGUF format (4bit, 8bit) on the hugging-face hub at [bastienp/Gemma-2-2B-it-JSON-data-extration](https://huggingface.co/bastienp/Gemma-2-2B-it-JSON-data-extration).

**Note**: It also gives more details on how to use it with **llama-cpp** or **unsloth**.

## 💻 Installation

### Dev setup

Recommended: Use the fast Python package installer and resolver **uv** from astral.

Alternatively, you can replace this command with *pip*. You can find the documentation
for installing uv [here](https://github.com/astral-sh/uv?tab=readme-ov-file#getting-started).

1. Sync the dependencies with uv

```bash
uv venv .venv
```

```bash
source .venv/bin/activate
```

```bash
uv sync --all-extras --dev # in addition it adds pytest and ruff 
```

2. Launch a flask dev server

```bash
flask --app src.web.app run --debug
```

To reproduce the fine-tuning, the easiest way is to use Google Collab (the free version is sufficient).

3. Run the tests (API testing)

```bash
pytest
```
**Note**: An example of how to call the API and the prompt format can be found in `examplesexample_api_call.py`.

## 👥 Deployment setup 

In order to deploy the model the easiest way to go is to use the provided docker image.

1. Pull the image from github (buit from the CI):

```bash
docker pull ghcr.io/bastienpo/unsloth_finetuning:main 
```


**Note**: Otherwise you can build the image yourself
```bash
docker build -tag unsloth_finetuning:0.0.1 .
```


2. Run the docker image

```bash
docker run -p 8000:8000 -d unsloth_finetuning:main # or 0.0.1
```

3. Make a post request

```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"query": "How are you ?"}' http://localhost:8000/api/v1/chat/completions
```