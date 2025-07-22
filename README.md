# RSS Data Processing Pipeline

A learning project focused on building an end-to-end data pipeline using Terraform, Python, and cloud data lake technologies to process and analyze RSS feed data.

## 🎯 Project Objectives

This project serves as a hands-on learning experience for:
- **Infrastructure as Code**: Using Terraform to provision and manage cloud infrastructure
- **Data Processing**: Analyzing RSS feeds with Python
- **Data Engineering**: Building ETL pipelines to process and load data into a data lake
- **Cloud Technologies**: Working with GCP

## 🏗️ Architecture Overview

```
RSS Sources → Python Scraper → Data Processing → Data Lake Storage → Analytics
                     ↑                                  ↑
                     └──────── Terraform IaC ───────────┘
```

## 🛠️ Technologies Used

- **Infrastructure**: Terraform
- **Programming Language**: Python
- **Data Processing**: 
  - RSS feed parsing (feedparser)
  - Data transformation (pandas)
- **Storage**: Google Cloud Storage

## 📁 Project Structure

```
data_rss/
├── Infrastructure/        # Infrastructure as Code
│   ├── main.tf            # Main Terraform configuration
│   ├── variables.tf       # Variable definitions
├── function/                   # Cloud function source
│   ├── correct_r_code.py       # janitor RSS R files
│   ├── main.py                 # main python file run by the function
│   ├── requirements.txt       # python package use
└── README.md             # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Terraform 6.0+
- GCP account
- Git


## 📊 Data Pipeline Components

### 1. RSS Feed Extraction
- Fetches RSS feeds from configured sources
- Parses RSS content

### 2. Data Transformation
- Cleans and normalizes feed data
- Extracts relevant fields (title, description, published date, etc.)
- Enriches data with metadata

### 3. Data  Loading
- Load the strucutre data in BigQuery
- Load the unstrucutre data (R program) in google cloud storage





## 🏃 Running the Pipeline

### Deploy Infrastructure
```bash
cd Infrastructure
terraform plan
terraform apply
```



### Schedule Regular Runs
For production use, consider scheduling with:
- Cron jobs
- Cloud Scheduler




## 📚 Learning Resources

### Terraform
- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices)

### RSS Processing
- [Python feedparser Documentation](https://feedparser.readthedocs.io/)
- [RSS 2.0 Specification](https://www.rssboard.org/rss-specification)



## 👤 Author

**François Lenne**
- GitHub: [@Francois-lenne](https://github.com/Francois-lenne)
- Location: Lille, France

## 🎓 Learning Progress

- [x] Set up project structure
- [x] Implement RSS feed parser
- [x] Create Terraform infrastructure
- [x] Build data transformation pipeline
- [x] Deploy to cloud data lake

---

**Note**: This is an educational project designed to learn about modern data engineering practices. Feel free to adapt and extend it for your own learning journey!
