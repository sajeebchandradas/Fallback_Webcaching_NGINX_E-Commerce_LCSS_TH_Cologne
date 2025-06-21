# Fallback Web Caching with NGINX Sidecar in Kubernetes

This project is part of the **LCSS Lab** at **TH Cologne**. It demonstrates how to implement **web caching fallback** using **NGINX** as a sidecar proxy in a Kubernetes deployment, serving a Flask-based e-commerce application hosted on an **AWS EC2 Ubuntu instance** with **Minikube**.



## 🚀 Project Overview

When the Flask app backend becomes unavailable, NGINX serves cached content to ensure **high availability** and **improved perceived uptime**. The caching behavior follows HTTP response codes and TTL settings, making use of `HIT`, `MISS`, and `EXPIRED` status headers.

### ✅ Key Features
- Flask E-Commerce Web App with SQLite DB
- Dockerized Backend
- Kubernetes Deployment with Sidecar Pattern
- NGINX Reverse Proxy with Web Caching
- NodePort Service Exposure
- Public Access using Ngrok Tunnel
- Cache Simulation: HIT, MISS, EXPIRED
- Fallback Testing when Flask App Fails



## 📁 Project Structure



.
├── app.py                # Flask application
├── Dockerfile            # Image build config
├── deployment.yaml       # Kubernetes deployment with NGINX sidecar
├── service.yaml          # Kubernetes service (NodePort)
├── nginx.conf            # NGINX caching configuration
├── style.css             # Stylesheet
├── templates/            # HTML templates
│   ├── index.html
│   └── buy.html
└── static/images/        # Product images (e.g., laptop.jpg, tablet.jpg)





## 🛠️ Setup Instructions

### 🔹 1. Launch EC2 and SSH

```bash
ssh -i your-key.pem ubuntu@<your-ec2-public-ip>
````

### 🔹 2. Install Docker

```bash
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker $USER
newgrp docker
```

### 🔹 3. Install Minikube & kubectl

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb

curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### 🔹 4. Start Minikube

```bash
minikube start --driver=docker
minikube ssh
sudo mkdir -p /mnt/nginx-cache && sudo chmod 777 /mnt/nginx-cache
exit
```

---

## 🐳 Build Docker Image

```bash
eval $(minikube docker-env)
docker build -t flask-ecommerce:latest .
```

---

## ⚙️ Create ConfigMap for NGINX

```bash
kubectl create configmap nginx-config --from-file=nginx.conf
```

---

## 🚀 Deploy to Kubernetes

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

## 🌐 Expose Using Ngrok

```bash
ngrok config add-authtoken <your-ngrok-token>
minikube ip   # Example: 192.168.49.2
ngrok http 192.168.49.2:31304
```

Copy the public HTTPS URL and open in browser.

---

## ✅ Test Caching Behavior

```bash
curl -I https://<your-ngrok-url>/ | grep X-Proxy-Cache
```

* First request → `MISS`
* Next request → `HIT`
* After TTL expires (10s) → `EXPIRED`

---

## 🔧 Simulate Backend Failure (Fallback Test)

1. Edit the Deployment to remove Flask container:

```bash
kubectl edit deployment ecommerce-deployment
# Delete the flask-app container section
```

2. Test again:

```bash
curl -I https://<your-ngrok-url>/
```

* You should see stale cache (`HIT` or `EXPIRED`)
* If cache is cleared: `502 Bad Gateway`

---

## ♻️ Clear Cache

```bash
minikube ssh
sudo rm -rf /mnt/nginx-cache/*
exit
```

---

## 🔄 Restore Flask Backend

Re-add the `flask-app` container section to the deployment or:

```bash
kubectl apply -f deployment.yaml
```

Test again:

```bash
curl -I https://<your-ngrok-url>/
```

---

## 📸 Screenshots & Logs

Include:

* Web UI
* Ngrok Terminal Output
* `curl` results showing HIT, MISS, EXPIRED
* 502 Fallback page
* Restored output

---

## 📚 Learning Outcomes

* Sidecar pattern implementation
* Reverse proxy and web caching with NGINX
* Minikube-based local Kubernetes deployment
* Ngrok tunneling for public exposure
* Cache simulation and backend failure fallback

---

## 📧 Contact

For any doubts, feel free to contact me through GitHub issues or \[[email@example.com](mailto:email@example.com)].

---

## 🏁 Final Notes

You have now successfully deployed a **robust web caching system** on Kubernetes using the **sidecar pattern** with fallback capabilities in case of backend service failure.

Happy learning! 🚀

```

---

Let me know if you want this file in `.md` format, zipped with the rest of the project files, or directly pushed to a GitHub repo.
```
