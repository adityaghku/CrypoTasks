Sure, here's a template for a README file on GitHub that you can use for your interview assignment:

# Crypto / Misc Coding tasks

## Task 1: Logger implementation

Create a logging component that writes strings to a text file asynchronously.

### Requirements

1. A call to write should be as fast as possible so that the calling application can continue
with its work without waiting for the log to be written to the file.
2. If we cross midnight, a new file with a new timestamp must be created. Logs will then be written to the new file.
3. The component must be possible to stop in two ways:
a. Stop immediately. Any outstanding logs in the pipeline will be omitted.
b. Wait for the component to finish writing any outstanding logs.
4. If an error occurs during logger operations, the calling application should not halt as a result. It is more important for the application to continue running, even if lines are not being written to the log.
5. Extra points will be awarded for implementing unit tests that ensure:
a. A call to log will result in something being written.
b. New files are created when midnight is crossed.
c. The stop behaviour works as described above.

### Example implementation

An example implementation is provided in the main() function of logger.py. The logger class can be instantiated and used for any logging activity. The output is provided in the log file of the folder as a sample output.

## Task 2: Smart Contract (Solidity)

Design a smart contract to randomly select an X number of winners in a lucky draw, using ChainLink’s on-chain verifiable random function

### Requirements

1. Only the owner/deployer of the contract should be able to control the following:
  a. Set the number of winners to be chosen.
  b. Set an array of candidate addresses that will enter the lucky draw.
  c. Withdraw funds (LINK) from the contract.
2. Write unit tests and scripts for deployment.
3. Fund the contract with LINK tokens on a test-net from a faucet.
4. Deploy the contract to a test-net.
5. Set the number of winners and array of candidate addresses.
6. Execute a transaction to randomly select the desired number of winners.

### Results

Requirements 5 and 6 were not completed but the rest were. The deployed contract is available in "contract address.txt" and main.sol and deploy.deploy.js are the main and deploy functions separately. Remix IDE very conveniently generated the unit tests scattered throughout the folders. 

## Task 3: Trading

Design and implement a client that uses a WebSocket to stream orderbook data from an exchange of your choice.

### Requirements

1. The orderbook must be stored in memory (at least 5 levels).
2. Justify your choice of the data structure used to store the orderbook data.
3. Updating the local version of the orderbook must be done asynchronously.
4. The code design must be fail-safe such that the flow of the main application is not interrupted even if the exchange’s server goes down.
5. Find the AWS instance that has the lowest latency with the server where the exchange’s matching engine resides. Explain your approach.

### Results

The exchange chosen was binance. The orderbook is stored as a JSON locally. The answer to Q5 is provided in the file "AWS approach.txt".
The best data structure for the orderbook would be a priority queue or a heap, but I did not implement this (due to time constraints). having a sorted array of bid and asks would be convenient when accessing the orderbook data.

## Conclusion

I hope you find the solutions demonstrate my coding capabilities. I'd never used Solidity before so it was quite fun to try it out. I know that there might be some mistakes with very edge cases in logger and the orderbook because my knowledge and experience of asyncio before this was not great, but I tried my best. I also wanted to attempt all the tasks (last 2 of task 2 and last 1 of task 3) But I had so many exams and submissions this week, I tried my best to give this task as much time as possible. Thank yoU!
