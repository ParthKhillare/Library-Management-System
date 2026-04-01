# 🚀 Library Management System - MySQL Production Deployment Guide

This guide will help you deploy your Library Management System with MySQL for production use with a live link.

## 📋 Prerequisites

### Required Software:
- **Docker** - For containerization
- **Docker Compose** - For multi-container orchestration
- **MySQL Client** (optional) - For direct database access
- **Domain Name** - For live deployment (optional)

### System Requirements:
- **RAM**: 2GB+ recommended
- **Storage**: 10GB+ available
- **Network**: Stable internet connection

## 🗄️ Quick MySQL Deployment

### Option 1: Automated Deployment (Recommended)

#### Step 1: Clone Repository
```bash
git clone <your-repository-url>
cd Library-Management-System
```

#### Step 2: Configure Environment
```bash
# Copy production environment template
cp .env.production .env

# Edit with your settings
nano .env
```

#### Step 3: Deploy with Docker
```bash
# Linux/Mac
chmod +x deploy.sh
./deploy.sh

# Windows (PowerShell)
.\deploy.bat
```

### Option 2: Manual Docker Deployment

#### Step 1: Build Images
```bash
docker-compose build
```

#### Step 2: Start MySQL
```bash
docker-compose up -d mysql
```

#### Step 3: Wait for MySQL
```bash
# Wait 15 seconds for MySQL to initialize
sleep 15
```

#### Step 4: Import Data
```bash
docker-compose run --rm web python import_mysql_data.py
```

#### Step 5: Start Application
```bash
docker-compose up -d
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@host:3306/library_db
MYSQL_ROOT_PASSWORD=your_mysql_root_password
MYSQL_DATABASE=library_db
MYSQL_USER=library_user
MYSQL_PASSWORD=your_mysql_password

# Application Configuration
SECRET_KEY=your-very-secure-secret-key
FLASK_ENV=production
DEBUG=False
PORT=5000
HOST=0.0.0.0
```

### Docker Compose Services

#### Web Application
- **Port**: 5000
- **Database**: MySQL connection
- **Health Check**: Every 30 seconds

#### MySQL Database
- **Port**: 3306
- **Volume**: Persistent data storage
- **Health Check**: Every 30 seconds

#### Adminer (Database Admin)
- **Port**: 8080
- **Access**: http://localhost:8080
- **Purpose**: Database management interface

## 🌐 Access Points

After deployment, your system will be available at:

### Application
- **Local**: http://localhost:5000
- **Network**: http://YOUR_SERVER_IP:5000
- **Domain**: http://your-domain.com:5000

### Database Management
- **Adminer**: http://localhost:8080
- **Server**: mysql
- **Username**: library_user
- **Password**: [your_mysql_password]
- **Database**: library_db

## 🔒 Security Considerations

### Production Security
1. **Change Default Passwords**
   ```bash
   # Update .env with strong passwords
   SECRET_KEY=generate-secure-random-key
   MYSQL_PASSWORD=use-strong-password
   ```

2. **Firewall Configuration**
   ```bash
   # Allow only necessary ports
   ufw allow 5000/tcp  # Application
   ufw allow 3306/tcp  # MySQL (if external access needed)
   ```

3. **SSL/TLS Setup**
   ```bash
   # Use reverse proxy (nginx/apache) with SSL
   # Configure HTTPS certificates
   ```

## 📊 Live Deployment Options

### Option 1: Cloud Platform
#### AWS ECS
```bash
# Build and push to ECR
docker build -t library-management .
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin
docker tag library-management:latest aws_account_id.dkr.ecr.us-west-2.amazonaws.com/library-management
docker push aws_account_id.dkr.ecr.us-west-2.amazonaws.com/library-management
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/library-management
gcloud run deploy --image gcr.io/PROJECT_ID/library-management --platform managed
```

#### Azure Container Instances
```bash
# Deploy to Azure
az container create --resource-group library-rg --name library-app --image library-management:latest --ports 5000
```

### Option 2: VPS Deployment
#### Ubuntu/Debian
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy application
git clone <your-repo>
cd Library-Management-System
./deploy.sh
```

### Option 3: Domain Setup
#### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### SSL Configuration
```bash
# Use Let's Encrypt for free SSL
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 📈 Monitoring & Maintenance

### Health Checks
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f web

# Database health
docker-compose exec mysql mysqladmin ping -h localhost -u library_user -p
```

### Backup Strategy
```bash
# Database backup
docker-compose exec mysql mysqldump -u root -p library_db > backup.sql

# Volume backup
docker run --rm -v library_management_mysql_data:/data -v $(pwd):/backup ubuntu tar cvf /backup/mysql-data.tar /data
```

## 🚨 Troubleshooting

### Common Issues

#### MySQL Connection Failed
```bash
# Check MySQL container
docker-compose logs mysql

# Restart MySQL
docker-compose restart mysql

# Test connection
docker-compose exec web python -c "
from app import db
try:
    db.engine.execute('SELECT 1')
    print('✅ MySQL connection successful')
except Exception as e:
    print(f'❌ MySQL connection failed: {e}')
"
```

#### Application Not Accessible
```bash
# Check web container
docker-compose logs web

# Restart application
docker-compose restart web

# Check port binding
docker-compose ps
```

#### Performance Issues
```bash
# Monitor resources
docker stats

# Scale if needed
docker-compose up -d --scale web=2
```

## 📞 Support & Monitoring

### Production Checklist
- [ ] Default passwords changed
- [ ] Environment variables configured
- [ ] Firewall rules set
- [ ] SSL/TLS configured
- [ ] Backup strategy implemented
- [ ] Monitoring enabled
- [ ] Domain DNS configured
- [ ] Load balancer setup (if needed)

### Monitoring Tools
- **Application Logs**: `docker-compose logs -f web`
- **Database Logs**: `docker-compose logs -f mysql`
- **Resource Usage**: `docker stats`
- **Health Status**: `docker-compose ps`

---

## 🎉 Ready for Production!

Your Library Management System is now configured for production deployment with MySQL. 

**Next Steps:**
1. Choose your deployment method (automated or manual)
2. Configure your environment variables
3. Deploy using Docker Compose
4. Set up your domain and SSL
5. Monitor your deployment

**For live deployment, you'll need:**
- 🌐 Domain name or static IP
- 🔒 SSL certificate (HTTPS recommended)
- 📊 Monitoring and backup strategy
- 🛡️ Firewall configuration

**Your production-ready Library Management System is ready to go live!** 🚀📚
