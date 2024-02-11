import { Blockchain, SandboxContract, TreasuryContract } from '@ton/sandbox';
import { Cell, toNano } from '@ton/core';
import { ContractExample } from '../wrappers/ContractExample';
import '@ton/test-utils';
import { compile } from '@ton/blueprint';

describe('ContractExample', () => {
    let code: Cell;

    beforeAll(async () => {
        code = await compile('ContractExample');
    });

    let blockchain: Blockchain;
    let deployer: SandboxContract<TreasuryContract>;
    let contractExample: SandboxContract<ContractExample>;

    beforeEach(async () => {
        blockchain = await Blockchain.create();

        contractExample = blockchain.openContract(ContractExample.createFromConfig({}, code));

        deployer = await blockchain.treasury('deployer');

        const deployResult = await contractExample.sendDeploy(deployer.getSender(), toNano('0.05'));

        expect(deployResult.transactions).toHaveTransaction({
            from: deployer.address,
            to: contractExample.address,
            deploy: true,
            success: true,
        });
    });

    it('should deploy', async () => {
        // the check is done inside beforeEach
        // blockchain and contractExample are ready to use
    });
});
