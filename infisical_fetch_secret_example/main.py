import os
from infisical_sdk import InfisicalSDKClient


client = InfisicalSDKClient(host="http://infisical:8080")

# Authenticate with a machine identity (Universal Auth)
client.auth.universal_auth.login(
    client_id=os.environ["INFISICAL_CLIENT_ID"],
    client_secret=os.environ["INFISICAL_CLIENT_SECRET"],
)

secret = client.secrets.get_secret_by_name(
    secret_name="DATABASE_URL",
    project_id="your-project-id",
    environment_slug="prod",     # matches your environment slug (dev/staging/prod)
    secret_path="/",
)

print(secret.secretValue)