# AllocSmart Deployment Guide

This guide provides instructions for deploying the AllocSmart application on Duke's Virtual Computing Manager (VCM) servers.

## Prerequisites

- Access to a Duke VCM instance (vcm-47453.vm.duke.edu)
- Anaconda or Miniconda installed
- Node.js and npm installed

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://gitlab.oit.duke.edu/yg262/Web_PM_FinRL.git
cd Web_PM_FinRL
```

### 2. Backend Setup

```bash
cd allocsmart/backend

# Create and activate conda environment
conda create -n FinRL python=3.10
conda activate FinRL

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python fix_db.py
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Build the frontend
npm run build
```

### 4. Automatic Startup Configuration

The application is configured to start automatically after system reboot using systemd services.

```bash
# Run the setup script
cd ..
chmod +x setup_vcm.sh
./setup_vcm.sh
```

This script will:
- Initialize the database
- Copy systemd service files to the appropriate location
- Enable and start the services

### 5. Verify Deployment

- Backend API should be accessible at: http://vcm-47453.vm.duke.edu:5003
- Frontend should be accessible at: http://vcm-47453.vm.duke.edu:5174

## Default Users

The setup script creates two default users:

1. Regular User:
   - Username: testuser
   - Password: password123

2. Admin User:
   - Username: admin
   - Password: admin123

## Troubleshooting

### Database Issues

If you encounter database issues, you can reset the database:

```bash
cd allocsmart/backend
python fix_db.py
```

### Service Issues

Check the status of the services:

```bash
sudo systemctl status allocsmart.service
sudo systemctl status allocsmart-frontend.service
```

Restart the services if needed:

```bash
sudo systemctl restart allocsmart.service
sudo systemctl restart allocsmart-frontend.service
```

View logs:

```bash
sudo journalctl -u allocsmart.service
sudo journalctl -u allocsmart-frontend.service
```
