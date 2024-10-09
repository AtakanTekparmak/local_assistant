# Local Assistant

It's a passion project to build a local AI assistant that can run on my own laptop (M1 Max 64GB). Will be some time before this is remotely useful, but I believe [Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct) has a lot of potential.

## Idea

1. LLMs express algorithmic thinking best in Python (most likely due to the abundance of Python code in their pretraining datasets).
2. Define tools in Python, use them in Python.
3. Local assistant.

## Requirements

- Python 3.10+
- Make
- An OpenAI compatible local LLM provider

## Setup

1. Serve the model using an OpenAI compatible API. I'm using [LM Studio](https://lmstudio.ai/) to host the model. But other options include:
    - [ollama](https://ollama.com/)
    - [vLLM](https://github.com/vllm-project/vllm)
    - [LocalAI](https://github.com/mudler/LocalAI)

2. Clone this repository and install the dependencies:

```bash
make install
```

3. Run the assistant:

```bash
make run
```

## Extending the Assistant's Capabilities   

You can add more tools to the assistant by adding them to `src/tools/__init__.py`, preferably by importing them from a dedicated file in `src/tools/` (not necesssary).