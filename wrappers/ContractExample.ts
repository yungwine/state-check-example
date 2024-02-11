import { Address, beginCell, Cell, Contract, contractAddress, ContractProvider, Sender, SendMode } from '@ton/core';

export type ContractExampleConfig = {};

export function contractExampleConfigToCell(config: ContractExampleConfig): Cell {
    return beginCell().endCell();
}

export class ContractExample implements Contract {
    constructor(readonly address: Address, readonly init?: { code: Cell; data: Cell }) {}

    static createFromAddress(address: Address) {
        return new ContractExample(address);
    }

    static createFromConfig(config: ContractExampleConfig, code: Cell, workchain = 0) {
        const data = contractExampleConfigToCell(config);
        const init = { code, data };
        return new ContractExample(contractAddress(workchain, init), init);
    }

    async sendDeploy(provider: ContractProvider, via: Sender, value: bigint) {
        await provider.internal(via, {
            value,
            sendMode: SendMode.PAY_GAS_SEPARATELY,
            body: beginCell().endCell(),
        });
    }
}
