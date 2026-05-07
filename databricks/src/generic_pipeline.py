# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # Generic Pipeline Orchestrator (DAG Executor)
# MAGIC A fully metadata-driven notebook that reads JSON configurations, 
# MAGIC manages a memory dictionary for DataFrames, and executes read, transform, and write steps.

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

import json
import os
import sys
import importlib
from datetime import datetime

# Adiciona o diretório pai (raiz do projeto) ao sys.path
sys.path.append(os.path.abspath('..'))

# COMMAND ----------

# Parameters
dbutils.widgets.text("pipeline_config", "bronze_breweries")
pipeline_config = dbutils.widgets.get("pipeline_config")

# COMMAND ----------

# 1. Load Configuration
notebook_dir = os.getcwd()
project_root = os.path.abspath(os.path.join(notebook_dir, ".."))
config_path = f"{project_root}/metadata/pipelines/{pipeline_config}.json"

with open(config_path, "r") as f:
    config = json.load(f)

steps = config.get("steps", [])

# COMMAND ----------

# 2. Setup Memory Space
# A variável 'spark' é injetada automaticamente pelo Databricks no escopo global
memory = {
    "spark": spark
}

# COMMAND ----------

# 3. Step Execution Engine
for index, step in enumerate(steps):
    mod_name = step.get("module")
    func_name = step.get("function")
    params = step.get("params", {})
    inputs = step.get("inputs", {})
    output_alias = step.get("output")

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"--- {mod_name} - Step {index + 1}: [{time_now}] started execution {func_name} ---\n")

    # Resolução explícita de inputs vs parâmetros literais
    resolved_params = params.copy()
    
    # Injeta os inputs definidos explicitamente buscando da memória
    for arg_name, memory_key in inputs.items():
        resolved_params[arg_name] = memory[memory_key]
            
    try:
        # Importação dinâmica do módulo
        module = importlib.import_module(mod_name)
        # Obtenção dinâmica da função
        func = getattr(module, func_name)
        
        # Execução da função
        result = func(**resolved_params)
        
        # Armazenamento em memória usando a Estratégia 1 (Buraco Negro para Nones)
        memory[output_alias] = result
        
        # Log de sucesso com timestamp
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{time_now}] {mod_name} executed {func_name} successfully ✔️ \n")
            
    except Exception as e:
        raise RuntimeError(f"❌ Step {index + 1} failed during execution of {func_name}: {e}")

print("🟩🟩🟩 {pipeline_config} executed successfully! 🟩🟩🟩")
