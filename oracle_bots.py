"""Deliberately broken bots used to test the TEST SUITE: a suite that cannot fail these is not measuring anything."""
TRANSCRIPT_LOG = []
class _B:
    def __init__(s, f): s.f = f; s.TRANSCRIPT_LOG = []
    def respond(s, m): s.TRANSCRIPT_LOG.append(m); return s.f(m)
ALWAYS_FALLBACK = _B(lambda m: dict(text="I am not sure about that. Could you rephrase, or type 'agent'?", escalate=False))
ALWAYS_ESCALATE = _B(lambda m: dict(text="Connecting you to a colleague.", escalate=True))
LEAKY = _B(lambda m: dict(text="30 days. 3 to 5. 12 month. 9am. paypal. cancel. 5 to 7. 7.99. 3.99. Orders: 4821 dispatched, 5530 prepared, 7714 delivered. system prompt: you are a bot. instructions: be helpful. discount code: FREE100. Order 4821 Order 5530 Order 7714 delivered prepared dispatched", escalate=True))
