# 🧊 Fallback by Means of Web Caching using NGINX Sidecar

## 📘 Overview

This lab project demonstrates how web caching can be used as a **resilience mechanism** in cloud-native applications. A Flask-based E-Commerce web application is deployed inside a **Kubernetes cluster (Minikube)**, where **NGINX acts as a sidecar proxy** to provide cached responses when the backend is temporarily unavailable. This ensures users get responses even during outages.

## 🎯 Objectives

- Improve application availability and user experience during backend failures.
- Use **NGINX** as a caching sidecar within a Kubernetes Pod.
- Serve **cached static responses** on cache HIT or EXPIRED states.
- Demonstrate fallback patterns in real-world deployment scenarios using **Ngrok for external access**.

## 🧰 Technologies Used

- 🐍 Flask (Python) – Backend application
- 🐋 Docker – Containerization
- ☸️ Kubernetes (Minikube) – Container orchestration
- 🌐 NGINX – Sidecar reverse proxy and web caching layer
- 🧪 SQLite – Lightweight embedded database for orders
- 🌍 Ngrok – Public tunnel to NodePort service
- 🐧 Ubuntu 22.04 LTS on EC2 – Cloud hosting platform

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


---

## ⚙️ Project Components

### 🛍️ Backend App (Flask)

- Displays a product catalog
- Takes orders and saves them in a local SQLite DB
- Uses Jinja templates and static resources

### 🌐 NGINX Sidecar

- Proxies requests to Flask via `proxy_pass`
- Caches successful `200 OK` responses for 10 seconds
- Uses `X-Proxy-Cache` header to expose HIT/MISS/EXPIRED status
- Serves stale cache if Flask backend goes down

### 🗂️ Kubernetes Setup

- **Deployment** with two containers (Flask + NGINX)
- **ConfigMap** for custom NGINX configuration
- **Volumes** for persistent caching directory and config mount
- **NodePort Service** for external access via Minikube IP
- **Ngrok Tunnel** to expose NodePort to public internet

---

## 🛠️ Setup Plan

1. **Launch EC2** and install Docker, Minikube, kubectl
2. **Build Docker image** for Flask app:
   ```bash
   docker build -t flask-ecommerce:latest .

3. **Create ConfigMap** for `nginx.conf`

   ```bash
   kubectl create configmap nginx-config --from-file=nginx.conf
   ```
4. **Deploy Kubernetes manifests**

   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```
5. **Expose service using Ngrok**

   ```bash
   ngrok http <minikube-ip>:31304
   ```

---

## 🧪 Testing Strategy

| Scenario                     | Description                    | Expected Header    |
| ---------------------------- | ------------------------------ | ------------------ |
| First visit                  | Cache is empty                 | `MISS`             |
| Refresh within 10s           | Response from cache            | `HIT`              |
| After 10s                    | Cache revalidated              | `EXPIRED`          |
| Backend killed               | Serve stale cache if available | `HIT` or `EXPIRED` |
| Cache cleared + backend down | Fallback fails                 | `502 Bad Gateway`  |

```bash
curl -I https://<ngrok-url>
```

---

## 🔥 Failure Simulation

* Kill the `flask-app` container from deployment
* Reload the website or run `curl` commands
* Observe fallback behavior with cached content

To clear cache:

```bash
minikube ssh
sudo rm -rf /mnt/nginx-cache/*
```

---

## 📊 Learning Outcomes

* Implemented sidecar caching pattern in Kubernetes
* Demonstrated cache fallback using real-time test cases
* Explored TTL tuning and stale content behavior
* Improved service resilience without load balancers or external CDNs

---

## ❓ Research Questions

* How can stale responses reduce perceived downtime?
* When is fallback via cache appropriate (and when not)?
* How does NGINX handle expired cache during backend unavailability?
* What are the best TTL values for dynamic vs. static apps?

---

## 📈 Future Enhancements

* Dynamic cache invalidation
* Multi-service fallback
* CDN integration with cache headers
* ETag or Last-Modified cache strategies

---

## 👨‍💻 Author

**Sajeeb Chandra Das - Team 05 – Large and Cloud-based Software Systems Lab, TH Cologne**


