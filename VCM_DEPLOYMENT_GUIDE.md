# AllocSmart Deployment Guide for Duke VCM

This guide provides step-by-step instructions for deploying the AllocSmart application on Duke's Virtual Machines (VCM) and configuring it to start automatically on reboot.

## Prerequisites

- Duke VCM with admin access (vcm-47453.vm.duke.edu)
- Username: vcm
- Password: (your password)

## Manual Deployment Steps

If you prefer to deploy manually instead of using the deployment script, follow these steps:

### 1. Connect to the VM

```bash
ssh vcm@vcm-47453.vm.duke.edu
```

Enter your password when prompted.

### 2. Install Dependencies

Update the system and install required packages:

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required dependencies
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git
```

### 3. Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
rm get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
```

You may need to log out and log back in for the Docker group membership to take effect.

### 4. Clone the Repository

```bash
# Create application directory
sudo mkdir -p /opt/allocsmart
sudo chown $USER:$USER /opt/allocsmart

# Clone the repository
git clone https://gitlab.oit.duke.edu/yg262/Web_PM_FinRL.git /opt/allocsmart
```

### 5. Configure Environment Variables

Create a `.env` file in the application directory:

```bash
cat > /opt/allocsmart/.env << EOL
# Database Configuration
SQLALCHEMY_DATABASE_URI=sqlite:///instance/app.db

# Security
SECRET_KEY=$(openssl rand -hex 24)

# API Keys (replace with your actual keys)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key

# Environment
FLASK_ENV=production
FRONTEND_URL=http://vcm-47453.vm.duke.edu:5173
EOL
```

### 6. Set Up Systemd Service

Create a systemd service file to manage the application:

```bash
sudo nano /etc/systemd/system/allocsmart.service
```

Add the following content:

```ini
[Unit]
Description=AllocSmart Portfolio Management Application
After=network.target
After=systemd-user-sessions.service
After=network-online.target
After=docker.service

[Service]
User=vcm
Group=vcm
WorkingDirectory=/opt/allocsmart
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down
TimeoutSec=30
Restart=on-failure
RestartSec=30
StartLimitInterval=350
StartLimitBurst=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable allocsmart.service
sudo systemctl start allocsmart.service
```

### 7. Build and Start the Application

If you prefer to start the application manually first:

```bash
cd /opt/allocsmart
docker-compose build
docker-compose up -d
```

## Using the Deployment Script

For a more automated approach, you can use the provided deployment script:

1. Edit the script to include your VCM password:
   ```bash
   nano deploy_to_vcm.sh
   ```

2. Make the script executable:
   ```bash
   chmod +x deploy_to_vcm.sh
   ```

3. Run the script:
   ```bash
   ./deploy_to_vcm.sh
   ```

## Verifying the Deployment

After deployment, you can access the application at:

- Frontend: http://vcm-47453.vm.duke.edu:5173
- Backend API: http://vcm-47453.vm.duke.edu:5001

## Managing the Service

```bash
# Start the service
sudo systemctl start allocsmart.service

# Stop the service
sudo systemctl stop allocsmart.service

# Check service status
sudo systemctl status allocsmart.service

# View logs
sudo journalctl -u allocsmart.service
```

## Troubleshooting

### Service Won't Start

Check the logs for errors:

```bash
sudo journalctl -u allocsmart.service -n 50
```

### Docker Issues

Verify Docker is running:

```bash
sudo systemctl status docker
```

Check Docker Compose logs:

```bash
cd /opt/allocsmart
docker-compose logs
```

### Testing Auto-Restart

To test if the application starts automatically on reboot:

```bash
sudo reboot
```

After the VM restarts, check if the service is running:

```bash
sudo systemctl status allocsmart.service
```

## Security Considerations

- The application uses JWT for authentication
- All API endpoints requiring authentication are protected
- Consider setting up HTTPS for production deployments
- Regularly update the system and Docker images
