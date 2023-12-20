import asyncio

from openfga_sdk import OpenFgaClient, ClientConfiguration, TupleKey
from openfga_sdk.client import ClientCheckRequest
from openfga_sdk.client.models import ClientListObjectsRequest

from prettytable import PrettyTable


class OpenFga:
    def __init__(self, api_scheme="http", api_host="localhost:8080"):
        self.configuration = ClientConfiguration(
            api_scheme=api_scheme,
            api_host=api_host,
            store_id="01HH3ZY8HPJXF5Y466WJ5BZ2QJ"
        )
        self.fga_client = OpenFgaClient(self.configuration)

    async def check(self, payload: ClientCheckRequest):
        resp = await self.fga_client.check(payload)
        print(f"{payload.user} is {payload.relation} of {payload.object} ? {resp.allowed}")

    async def list_objects(self, payload: ClientListObjectsRequest):
        resp = await self.fga_client.list_objects(payload)
        print(f"{payload.user} is {payload.relation} of {payload.type}s: ", resp.objects)

    async def list_read(self, payload: TupleKey):
        resp = await self.fga_client.read(payload)
        await self.print_data(resp.tuples)

    @staticmethod
    async def print_data(data):
        x = PrettyTable()
        x.field_names = ["Object", "Relation", "User"]

        for item in data:
            x.add_row([item.key.object, item.key.relation, item.key.user])
        print(x)


async def main():
    openfga = OpenFga()

    print("\n", "---" * 15)
    print("Check for access:")
    payload = ClientCheckRequest(
        user="user:1",
        relation="owner",
        object="doc:1"
    )

    await openfga.check(payload)

    payload = TupleKey(
        user="user:3",
        object="doc:",
        relation="owner",
    )
    print("\n", "---" * 15)
    print(f"docs of {payload.user} are: ")
    await openfga.list_read(payload)

    payload = TupleKey(
        relation="member",
        object="team:1"
    )
    print("\n", "---" * 15)
    print(f"{payload.relation}s of {payload.object} are: ")
    await openfga.list_read(payload)

    payload = TupleKey(
        user="user:3",
        object="doc:"
    )
    print("\n", "---" * 15)
    print(f"{payload.object}s of {payload.user} are: ")
    await openfga.list_read(payload)

    payload = TupleKey(
        object="doc:t1"
    )
    print("\n", "---" * 15)
    print(f"{payload.object} is shared with: ")
    await openfga.list_read(payload)

    await openfga.fga_client.close()


if __name__ == "__main__":
    asyncio.run(main())

"""
1. Listing api for a user and for doc
2. If user owner/admin of team he can not be member in another/same team
3. Create team as resource and give him some permission and some permission to team member
4. If user has access to which all docs -  vice versa
5. Team wala access
"""
