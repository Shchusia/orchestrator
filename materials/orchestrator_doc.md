# Orchestartor documentation

[[_TOC_]]

## exc.py


Import exceptions orchestrator


### Class  `UniqueNameException(Exception)`


    Exception for not unique flows
    

##### Function  `UniqueNameException.__init__`

### Class  `NoDateException(Exception)`


    Exception if dict flow is empty
    

##### Function  `NoDateException.__init__`

### Class  `WrongTypeException(Exception)`


    Exception for incorrect inputted types
    

##### Function  `WrongTypeException.__init__`

## orchestrator.py


Orchestrator


### Class  `Orchestrator`


    Orchestrator class for build service
    

#### Class variables

+ `_flows = dict()`

+ `_targets = dict()`

##### Function  `Orchestrator.__init__`

 ``` 
 Init Orchestrator 
 ```

###### **Arguments**:

 + `flows`: `` 

 + `blocks`: `` 

 + `incorrect_messages_handler`: `` 

 + `flow_field`: `` 

 + `block_field`: `` 

 + `log`: `` 

 + `flows_to_ignore`: `List[str]`  names classes to ignore
(Attention) applies only if a module flows is passed

 + `blocks_to_ignore`: `List[str]`  names classes to ignore
(Attention) applies only if a module blocks is passed

##### Function  `Orchestrator._generate_data`

###### decorators

+ @staticmethod

 ``` 
  
 ```

###### **Arguments**:

 + `data_to_process`: `` 

 + `_type_to_compare`: `` 

 + `attribute_to_get`: `` 

 + `names_to_ignore`: `` 

 + `_type_data`: `` 

###### **Returns**:

 

##### Function  `Orchestrator.handle`

 ``` 
  
 ```

###### **Arguments**:

 + `message`: `Message`  message to process

###### **Returns**:

  message if don't have information for processing or incorrect

### exc.py


Flow module exceptions


#### Class  `FlowBlockException(Exception)`


    Class custom exception
    for wrong type of flow block
    

###### Function  `FlowBlockException.__init__`

#### Class  `FlowBuilderException(Exception)`


    Class custom exception
    for wrong types
    

###### Function  `FlowBuilderException.__init__`

### flow.py


Module with Flow


#### Class  `FlowBlock`


    Block for FlowBuilder
    

###### Function  `FlowBlock.__init__`

 ``` 
 Init FlowBlock 
 ```

####### **Arguments**:

 + `obj_block`: ``  type stepBlock

 + `pre_handler_function`: `` 

 + `post_handler_function`: `` 

###### Function  `FlowBlock.init_block`

 ``` 
 Method init instance subclass MainBlock 
 ```

####### **Arguments**:

 + `instance_main`: `` 

####### **Returns**:

  object subclass MainBlock

#### Class  `FlowBuilder`


    Flow building class
    build chain flow from flow blocks
    

###### Function  `FlowBuilder.__init__`

 ``` 
 Init FlowBuilder 
 ```

####### **Arguments**:

 + `step`: `FlowBlock`  first block in flow

###### Function  `FlowBuilder.build_flow`

 ``` 
 Build chain flow for StrategyFlow 
 ```

####### **Arguments**:

 + `instance_main`: `` 

####### **Returns**:

 

#### Class  `Flow`


    Class for inheritance for a specific flow
    

###### Function  `Flow.name_flow`

####### decorators

+ @property

 ``` 
 Name current flow 
 ```

####### **Returns**:

  name flow

###### Function  `Flow.steps_flow`

####### decorators

+ @property

 ``` 
 Steps current flow 
 ```

####### **Returns**:

 

###### Function  `Flow.steps_flow`

####### decorators

+ @<_ast.Name object at 0x0E771330>

 ``` 
 Steps current flow 
 ```

####### **Arguments**:

 + `flow`: `FlowBuilder` empty description

####### **Returns**:

 

###### Function  `Flow.__init__`

 ``` 
 Init Flow 
 ```

###### Function  `Flow.to_go_with_the_flow`

 ``` 
 Method that starts flow execution from the first block 
 ```

