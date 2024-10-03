## Intermediate Data Engineer test
### Context
A supermarket stores its transaction data in a relational database for further analysis. The transaction data is uploaded to the system as a CSV file multiple times per day. Each transaction has a unique `id`. As a data engineer, your task is to implement and maintain a pipeline to store the transaction data in the database.

### Elements
For the test, the following elements are provided:
- A sqlite database contains historical transactions data
- A csv file `retail_15_01_2022.csv` contains transaction data of 15/01/2022.
- The tax for all products is 20%.

### Requirements
#### Implement the ETL workflow
Your task is to implement the Python code to store the data from the CSV in the database.

As implementation is only half of the work for a Data Engineer, you're also asked to implement test cases to verify things work as expected. An example of test is provided in the file `test.py`. You need to complete it. Do not hesitate to add more relevant test cases.

#### Explore the data using SQL
After loading the data into the system, the stakeholder wants to extract some information. As a data engineer, you're in charge of the task. Please write the SQL query to answer the following questions:
- What is the number of transactions on 14/01/2022?
```
SELECT COUNT(*) FROM transactions WHERE transaction_date = '2022-01-14';
> 47
```
- What is the total amount, including tax, of all `SELL` transactions?
```
SELECT SUM(amount_inc_tax) FROM transactions WHERE category = 'SELL';
> 360448.98
```
- Consider the product `Amazon Echo Dot`:
  - What is the balance (`SELL` - `BUY`) by date?
```
WITH sell_product AS (
    SELECT
        transaction_date, SUM(amount_inc_tax) AS total_sell
    FROM
        transactions
    WHERE
        name = 'Amazon Echo Dot' AND category = 'SELL'
    GROUP BY
        transaction_date
),
buy_product AS (
    SELECT
        transaction_date, SUM(amount_inc_tax) AS total_buy
    FROM
        transactions
    WHERE
        name = 'Amazon Echo Dot' AND category = 'BUY'
    GROUP BY
        transaction_date
)
SELECT
    COALESCE(s.transaction_date, b.transaction_date) AS transaction_date,
    COALESCE(total_sell, 0) - COALESCE(total_buy, 0) AS balance
FROM
    sell_product s
FULL OUTER JOIN
    buy_product b
ON
    s.transaction_date = b.transaction_date
ORDER BY
    transaction_date;
```
```
2022-01-01|59.98
2022-01-02|-239.9
2022-01-03|-209.91
2022-01-04|-89.96
2022-01-05|-509.79
2022-01-06|59.98
2022-01-07|-149.94
2022-01-08|659.72
2022-01-09|-89.97
2022-01-10|389.84
2022-01-11|-59.97
2022-01-12|-59.98
2022-01-13|-59.98
2022-01-14|-30.0
2022-01-15|239.89
```
  - (Optional) What is the cumulated balance (`SELL` - `BUY`) by date?
```
WITH sell_product AS (
    SELECT
        transaction_date, SUM(amount_inc_tax) AS total_sell
    FROM
        transactions
    WHERE
        name = 'Amazon Echo Dot' AND category = 'SELL'
    GROUP BY
        transaction_date
),
buy_product AS (
    SELECT
        transaction_date, SUM(amount_inc_tax) AS total_buy
    FROM
        transactions
    WHERE
        name = 'Amazon Echo Dot' AND category = 'BUY'
    GROUP BY
        transaction_date
)
SELECT
    COALESCE(s.transaction_date, b.transaction_date) AS transaction_date,
    SUM(COALESCE(total_sell, 0) - COALESCE(total_buy, 0)) 
        OVER (ORDER BY COALESCE(s.transaction_date, b.transaction_date)) 
        AS cumulated_balance
FROM
    sell_product s
FULL OUTER JOIN
    buy_product b
ON
    s.transaction_date = b.transaction_date
ORDER BY
    transaction_date;
```
```
2022-01-01|-59.98
2022-01-02|179.92
2022-01-03|389.83
2022-01-04|479.79
2022-01-05|989.58
2022-01-06|929.6
2022-01-07|1079.54
2022-01-08|419.82
2022-01-09|509.79
2022-01-10|119.95
2022-01-11|179.92
2022-01-12|239.9
2022-01-13|299.88
2022-01-14|329.88
2022-01-15|89.9900000000001
```

#### Deployment (optional)
Of course, the workflow cannot run on the developer's machine, we need to deploy it and automate the process. Can you list the necessary elements of such a system ?
```
Our solution ATM :
- data need to be uploaded multiple time per day (so we imagine at each transaction, the data is uploaded)
- destinate to the analysis
- Sqlite isn't scalable (we have to change this solution)
- Transactions data extracted from a csv

So according to the need and the Well-Architected Framework, we must ensure that :
_the process must be operational,
_data must be secure,
_the infrastructure must be reliable,
_performance must be optimal,
_costs must be controlled.


Transaction: csv / websockets / api

For a AWS cloud infra:
Transaction -> API Gateway -> AWS Lambda -> AWS Glue (ETL) -> AWS SQS (Queue) -> AWS RDS (PostgreSQL) & AWS Backup -> AWS QuickSight (for the analyze/visualisation) -> AWS CloudWatch (Consumption tracking) / AWS IAM (Manage rules)

To avoid limitations with relational and structured databases, we can opt for an AWS solution that can scale horizontally, like AWS RDS, along with PostgreSQL because it's more optimized for big data than MySQL/Sqlite. We can envision that this shop will grow and eventually have multiple locations.

With such a non-complex database, we don’t need multiple clusters in case of a crash (as that would be very expensive for this need). We can simply use AWS Backup to ensure that no data is lost, and wait for RDS to auto-reload. In the event that data is lost (which typically shouldn't happen, but we are very cautious), AWS Backup is here to help us. While the database is down, the messages are stored in a queue, and once the database is back up, the queue will be emptied.

Next, we will use AWS QuickSight for analyzing transactions.

AWS CloudWatch will allow us to monitor the consumption of services as well as their costs.

Manage rules with AWS IAM to control access to the resources.


For a self-hosted infra:
Transaction -> Docker -> Python ETL (sur un VPS) -> Queueing technology (Kafka, RedisMQ) -> PostgreSQL -> DataViz (Tableau / PowerBI / Grafana / Kibana / custom-designed web application...) / hook to pull last commit on master branch

docker-compose.yml:
image: python
python-script: ETL
kafka: ensure availability with multiple nodes
postgresql: schedule automatic backups (with sharding)
dataviz: start instance/web application

everything in "restart: always" to ensure the availability of the data solution.
```

### Evaluation
We look into the following elements:
- The correctness of the solution
- The quality of the code
- Usage of good practices and modern Python
- For the deployment part: The way you reason to choose suitable components for the system 
