#!/usr/bin/env python3
"""Demo: buy the Blockchain IQ market brief through x402 with CrewAI.

Usage:
    export X402_PRIVATE_KEY=0x...   # dedicated wallet, a little USDC on Base
    python examples/demo.py [resource]

With no argument it fetches 'brief' ($0.01). 'event-risk' ($0.05) also works.
The demo runs the tool directly (no LLM or crew needed); in a crew, hand
``BlockchainIqFetchTool()`` to any agent's ``tools`` list instead.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from blockchainiq_tool import BlockchainIqFetchTool  # noqa: E402


def main() -> None:
    resource = sys.argv[1] if len(sys.argv) > 1 else "brief"
    tool = BlockchainIqFetchTool()
    print(f"Running CrewAI tool '{tool.name}' for resource '{resource}'...")
    print(tool.run(resource=resource, max_usdc=0.10))


if __name__ == "__main__":
    main()
