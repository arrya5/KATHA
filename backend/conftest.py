"""pytest bootstrap.

Runs before any test module (and therefore before app.config reads the
environment). We force-disable analytics so the test suite can NEVER write
telemetry into a configured production backend (e.g. a real SUPABASE_URL in
backend/.env). `setdefault` lets an explicit `KATHA_ANALYTICS=1` still opt in
for a deliberate analytics test.
"""
import os

os.environ.setdefault("KATHA_ANALYTICS", "0")
