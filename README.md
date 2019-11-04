# FrameQL
## Overview
FrameQL is a Declearative language that takes SQL-ish language to perform video analytic

## Structure of FrameQL language
A valid FrameQL program is a ***frameQLstatements***.
*frameQL statements* will consists of multiple ***frameQL statement***.
Each ***frameQLstatement*** can be either ***ddlStatement*** or ***dmlStatement***, *** transactionStatement***
Since FrameQL will be used mainly for video exploratory purpose, we will focus on ***dmlStatement***, specifically, ***selectStatement***.

A ***selectStatement*** will contain ***querySpecification*** that starts with **SELECT**.

Each ***querySepcification*** will take the form of of:
```
     SELECT ***selectSpec*** ***selectElements***
    ***fromClause***  ***errorTolerenceExpression*** ***confLevelExpression***
```

Where ***selectSpec*** can be empty or **DISTINCT**.

***selectElements*** is a list of attribltes from the table returned in ***fromClause***

***fromClause*** will take the form of
```
FROM tableSources WHERE (expressions)
```


###
## How to test Arithmetic Operator

Put your query in test.txt.

Run 
```
python end2end.py --input test.txt
```

## How to test Join Operator

Put your query in joinQuery.txt.

Run 
```
python end2end.py --input joinQuery.txt
```


