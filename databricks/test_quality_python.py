import json
import pandas as pd
import re

def clean_website_url_python(df, column_name, new_column_name):
    """
    Versão Pure Python/Pandas da função de limpeza de URLs.
    """
    # Regex para manter apenas caracteres seguros (mesma lógica do Spark)
    regex_invalid_chars = r"[^a-zA-Z0-9\.\-\/:]"
    
    def apply_cleaning(val):
        if val is None or pd.isna(val):
            return None
        # 1. trim (strip) e lower
        cleaned = str(val).strip().lower()
        # 2. regex_replace
        cleaned = re.sub(regex_invalid_chars, "", cleaned)
        return cleaned

    # Criamos a nova coluna aplicando a função linha a linha
    df[new_column_name] = df[column_name].apply(apply_cleaning)
    return df

# 1. Ler o arquivo JSON utilizando o módulo nativo json
with open("sample_bronze.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Transformar os dados em um DataFrame do Pandas
df = pd.DataFrame(data)

# 3. Aplicar a limpeza de URLs
df_modified = clean_website_url_python(df, "website_url", "website_url_cleaned")

# 4. Exibir o resultado final (Top 20 linhas)
print("Resultados da Limpeza (Versão Python/Pandas):")
# O to_string() evita que o pandas corte a visualização das colunas
print(df_modified[["name", "website_url", "website_url_cleaned"]].head(20).to_string(index=False))
