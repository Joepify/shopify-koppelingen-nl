#!/usr/bin/env python3
"""verify_shopify_webhook: controleer de HMAC-handtekening van een Shopify-webhook.

Shopify tekent elke webhook met HMAC-SHA256 over de ruwe body, base64-gecodeerd, in de
header X-Shopify-Hmac-Sha256. Gebruik de ruwe bytes van de body, niet opnieuw geserialiseerde JSON.

    from verify_shopify_webhook import verify
    ok = verify(raw_body_bytes, header_value, app_secret)

Zelftest:  python3 verify_shopify_webhook.py --test
Alleen standaardbibliotheek. Gemaakt door Joepify (https://www.joepify.nl), MIT-licentie.
"""
import base64, hashlib, hmac, sys


def sign(body: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("ascii")


def verify(body: bytes, header_value: str, secret: str) -> bool:
    """True als de handtekening klopt. Vergelijkt in constante tijd."""
    if not header_value:
        return False
    return hmac.compare_digest(sign(body, secret), header_value.strip())


def _selftest() -> int:
    secret = "geheim"
    body = b'{"id":1001,"total_price":"24.95"}'
    good = sign(body, secret)
    checks = [
        ("geldige handtekening", verify(body, good, secret), True),
        ("gewijzigde body", verify(body + b" ", good, secret), False),
        ("verkeerd geheim", verify(body, good, "ander"), False),
        ("lege header", verify(body, "", secret), False),
    ]
    bad = 0
    for naam, got, want in checks:
        status = "OK" if got == want else "FOUT"
        bad += got != want
        print(f"{status:<5} {naam}")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
