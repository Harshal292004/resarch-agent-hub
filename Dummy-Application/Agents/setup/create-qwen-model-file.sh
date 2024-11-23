#!/bin/bash

# Variables
model_name="qwen"
custom_model_name="crewai-qwen"

# Get the base model
ollama pull $model_name

# Create the model file 
ollama create $custom_model_name -f ./qwenModelfile