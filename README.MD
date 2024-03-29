## ``orchestrator`` - convenient configuration of interaction between services in microservice architecture

### Installation

```commandline
pip install orchestrator-service
```

### Problem

The application has a lot of services for performing tasks. Each service performs its own task. Different services bundles are used to perform different tasks.

<u>Example:</u>

Task | Service execution sequence 
--- | --- 
*Task1* | service1 -> service2 -> service3
*Task2* | service2 -> service4 -> service1
*...* | ...
*TaskN* | service3 -> service2 -> ... -> serviceM
    
In order to centralized control the permissible sequence of execution of services for different tasks, we offer you an orchestrator.

![file not found](./materials/solution_application_diagram.png "solution_application_diagram")

<u>Pros:</u>
* centralized control
* easy expansion
* easy setup
* reuse of services in different tasks

<u>What is needed to be implemented in current architectures</u>
* implement block for the corresponding service
* add a `source` to messages (the name of the service to which the corresponding block in the orchestrator should be)
* add a `flow` to messages (similarly as the source)
* redefine blocks for the desired type of queue

<u>Bonus:</u>
* service for build microservice architecture.

<u>Future plans:</u>
* add async functions to orchestrator
* add handler for incorrect messages to service


[more details in examples](https://github.com/Shchusia/orchestrator/blob/develop/examples)
