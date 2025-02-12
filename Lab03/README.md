# Lab 3

## Team Members
Marco Ebeling
Jaydnne Zane

## Lab Question Answers

Question 1: Why are RESTful APIs scalable?
RESTful APIs are scalable because they are stateless, allowing requests to be processed independently without server-side session storage. This enables efficient load balancing and horizontal scaling. Caching, proxies, and distributed systems are all supported by their layered architecture, which reduces the server load and overall improves performance.


Question 2: According to the definition of "resources" provided in the AWS article above, What are the resources the mail server is providing to clients?
The resources the mail server provides to the client include emails, mailboxes (sent, drafts, inbox), contacts, attachments, user accounts, and various filtering rules. These resources that are provided to the client allow for the retrieval and management of emails along with the ability to send and store messages.


Question 3: What is one common REST Method not used in our mail server? How could we extend our mail server to use this method?
PATCH is a common REST Method not used in our mail servers. It updates a particular resource. We could extend our mail server to use this method by allowing partial updates to emails. For example, we could mark an email as read or unread or update its labels without hindering the entire email resource. 


Question 4: Why are API keys used for many RESTful APIs? What purpose do they serve? Make sure to cite any online resources you use to answer this question!
API keys are used for many RESTful APIs in order to provide authentication, authorization, and usage tracking. They essentially act as unique identifiers assigned to clients, further ensuring that only those authorized can access the API. API keys help control access levels, prevent unauthorized/unwanted users, and monitor usage patterns (which can be used for security or billing purposes). 

Resources:
https://docs.aws.amazon.com/apigateway/latest/developerguide/security-best-practices.html
https://cloud.google.com/apis/docs/troubleshooting

