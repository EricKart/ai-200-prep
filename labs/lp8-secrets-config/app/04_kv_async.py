"""Part 4 - Async client: fetch several secrets at the same time.

What this shows (LP8 Module 1, unit 3, "async client"):
  - azure.keyvault.secrets.aio.SecretClient has the same methods, but you `await` them
  - Both the client and the credential must be closed (async with / await close())
  - asyncio.gather() runs the 3 calls concurrently instead of one after another
"""
import lab_env  # noqa: F401  first import: stops with a clear message if the venv isn't active
import asyncio
import time

from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient

from lab_env import need

NAMES = ["openai-api-key", "cosmosdb-connection-string", "storage-connection-string"]


async def main():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=need("KEY_VAULT_URL"), credential=credential)

    async with client:                       # closes the client at the end
        await client.get_secret(NAMES[0])    # warm-up (sign-in)

        start = time.perf_counter()
        for name in NAMES:                   # one after another
            await client.get_secret(name)
        one_by_one = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        secrets = await asyncio.gather(*(client.get_secret(n) for n in NAMES))   # all at once
        together = (time.perf_counter() - start) * 1000

    await credential.close()                 # the async credential must be closed too

    for s in secrets:
        print(f"  got {s.name:<28} version {s.properties.version[:8]}..")
    print(f"\n  one after another : {one_by_one:.0f} ms")
    print(f"  asyncio.gather    : {together:.0f} ms")
    print("\nDone. Part 4 complete.")


asyncio.run(main())
