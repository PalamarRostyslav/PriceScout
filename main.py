import modal
from pricer_service_cls_version import app, Pricer

@app.local_entrypoint()
def main(description: str = "Quadcast HyperX condenser mic, connects via usb-c to your computer for crystal clear audio"):
    """Local entrypoint that calls the Pricer class to get a price estimate."""
    pricer = Pricer()
    print(f"Getting price for: {description}")
    reply = pricer.price.remote(description)
    print(f"Estimated price: ${reply}")
    return reply