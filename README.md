# 🚀 Ansible Monitoring Stack

Production-ready Ansible project to deploy:

* Prometheus
* Grafana
* Alertmanager
* Node Exporter

---

# 📂 Project Structure

```
monitoring-stack/
├── inventory.ini
├── playbook.yml
├── README.md
└── roles/
    ├── common/
    ├── prometheus/
    ├── alertmanager/
    ├── grafana/
    └── node_exporter/
```

---

# ⚙️ Prerequisites

* Ansible >= 2.9
* Ubuntu 3 servers
* ansible server  need t3.micro 
* grafna promethous node t3.medium and storage 30 gb min
* node server t2.micro or t3.medium   and storage 30 gb min
* SSH access with sudo privileges

---

# 🖥️ Inventory Setup

Edit `inventory.ini`:

```
[monitor]
monitor1 ansible_host=YOUR_MONITOR_IP

[nodes]
node1 ansible_host=NODE_IP_1      ## grafana promethoous ip
node2 ansible_host=NODE_IP_2       ### node server ip
```
#  ssh keys 

```
ssh-keygen -t rsa
````
- update the public key in both servers authorized file in .ssh
- run the ping commnd
```
ansible all -m ping -i inventory.ini
```
---

# ▶️ Run Deployment

```
ansible-playbook -i inventory.ini playbook.yml
```

---

# 🌐 Access Services

| Service       | URL                           |
| ------------- | ----------------------------- |
| Prometheus    | http://<monitor-ip>:9090      |
| Grafana       | http://<monitor-ip>:3000      |
| Node Exporter | http://<node-ip>:9100/metrics |

---

# 🔐 Default Credentials

Grafana:

* Username: admin
* Password: admin

⚠️ Change password after first login.

---

# 📊 Features

* Centralized monitoring node
* Distributed node exporters
* Alertmanager integration
* PagerDuty ready
* EC2 Service Discovery support
* Idempotent Ansible roles

---

# 🧠 Best Practices Implemented

## 1. Idempotency

Roles ensure repeated runs do not break setup.

## 2. Role-Based Design

Each component is modular and reusable.

## 3. Security

* Dedicated system users
* No root execution for services

## 4. Scalability

Add nodes easily in inventory.

## 5. Separation of Concerns

Each role handles only one responsibility.

---

# 🔧 Customization

## Change AWS Region and your node tag name
## also add iam role to grafana prometheous server

Edit:

```
roles/prometheus/templates/prometheus.yml.j2
```

## Add More Nodes

Update inventory file only.

## Update PagerDuty Key

Edit:

```
roles/alertmanager/tasks/main.yml
```

---


# 📦 Future Enhancements

* Grafana dashboards auto import
* Slack/Email alerts
* TLS (HTTPS)
* Kubernetes Helm deployment
* Docker-based setup

---


## run cmd

```
ansible-playbook -i inventory.ini  playbook.yml
```


# ❗ Troubleshooting

## Check Service Status

```
systemctl status prometheus
systemctl status grafana-server
systemctl status alertmanager
systemctl status node_exporter
```

---

# 👨‍💻 Author

DevOps Monitoring Project

---

# ⭐ Use Case

Perfect for:

* DevOps Engineers
* SREs
* Monitoring setups in AWS
* Interview projects

---

# 🎯 Resume Point

"Implemented centralized monitoring using Prometheus, Grafana, and Alertmanager with Ansible automation and EC2 service discovery."
