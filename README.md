# 🚀 LDI Deployment Guide

This guide describes how to deploy the LDI service using Docker and Let's Encrypt with HTTPS support.

---

## 🔧 1. Configure Environment Variables

Create a `.env` file in the project root and define the required variables. For example:

```env
DOMAIN=example.com
EMAIL=your-email@example.com
```
## 🔐 2. Generate SSL Certificate
Run the initialization script to obtain and configure a free Let's Encrypt SSL certificate:

```bash
./init-letsencrypt.sh
```
This script will:
* Download TLS configuration files
* Create a dummy certificate
* Start Nginx to serve the challenge
* Replace the dummy certificate with a real one
* Reload Nginx to apply the new certificate

## 📦 3. Start Services
Bring up the full application stack with:

```bash
docker-compose up -d
```
This will launch all necessary containers, including Nginx and your application.

## 🌐 Access the Application
After setup, your application should be available at:

```arduino
https://your-domain.com
```

## 🛠 Additional Notes
You can re-run init-letsencrypt.sh to renew or reissue certificates.

Ensure ports 80 and 443 are open in your firewall.

For local development, you can skip SSL or use self-signed certificates.