####### **Arguments**:

 + `message`: `` 

####### **Returns**:

  None

###### Function  `Flow.get_steps`

 ``` 
 Print steps flow 
 ```

####### **Returns**:

 

### block.py


Module with base class blocks


#### Class  `BlockHandler(ABC)`


    The Handler interface declares a method for building a chain of handlers.
    It also declares a method to fulfill the request.
    

###### Function  `BlockHandler.set_next`

####### decorators

+ @abstractmethod

 ``` 
 method for adding a new handler 
 ```

####### **Arguments**:

 + `handler`: `BlockHandler`  object next handler in chain flow

####### **Returns**:

  BlockHandler

###### Function  `BlockHandler.handle`

####### decorators

+ @abstractmethod

 ``` 
 flow chain management method 
 ```

####### **Arguments**:

 + `message`: `MessageQueue` 

####### **Returns**:

  None

###### Function  `BlockHandler.process`

####### decorators

+ @abstractmethod

 ``` 
 method for executing the logic of a given block
in it, only send messages to other services 
 ```

####### **Arguments**:

 + `message`: `MessageQueue`  msg to process

####### **Returns**:

  None

###### Function  `BlockHandler.get_list_flow`

####### decorators

+ @abstractmethod

 ``` 
 Method return str steps flow 
 ```

####### **Returns**:

  str

#### Class  `Block(BlockHandler)`


    The main class for inheriting the blocks that make up the flow of tasks execution
    

###### Function  `Block.pre_handler_function`

####### decorators

+ @property

 ``` 
 function which call before send to handler 
 ```

####### **Returns**:

 

###### Function  `Block.post_handler_function`

####### decorators

+ @property

 ``` 
 function which call after received from source 
 ```

####### **Returns**:

 

###### Function  `Block.name_block`

####### decorators

+ @property

 ``` 
 Unique name to identify block
for override in subclass   name_block 
 ```

###### Function  `Block.__init__`

 ``` 
 Init Block 
 ```

####### **Arguments**:

 + `pre_handler_function`: ``  function should accept and return objects of type Message
which be run before call method

 + `post_handler_function`: ``  function should accept and return objects of type Message
which be run after got msg from source

###### Function  `Block.set_next`

 ``` 
 Save Next handler after this handler 
 ```

####### **Arguments**:

 + `handler`: `` 

####### **Returns**:

  Optional[BlockHandler, None]

###### Function  `Block.handle`

 ``` 
 Flow chain management method
check step by step 
 ```

####### **Arguments**:

 + `message`: `MessageQueue`  msg to process
in source have name block from which orchestrator get msg

####### **Returns**:

  None

###### Function  `Block.process`

 ``` 
 Method for executing the logic of a given block
in it, only send messages to other services 
 ```

####### **Arguments**:

 + `message`: `` 

####### **Returns**:

 

###### Function  `Block.get_list_flow`

 ``` 
 Method return str flow 
 ```

####### **Returns**:

  str

###### Function  `Block.pre_handler_function`

####### decorators

+ @<_ast.Name object at 0x0E771070>

 ``` 
 function which call before send to handler 
 ```

####### **Arguments**:

 + `func`: `Callable` empty description

####### **Returns**:

 

###### Function  `Block.post_handler_function`

####### decorators

+ @<_ast.Name object at 0x0E7714F0>

 ``` 
 function which call after received from source 
 ```

####### **Arguments**:

 + `func`: `Callable` empty description

####### **Returns**:

 

### exc.py


Flow exceptions module


#### Class  `FlowException(Exception)`


    Class custom exception
    for incorrect type flow
    

###### Function  `FlowException.__init__`

### incorrect.py


a module with a strategy for what to do with
incorrect messages and a default solution


#### Class  `StrategyIncorrectMessages(ABC)`


    class strategy for handling messages of wrong structure
    

###### Function  `StrategyIncorrectMessages.is_process_incorrect_messages`

####### decorators

+ @property

 ``` 
 boolean parameter whether to process invalid messages
True - process
flow - ignore 
 ```

###### Function  `StrategyIncorrectMessages.message_checker`

