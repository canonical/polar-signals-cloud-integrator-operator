# Polar Signals Cloud Integrator for Charms

Represent the Polar Signals Cloud service in your Juju model. Use this charm to configure both
Parca Agent and Parca Server deployments with the endpoints and token they need to send data to
Polar Signals Cloud.

## Example Use

```bash
# Deploy PostgreSQL
juju deploy postgresql --constraints="virt-type=virtual-machine"

# Deploy the parca-agent subordinate
juju deploy parca-agent

# Integrate the agent with PostgreSQL
juju integrate postgresql parca-agent

# Deploy the Polar Signals Cloud Integrator
juju deploy polar-signals-cloud-integrator polar-signals-cloud
juju config polar-signals-cloud bearer-token="<your token>"

# Relate the agent to the cloud integrator
juju integrate parca-agent polar-signals-cloud
```

## Relations

This charm can be related to any application that consumes the `parca_store` relation interface.
