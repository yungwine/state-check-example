import asyncio
import typing

from pytoniq import LiteBalancer, Contract, WalletV4R2, LiteClient
from pytoniq_core import StateInit, begin_cell, HashMap, Cell, Address
from secret import mnemo


class MyLiteClient(LiteClient):
    async def get_account_proof(self, address: typing.Union[str, Address]):
        if isinstance(address, str):
            address = Address(address)
        block = self.last_mc_block
        account = address.to_tl_account_id()
        data = {'id': block.to_dict(), 'account': account}
        result = await self.liteserver_request('getAccountState', data)
        account_state_root = Cell.one_from_boc(result['state'])
        return *Cell.from_boc(result['proof']), account_state_root, block  # need also return shard_proof cells for account not in master


async def get_wallet(client):
    return await WalletV4R2.from_mnemonic(client, mnemo, 0)


async def main():
    client = MyLiteClient.from_mainnet_config(5, 2)
    await client.connect()
    addr = Address('Uf_BvG8IeNYQFsOQ8Z5WqhcFLAcjZP_rvx-5_y32IyIYkJWz')
    block_proof, state_proof, account_state, block = await client.get_account_proof(addr)
    print(account_state)

    proof = (begin_cell()
             .store_bytes(block.root_hash)
             .store_ref(block_proof)
             .store_ref(state_proof)
             .store_bytes(addr.hash_part)
             .store_ref(account_state)
             .store_maybe_ref(None)  # shard_proof
             .end_cell())

    code = Cell.one_from_boc('b5ee9c7241020b01000169000114ff00f4a413f4bcf2c80b0102012003020114f26c31db3cf800d2005b060202cf05040047675ce6674c1cc30007cb913db638534800067f5007c0140750c3c01485ba44c780c3838a010fd3618ed9e69002dc060390d3ffd4d4d3ffd401d001f40430206e9130e30e55302450347fdb3c01d739544113db3cf2e44dd430d0d431d430d0f40430206ef2d3eb8307f40e6fa1f2e3ebf90101f901baf2e3ec07080a02dad0d4d4d3ffd31f302850427fdb3c02d739544114db3cf2e44d01d430d0d431d431d431d430d0f40430128020f40e6fa1f2e3edc801cf16c9d73999d30730c001f2e44f6d8e14d200019fd401f00501d430f005216e9131e030e0e2206ef2e3ee8100c0d721d3ff3001baf2e3ef080a024402d739544113db3cf2e44d018e91d430d0d431d431d430d739db3c20f2e44ee030700a090028923070e1d30701c004923070e18307d721d3ff30003001925b70e101d30701c003925b70e1d3ff3001ba9170e17ff03bfb1e')
    si = StateInit(code=code, data=Cell.empty())
    contract = await Contract.from_state_init(client, 0, si)
    print(contract)
    # await contract.send_external(body=proof)
    wallet = await get_wallet(client)
    # print(proof)
    await wallet.transfer(contract.address, 3 * 10 ** 7, body=proof)

    await client.close()


asyncio.run(main())
