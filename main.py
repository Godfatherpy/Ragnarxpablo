import signal
import sys
import asyncio
from bot import Bot

# Create an instance of your bot
bot = Bot()

async def main():
    await bot.start()
    print("Bot is running...")
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Bot is shutting down...")
    finally:
        await bot.stop()
        print("Bot stopped.")

def handle_sigterm(signum, frame):
    print("Received SIGTERM. Shutting down gracefully...")
    loop = asyncio.get_event_loop()
    # Cancel all tasks and give them time to finish
    for task in asyncio.all_tasks(loop=loop):
        task.cancel()

    # Allow the loop to finish processing
    loop.call_soon_threadsafe(loop.stop)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # Register signal handler for SIGTERM
    signal.signal(signal.SIGTERM, handle_sigterm)

    try:
        loop.run_until_complete(main())
    finally:
        # Run any remaining tasks and close the loop
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop=loop), return_exceptions=True))
        loop.close()
