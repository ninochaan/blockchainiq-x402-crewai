"""CrewAI tool for Blockchain IQ's pay-per-call x402 API.

``BlockchainIqFetchTool`` lets a CrewAI agent buy crypto market data from
Blockchain IQ (https://www.blockchainiq.co/agents) one call at a time. The
tool runs the whole x402 v2 flow itself: unpaid call, HTTP 402, EIP-3009
USDC (Base) payment authorization signed with the key in the
``X402_PRIVATE_KEY`` environment variable, paid retry, JSON data back.

Bounty: Blockchain IQ x402 build bounties, CrewAI slot (CrewAI or
Cloudflare Agents) — a public repo with a working paid call to ``brief``
($0.01) or ``event-risk`` ($0.05).
"""

from __future__ import annotations

import json
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from blockchainiq_x402 import BASE_URL, fetch_paid_resource


class BlockchainIqFetchInput(BaseModel):
    """Arguments of the BlockchainIqFetchTool."""

    resource: str = Field(
        default="brief",
        description=(
            "Blockchain IQ resource to fetch: a catalogue name such as "
            "'brief' (market brief, $0.01) or 'event-risk' (scheduled "
            "market-moving events, $0.05), any other path from the free "
            f"catalogue at {BASE_URL} (e.g. '/macro', '/stablecoins'), or a "
            "full URL. Paid resources are paid automatically through x402."
        ),
    )
    max_usdc: float = Field(
        default=0.10,
        description=(
            "Spend guard: refuse to pay if the resource costs more than "
            "this many USDC in a single call."
        ),
    )


class BlockchainIqFetchTool(BaseTool):
    """Fetch Blockchain IQ data, paying per call through x402."""

    name: str = "blockchainiq_fetch"
    description: str = (
        "Fetch crypto market data from Blockchain IQ, paying per call in "
        "USDC on Base through the x402 protocol when the resource is paid. "
        "Use 'brief' for a $0.01 market brief (BTC/ETH/SOL/XRP prices, 48h "
        "events, risk flags) or 'event-risk' for $0.05 scheduled "
        "market-moving events. The payment signing key comes from the "
        "X402_PRIVATE_KEY environment variable. Returns a JSON string with "
        "the data and, for paid calls, the settlement proof."
    )
    args_schema: Type[BaseModel] = BlockchainIqFetchInput

    def _run(self, resource: str = "brief", max_usdc: float = 0.10) -> str:
        result = fetch_paid_resource(resource, max_amount_usd=max_usdc)
        return json.dumps(
            {
                "resource": resource,
                "paid": result.paid,
                "amount_usd": result.amount_usd,
                "settlement": result.settlement,
                "data": result.data,
            }
        )
