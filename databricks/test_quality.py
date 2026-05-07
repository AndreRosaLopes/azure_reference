import os
from pathlib import Path
from pyspark.sql import SparkSession

# Força o PySpark a usar a versão instalada no ambiente virtual (4.1.1)
# em vez da versão instalada globalmente no Windows (3.5.2)
# if "SPARK_HOME" in os.environ:
#     del os.environ["SPARK_HOME"]

from src.utils.data_quality import clean_website_url

# 1. Iniciar a sessão Spark
# No Databricks, o objeto 'spark' já vem pré-configurado.
spark = SparkSession.builder.appName("DataQualityTest").remote("local[*]").getOrCreate()

# 2. Caminho do arquivo JSON
# Certifique-se de que o arquivo sample_bronze.json está no mesmo diretório ou acessível.
json_path = str(Path(__file__).parent / "sample_bronze.json")

# 3. Ler o arquivo JSON e transformar em DataFrame
# Usamos multiline=True pois o JSON é um array de objetos.
df = spark.read.option("multiline", "true").json(json_path)

# 4. Chamar a função de limpeza para endereços de sites
# Passamos o DF original, a coluna de origem e o nome da nova coluna.
df_modified = clean_website_url(df, "website_url", "website_url_cleaned")

# 5. Exibir o DataFrame modificado
# Selecionamos apenas algumas colunas para facilitar a visualização no console.
print("Exibindo DataFrame com URLs limpas (mantendo o prefixo http/www):")
df_modified.select("name", "website_url", "website_url_cleaned").show(20, truncate=False)


input("Pressione ENTER para encerrar o Spark e fechar a UI...")
# 6. Encerrar a sessão Spark
spark.stop()
