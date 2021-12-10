from flask import Flask, send_file, request, Response
from prometheus_client import start_http_server, Counter, generate_latest, Gauge
import logging
from xrpl.clients import JsonRpcClient
from xrpl.ledger import get_latest_validated_ledger_sequence
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

get_public_node_current_validated_ledger_gauge = Gauge('ripple_public_node_current_validated_ledger', 'The block number of public ripple node.')
get_private_node_current_validated_ledger_gauge = Gauge('ripple_private_node_current_validated_ledger', 'The block number of private ripple node.')


@app.route('/metrics', methods=['GET'])
def get_data():
    """Returns all data as plaintext."""

    PUBLIC_NODE = os.environ.get("PUBLIC_NODE")
    PRIVATE_NODE = os.environ.get("PRIVATE_NODE")

    public_client = JsonRpcClient(PUBLIC_NODE)
    private_client = JsonRpcClient(PRIVATE_NODE)


    public_node_current_validated_ledger = get_latest_validated_ledger_sequence(public_client)
    private_node_current_validated_ledger = get_latest_validated_ledger_sequence(private_client)


    try:
        get_public_node_current_validated_ledger_gauge.set(public_node_current_validated_ledger)
        get_private_node_current_validated_ledger_gauge.set(private_node_current_validated_ledger)

    except Exception as e:
        logger.error("Failed to get balance metric. Exception: {}".format(e))

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')