# Infisical Fetch Secret Example

Fetches a secret from a self-hosted [Infisical](https://infisical.com/) instance using a machine identity.
See [`main.py`](./main.py).

## What is Infisical?

Infisical is an open-source secrets manager. Instead of scattering API keys, database URLs, and tokens across `.env`
files, CI variables, and chat messages, you store them once in Infisical and pull them at runtime, just like you would 
do with Azure KeyVault. 

It organizes secrets by project, environment (dev/staging/prod), and folder path, and keeps an audit trail of who read
or changed what.

The whole thing is open source and can run on your own hardware.

## Why self-host?

With a self-hosted instance your secrets never leave infrastructure you control. That matters for regulated data, 
air-gapped networks, or just not wanting a third party in the path between your app and its credentials.

You get the same features as the cloud version: machine identities, environment scoping, versioning, and access 
policies. The usual setup is a Docker Compose stack (the Infisical server plus a Postgres and a Redis) behind your 
reverse proxy. In this example the server is reachable at `http://infisical:8080`, which is how a container names it on
a shared Docker network.

## How the example manages secrets safely

The pattern in `main.py`:

1. **Authenticate with a machine identity, not a personal login.** The app uses Universal Auth with a client ID and 
secret. These belong to the service, not a human, so you can scope and revoke them independently.
2. **Keep the bootstrap credentials in the environment.** `INFISICAL_CLIENT_ID` and `INFISICAL_CLIENT_SECRET` come from
`os.environ`, never hardcoded. They're the only two values the app needs to know up front; everything else lives in
Infisical.
3. **Scope the read.** The fetch names an exact project, environment slug, and path. A leaked prod identity can't read
staging, and a dev token can't reach prod.
4. **Pull at runtime.** The `DATABASE_URL` is retrieved when the app runs and held in memory, so the actual secret is
never committed to the repo or baked into an image.

```python
import os
from infisical_sdk import InfisicalSDKClient

client = InfisicalSDKClient(host="http://infisical:8080")

client.auth.universal_auth.login(
    client_id=os.environ["INFISICAL_CLIENT_ID"],
    client_secret=os.environ["INFISICAL_CLIENT_SECRET"],
)

secret = client.secrets.get_secret_by_name(
    secret_name="DATABASE_URL",
    project_id="your-project-id",
    environment_slug="prod",
    secret_path="/",
)
```

## Running it

Install the dependency (the project uses [uv](https://docs.astral.sh/uv/)):

```bash
uv sync
```

Set the machine identity credentials, then run:

```bash
export INFISICAL_CLIENT_ID=...
export INFISICAL_CLIENT_SECRET=...
uv run main.py
```

Before it works, replace `your-project-id` with your project's ID, adjust `host` to point at your instance, and create
a Universal Auth machine identity in the Infisical dashboard with read access to the target project and environment.
