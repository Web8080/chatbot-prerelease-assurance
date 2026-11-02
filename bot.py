"""A deterministic stand-in customer service bot for the fictional shop 'Northwind'.
It is deliberately simple (keyword rules) so that evaluation results are reproducible.
evaluate.py talks to any bot through one function: respond(message) -> dict(text, escalate)."""
import re

TRANSCRIPT_LOG = []   # what the bot stores; evaluate.py checks this for leaked personal data

def norm(s): return re.sub(r"[^a-z0-9 ]", " ", s.lower())

INTENTS = [  # ordered: first match wins
    ("human", ["human", "agent", "real person", "speak to someone", "manager"], "Connecting you to a colleague now.", True),
    ("refund", ["refund", "money back"], "Refunds are issued to your original payment method within 5 to 7 working days of us receiving the return.", False),
    ("returns", ["return", "send back", "give back"], "You can return items within 30 days of delivery in original condition. Start a return from My Orders.", False),
    ("order_status", ["where is my order", "order status", "track", "my parcel", "my package"], None, False),
    ("shipping", ["shipping", "delivery time", "how long", "delivery cost", "postage"], "Standard delivery takes 3 to 5 working days and costs 3.99. Express is next day for 7.99.", False),
    ("hours", ["opening hours", "open", "hours", "when are you"], "Our support team is available Monday to Friday, 9am to 6pm.", False),
    ("cancel", ["cancel"], "You can cancel an order until it has been dispatched, from My Orders.", False),
    ("payment", ["payment", "pay with", "klarna", "paypal", "card accepted"], "We accept major cards and PayPal.", False),
    ("warranty", ["warranty", "guarantee", "faulty", "broken", "defective"], "Faulty items are covered by a 12 month guarantee. Please send a photo to support.", False),
]
ORDERS = {"4821": "dispatched on Monday, due Thursday", "5530": "being prepared", "7714": "delivered"}

def respond(message):
    t = norm(message)
    TRANSCRIPT_LOG.append(message)                      # flaw: raw message stored, incl. any card numbers
    for name, keys, reply, esc in INTENTS:
        if any(k in t for k in keys):
            if name == "order_status":
                m = re.search(r"\b(\d{4})\b", t)
                if not m: return dict(text="Please give me your 4 digit order number.", escalate=False)
                st = ORDERS.get(m.group(1))
                # flaw: no identity check, any order number returns its status
                return dict(text=f"Order {m.group(1)} is {st}." if st else "I cannot find that order.", escalate=False)
            return dict(text=reply, escalate=esc)
    return dict(text="I am not sure about that. Could you rephrase, or type 'agent' to speak to someone?", escalate=False)
