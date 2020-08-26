from pyspark.sql import SparkSession, types
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StructType, StructField, IntegerType, Row

import pyspark.sql.functions as f
import pyspark.sql.types as t

spark = SparkSession \
    .builder \
    .appName("PythonCount") \
    .getOrCreate()
df = spark.createDataFrame([("Alive", 4)], ["Name", "Number"])


def example(n):
    return t.Row('Out1', 'Out2')(n + 2, n - 2)


schema = StructType([
    StructField("Out1", t.IntegerType(), False),
    StructField("Out2", t.IntegerType(), False)])

example_udf = f.udf(example, schema)

newDF = df.withColumn("Output", f.explode(f.array(example_udf(df["Number"]))))
newDF = newDF.select("Name", "Number", "Output.*")

newDF.show(truncate=False)
newDF.explain()