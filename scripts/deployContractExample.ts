import { toNano } from '@ton/core';
import { ContractExample } from '../wrappers/ContractExample';
import { compile, NetworkProvider } from '@ton/blueprint';

export async function run(provider: NetworkProvider) {
    const contractExample = provider.open(ContractExample.createFromConfig({}, await compile('ContractExample')));

    await contractExample.sendDeploy(provider.sender(), toNano('0.05'));

    await provider.waitForDeploy(contractExample.address);

    // run methods on `contractExample`
}
