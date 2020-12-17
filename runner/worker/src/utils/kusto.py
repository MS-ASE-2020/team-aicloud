from azure.kusto.data import KustoClient, KustoConnectionStringBuilder

cluster = "<insert here your cluster name>"
client_id = "<insert here your AAD application id>"
client_secret = "<insert here your AAD application key>"
authority_id = "<insert here your AAD tenant id>"

kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
    cluster, client_id, client_secret, authority_id)
client = KustoClient(kcsb)

db = "Samples"
query = "StormEvents | take 10"

response = client.execute(db, query)
for row in response.primary_results[0]:
    print(row[0], " ", row["EventType"])
