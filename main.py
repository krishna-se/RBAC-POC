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
            store_id="01HKPX2406CPR7Q18RV58R4J9N"
        )
        self.fga_client = OpenFgaClient(self.configuration)

    async def check(self, payload: ClientCheckRequest):
        resp = await self.fga_client.check(payload)
        print(f"{payload.user} is {payload.relation} of {payload.object} ? {resp.allowed}")

    async def list_objects(self, payload: ClientListObjectsRequest):
        resp = await self.fga_client.list_objects(payload)
        x = PrettyTable()
        x.field_names = [payload.user]
        x.add_row(resp.objects)
        print(x)

    async def list_read(self, payload: TupleKey):
        try:
            resp = await self.fga_client.read(payload)
            await self.print_data(resp.tuples)
        except Exception as e:
            print(e.__dict__)

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
    payload = ClientCheckRequest(
        user="user:u3",
        relation="owner",
        object="file:f1"
    )
    print("Check for access:")
    await openfga.check(payload)

    print("\n", "---" * 15)
    payload = ClientCheckRequest(
        user="user:m5",
        relation="viewer",
        object="file:f1"
    )
    print("Check for access for a member where team:t1 is viewer for doc:t1:")
    await openfga.check(payload)

    print("\n", "---" * 15)
    print("1. List all file-objects a member/admin has access to.")
    payload = TupleKey(
        user="user:m2",
        object="file:",
    )
    await openfga.list_read(payload)

    print("\n", "---" * 15)
    print("2. List all member/admin who has <define-perm> to a file-object.")
    payload = TupleKey(
        object="file:f1"
    )
    await openfga.list_read(payload)

    print("\n", "---" * 15)
    print("3. List all teams for a admin/member. ")
    payload = TupleKey(
        user="user:m2",
        object="team:"
    )
    await openfga.list_read(payload)

    print("\n", "---" * 15)
    print("4. List all members/admin of a team.")
    payload = TupleKey(
        object="team:t2",
        relation="member"
    )
    await openfga.list_read(payload)

    print("\n", "---" * 15)
    print("5. List all teams in an Organization/Company.")
    payload = ClientListObjectsRequest(
        user="company:xyz",
        relation="org",
        type="team"
    )
    await openfga.list_objects(payload)

    await openfga.fga_client.close()


if __name__ == "__main__":
    asyncio.run(main())
