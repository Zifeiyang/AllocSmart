# AllocSmart Deployment Guide

This guide provides instructions for deploying the AllocSmart application on Duke's Virtual Machines (vcm-47453.vm.duke.edu).

## Prerequisites

- Access to the Duke VM (vcm-47453.vm.duke.edu)
- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://gitlab.oit.duke.edu/yg262/Web_PM_FinRL.git
cd Web_PM_FinRL
```

### 2. Set Up the Backend

```bash
cd allocsmart/backend
pip install -r requirements.txt
flask db upgrade

# Create admin account if it doesn't exist
python create_admin.py
```

### 3. Set Up the Frontend

```bash
cd ../frontend
npm install
```

### 4. Configure Systemd Services

Copy the service files to the systemd directory:

```bash
sudo cp allocsmart-backend.service /etc/systemd/system/
sudo cp allocsmart-frontend.service /etc/systemd/system/
```

Update the paths in the service files to match your installation directory.

### 5. Enable and Start the Services

```bash
sudo systemctl daemon-reload
sudo systemctl enable allocsmart-backend.service
sudo systemctl enable allocsmart-frontend.service
sudo systemctl start allocsmart-backend.service
sudo systemctl start allocsmart-frontend.service
```

### 6. Verify the Services

```bash
sudo systemctl status allocsmart-backend.service
sudo systemctl status allocsmart-frontend.service
```

## Accessing the Application

- Backend API: [http://vcm-47453.vm.duke.edu:5003](http://vcm-47453.vm.duke.edu:5003)
- Frontend: [http://vcm-47453.vm.duke.edu:5173](http://vcm-47453.vm.duke.edu:5173)

## Troubleshooting

### Checking Logs

```bash
sudo journalctl -u allocsmart-backend.service
sudo journalctl -u allocsmart-frontend.service
```

### Restarting Services

```bash
sudo systemctl restart allocsmart-backend.service
sudo systemctl restart allocsmart-frontend.service
```

## Admin Account

The application has an admin account with the following credentials:

- Username: admin
- Password: admin123

This account has access to additional administrative features.
