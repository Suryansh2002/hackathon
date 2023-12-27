from agents import assistant
from uagents import Bureau

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://localhost:8000/submit", port=8000)
    bureau.add(assistant)
    # This address is needed to communicate with assistant
    print("Address for assistant: ", assistant.address)
    bureau.run()