####### decorators

+ @abstractmethod

 ``` 
 Method for validating messages 
 ```

####### **Arguments**:

 + `message`: `Message`  message to check

####### **Returns**:

  is_correct_message: bool, warning message

###### Function  `StrategyIncorrectMessages.process_incorrect_message`

####### decorators

+ @abstractmethod

 ``` 
 method for handling messages with incorrect structure
save for send report or save to log 
 ```

####### **Arguments**:

 + `message`: `Message`  message to process

####### **Returns**:

  None

#### Class  `IgnoreIncorrectMessage(StrategyIncorrectMessages)`


    Default class if no strategy for handling invalid messages is specified
    

###### Function  `IgnoreIncorrectMessage.is_process_incorrect_messages`

####### decorators

+ @property

###### Function  `IgnoreIncorrectMessage.message_checker`

 ``` 
 consider all messages correct 
 ```

####### **Arguments**:

 + `message`: `Message`  message to check

####### **Returns**:

 

###### Function  `IgnoreIncorrectMessage.process_incorrect_message`

 ``` 
  
 ```

####### **Arguments**:

 + `message`: `Message` empty description

####### **Returns**:

  None

## custom.py


Module with custom msg


### Class  `MessageCustom(Message)`


    Class for build custom messages
    

##### Function  `MessageCustom.__init__`

 ``` 
 Init MessageCustom 
 ```

###### **Arguments**:

 + `body`: `dict` 

 + `header`: `dict` 

## message.py


Module with Base class for orchestrator operation


### Class  `Message`


    Class for working with a received message from the queue
    

#### Class variables

+ `__body = error`

+ `__header = error`

##### Function  `Message.body`

###### decorators

+ @property

 ``` 
 Property class message - body 
 ```

###### **Returns**:

  dict body: message

##### Function  `Message.header`

###### decorators

+ @property

 ``` 
 Property class message - header 
 ```

###### **Returns**:

  dict header: message

##### Function  `Message.body`

###### decorators

+ @<_ast.Name object at 0x0E75BEF0>

 ``` 
 Property class message - body 
 ```

###### **Arguments**:

 + `body`: `None` empty description

###### **Returns**:

  dict body: message

##### Function  `Message.header`

###### decorators

+ @<_ast.Name object at 0x0E75B7B0>

 ``` 
 Property class message - header 
 ```

###### **Arguments**:

 + `header`: `None` empty description

###### **Returns**:

  dict header: message

##### Function  `Message.__init__`

##### Function  `Message.__str__`

##### Function  `Message.print_message`

 ``` 
 Method print message 
 ```

###### **Returns**:

  None

##### Function  `Message.update_body`

 ``` 
 Method add value to body
if a `key` exists, then the date_to_add will be added by this `key`
if the key doesn't exist then date_to_add must be a dictionary
and the current __body will be updated 
 ```

###### **Arguments**:

 + `date_to_add`: `` 

 + `key`: `str` 

###### **Returns**:

  None

##### Function  `Message.update_header`

 ``` 
 Method add value to body
if a `key` exists, then the date_to_add will be added by this `key`
if the key doesn't exist then date_to_add must be a dictionary
and the current __header will be updated 
 ```

###### **Arguments**:

 + `date_to_add`: `` 

 + `key`: `` 

###### **Returns**:

  None

##### Function  `Message.get_body`

 ``` 
 The method returns the body of the message str or dict for future processing 
 ```

###### **Arguments**:

 + `returned_type_str`: `bool`  type string may be needed if send to queue

###### **Returns**:

  body in str or dict type

##### Function  `Message.get_header`

 ``` 
 The method returns the header of the message str or dict for future processing 
 ```

###### **Arguments**:

 + `returned_type_str`: `bool`  type string may be needed if send to rabbit queue

###### **Returns**:

  header in str or dict type

##### Function  `Message.get_source`

 ``` 
  
 ```

###### **Returns**:

 

##### Function  `Message.set_source`

 ``` 
  
 ```

###### **Arguments**:

 + `new_source`: `` 

###### **Returns**:

 