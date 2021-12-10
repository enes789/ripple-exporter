# Ripple node exporter for Prometheus

## QuickStart

Clone this repo, fill the .env file and type below command

```
docker-compose up -d
```

Ripple node exporter will give you two metrics;

```
ripple_public_node_current_validated_ledger 6.8246091e+07
ripple_private_node_current_validated_ledger 6.8246091e+07
```


You can custome app.py file to add more metrics.
Don't forget to fill .env file.



