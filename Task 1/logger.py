import asyncio
import datetime
import time


class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.queue = asyncio.Queue()
        self.task = None
        self.running = False
        self.file_date = None

    async def start(self):
        # Open the log file with today's date in "append" mode
        self.file = open(
            f'{self.filename}.{datetime.date.today().strftime("%Y%m%d")}', "a"
        )
        # Start the write loop task
        self.task = asyncio.create_task(self.write_loop())

    async def stop(self, wait=False):
        if not wait:
            self.task.cancel()

        # Wait for the write loop to finish if wait=True
        if wait:
            await self.task
        # Close the log file
        if self.file is not None and not self.file.closed:
            self.file.close()

    async def write(self, message):
        time.sleep(10)
        # Put the message into the queue if it's not empty
        if message:
            await self.queue.put(f"{datetime.datetime.now()} - {message}")

    async def write_loop(self):
        # Set the running flag to True to start the loop
        self.running = True
        while self.running:
            try:
                # Get a message from the queue with timeout=2.0 seconds
                message = await asyncio.wait_for(self.queue.get(), timeout=2.0)
                # Exit the loop if a "stop" message is received
                if message is None:
                    break
                # If the logger is not running, exit the loop
                if not self.running:
                    break
                # Check if a new file needs to be created
                if not self.file or self.should_rotate():
                    # Close the old file if it's open
                    if self.file is not None and not self.file.closed:
                        self.file.close()
                    # Create a new file with today's date
                    self.file = self.get_new_file()
                # Write the message to the file and flush the buffer
                self.file.write(message + "\n")
                self.file.flush()
                # Mark the item as done after processing
                self.queue.task_done()

            except asyncio.TimeoutError:
                # If the queue times out, continue the loop
                continue
            except Exception as e:
                # Handle the specific exception here
                # Print the error to the console without stopping the program
                print(f"Exception occurred in write_loop: {e}")

    def should_rotate(self):
        # Check if today's date is different from the last time the file was rotated
        if self.file_date is None or datetime.date.today() != self.file_date:
            return True
        return False

    def get_new_file(self):
        today = datetime.date.today()
        # Create a new file with today's date
        filename = f'{self.filename}.{today.strftime("%Y%m%d")}'
        self.file_date = today
        return open(filename, "a")


def add_numbers(a, b):
    # Add two numbers and return the result - test function
    result = a + b
    return result


async def main():

    # Create a logger object with filename "sum.log"
    logger = Logger("sum.log")
    # Start the logger write loop
    await logger.start()
    # Add two numbers and write the result to the logger
    result = add_numbers(2, 3)
    print("here")
    await logger.write(f"The sum is {result} also")
    print("here")
    # Stop the logger and wait for any outstanding logs to be written
    await logger.stop(wait=True)  # flag stops immediately or after processing


if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()

    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        # If there's already an event loop running, create a task for the main function
        tsk = loop.create_task(main())

    else:
        # If there's no event loop running, create a new one and run the main function
        result = asyncio.run(main())
