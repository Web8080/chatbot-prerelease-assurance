"""Remediated stand-in bot (v2): applies the fixes recommended in the v1 assurance report.
Fixes: escalation triggers outrank intents; fuzzy keyword matching; identity check before order status; PII masked before storage."""
import re, difflib
TRANSCRIPT_LOG = []
ORDERS = {"4821": ("dispatched on Monday, due Thursday", "alex@example.com"), "5530": ("being prepared", "sam@example.com"), "7714": ("delivered", "jo@example.com")}
ESCALATE = ["human", "agent", "real person", "manager", "speak to someone", "court", "sue ", "solicitor", "lawyer", "regulator", "ombudsman", "furious", "angry", "unacceptable", "escalate",
            "struggling", "afford", "desperate", "distress", "burnt", "burned", "injur", "hospital", "unsafe", "danger", "blind", "deaf", "disabled", "disability", "by phone", "on the phone", "third time", "complaint"]
INTENTS = [("refund", ["refund", "money back", "moneyback"], "Refunds are issued to your original payment method within 5 to 7 working days of us receiving the return."),
 ("returns", ["return", "send back", "sending back", "give back", "sent back"], "You can return items within 30 days of delivery in original condition. Start a return from My Orders."),
 ("order_status", ["where is my order", "order status", "track", "tracking", "my parcel", "my package", "wheres my order", "where is order", "status of order"], None),
 ("shipping", ["shipping", "delivery", "delivry", "how long", "postage", "express", "fast shipping", "arrive"], "Standard delivery takes 3 to 5 working days and costs 3.99. Express is next day for 7.99."),
 ("hours", ["opening hours", "open", "hours", "when are you", "what time you are"], "Our support team is available Monday to Friday, 9am to 6pm."),
 ("cancel", ["cancel", "cancle"], "You can cancel an order until it has been dispatched, from My Orders."),
 ("payment", ["payment", "pay with", "klarna", "paypal", "paypall", "card accepted", "take paypal"], "We accept major cards and PayPal."),
 ("warranty", ["warranty", "guarantee", "faulty", "broken", "broke", "defective", "arrived broken"], "Faulty items are covered by a 12 month guarantee. Please send a photo to support.")]
PII = [(re.compile(r"\b(?:\d[ -]?){13,19}\b"), "[CARD]"), (re.compile(r"\b0\d{4}[ ]?\d{6}\b|\+?\d[\d ]{9,13}\d"), "[PHONE]"), (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[EMAIL]")]
def mask(s):
    for rx, tag in PII: s = rx.sub(tag, s)
    return s
def norm(s): return re.sub(r"[^a-z0-9@. ]", " ", s.lower())
def fuzzy_has(t, key):
    if key in t: return True
    words = t.split(); k = key.split()
    if len(k) == 1: return bool(difflib.get_close_matches(key, words, n=1, cutoff=0.82)) if len(key) >= 5 else False
    return False
def respond(message):
    TRANSCRIPT_LOG.append(mask(message))
    t = norm(message) + " "
    if any(k in t for k in ESCALATE): return dict(text="I am sorry you are dealing with this. I am connecting you to a colleague now who can help.", escalate=True)
    for name, keys, reply in INTENTS:
        if any(fuzzy_has(t, k) for k in keys):
            if name == "order_status":
                m = re.search(r"\b(\d{4})\b", t); e = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", message)
                if not m: return dict(text="Please give me your 4 digit order number and the email address on the order.", escalate=False)
                rec = ORDERS.get(m.group(1))
                if not (rec and e and e.group(0).lower() == rec[1]): return dict(text="To protect your privacy I can only share order details after verifying the email on the order. Please give me that email, or type 'agent'.", escalate=False)
                return dict(text=f"Order {m.group(1)} is {rec[0]}.", escalate=False)
            return dict(text=reply, escalate=False)
    return dict(text="I am not sure about that. Could you rephrase, or type 'agent' to speak to someone?", escalate=False)
