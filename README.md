# AWS Resource Management Portal 🌐

## Overview 📄

This project is a Flask-based web application designed to help developers manage AWS resources, including EC2 instances, S3 buckets, and Route 53 domains. The application provides an intuitive web interface for performing operations such as creating, modifying, and deleting cloud resources.

## Features 🚀

### EC2 Management 🖥️:

- Create EC2 instances with custom configurations.
- Start, stop, and restart instances.
- View a list of existing instances.


![EC2](gifs/ec2.gif)


### S3 Bucket Management 🗂️:

- Create S3 buckets with configurable access settings.
- Upload files to an S3 bucket.
- List all existing S3 buckets.
- Delete S3 buckets and their contents.


![S3](gifs/s3.gif)



### Route 53 Domain Management 🌍:

- Create hosted zones (domains).
- Manage DNS records (add/delete records).
- Fetch hosted zone details.
- Delete hosted zones.



![Route 53](gifs/route53.gif)



## Technologies Used 🛠️

- **Backend:** Flask (Python)
- **AWS Services:** EC2, S3, Route 53
- **Infrastructure as Code:** Pulumi
- **Templating Engine:** Jinja2 (for rendering HTML templates)
- **Deployment:** Docker (optional), AWS EC2 (for hosting the application)

## Installation and Setup ⚙️

### Prerequisites 🔑

Ensure you have the following installed:

- Python 3 🐍
- Flask ⚡
- AWS CLI (configured with valid credentials)
- Pulumi 🛠️
- Boto3 (Python SDK for AWS)
- Git (for cloning the repository)

### Clone the Repository 💻

```bash
git clone https://github.com/guytamari/aws-resource-management.git
cd aws-resource-management
```

### Install Dependencies 📥

```bash
pip install -r requirements.txt
```

### Set Up AWS Credentials 🏞️

Ensure you have AWS credentials configured using:

```bash
aws configure
```

### Run the Application 🚶

```bash
python main.py
```

The application will be accessible at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Usage 📝

### EC2 Management 🖥️

- Navigate to the EC2 section (/ec2).
- Create an instance by specifying instance type, AMI, tags, and quantity.
- Start, stop, or restart instances from the web interface.

### S3 Management 🗂️

- Navigate to the S3 section (/s3).
- Create an S3 bucket with a specified name and access type.
- Upload files to a bucket.
- View and delete existing buckets.

### Route 53 Management 🌍

- Navigate to the Route 53 section (/route53).
- Create a new hosted zone (domain).
- Manage DNS records (add/delete records).
- Delete hosted zones if necessary.

## API Endpoints 🌐

### EC2 Endpoints 🖥️

| Endpoint         | Method | Description               |
| ---------------- | ------ | ------------------------- |
| `/create-ec2`    | POST   | Create a new EC2 instance |
| `/ec2/instances` | GET    | Get list of EC2 instances |
| `/ec2/start`     | POST   | Start an EC2 instance     |
| `/ec2/stop`      | POST   | Stop an EC2 instance      |
| `/ec2/restart`   | POST   | Restart an EC2 instance   |

### S3 Endpoints 🗂️

| Endpoint      | Method | Description               |
| ------------- | ------ | ------------------------- |
| `/create-s3`  | POST   | Create a new S3 bucket    |
| `/s3/buckets` | GET    | Fetch existing S3 buckets |
| `/s3/delete`  | POST   | Delete an S3 bucket       |
| `/s3/upload`  | POST   | Upload a file to S3       |

### Route 53 Endpoints 🌍

| Endpoint                 | Method | Description                 |
| ------------------------ | ------ | --------------------------- |
| `/route53/zones`         | GET    | Fetch existing hosted zones |
| `/route53/add-record`    | POST   | Add a DNS record            |
| `/route53/delete-record` | POST   | Delete a DNS record         |
| `/route53/delete-zone`   | POST   | Delete a hosted zone        |

## Deployment 🚀

### Running with Docker 🐳

You can also run the application inside a Docker container:

```bash
docker build -t aws-resource-management .
docker run -p 5000:5000 aws-resource-management
```

### Deploying to AWS EC2 ☁️

- Launch an EC2 instance.
- Install dependencies (Flask, Pulumi, AWS CLI, etc.).
- Clone the repository and run `python main.py`.
- Use an Nginx reverse proxy for production deployment.
