# __init__.py

## Importing

# exc.py

## import all except classes

## __init__.py

### Importing classes

## exc.py

### Import exceptions orchestrator

### Class  `UniqueNameException(Exception)`

`Exception for not unique flows`

#### Function `UniqueNameException.__init__`

##### **Arguments**:

+ `not_unique_flow_name`: str

+ `_type`: str

### Class  `NoDateException(Exception)`

`Exception if dict flow is empty`

#### Function `NoDateException.__init__`

##### **Arguments**:

+ `_type`: unknown

### Class  `WrongTypeException(Exception)`

`Exception for incorrect inputted types`

#### Function `WrongTypeException.__init__`

##### **Arguments**:

+ `variable`: str

+ `type_variable`: str

## orchestrator.py

### Orchestrator

### Class  `Orchestrator`

`Orchestrator class for build service`

##### Class variables

+ `_flows` = dict(): object

+ `_targets` = dict(): object

#### Function `Orchestrator.__init__`

 ``` 
 Init Orchestrator 
 ```

##### **Arguments**:

 + `flows`: `Union[ModuleType,List]` - empty description

 + `blocks`: `Union[ModuleType,List]` - empty description

 + `incorrect_messages_handler`: `StrategyIncorrectMessages` - empty description

 + `flow_field`: `str` - empty description

 + `block_field`: `str` - empty description

 + `log`: `Logger` - empty description

 + `flows_to_ignore`: `List[str]` -  names classes to ignore
(Attention) applies only if a module flows is passed

 + `blocks_to_ignore`: `List[str]` -  names classes to ignore
(Attention) applies only if a module blocks is passed

#### Function `Orchestrator._generate_data`

##### **Arguments**:

 + `data_to_process`: `Union[ModuleType,List]` - empty description

 + `_type_to_compare`: `type` - empty description

 + `attribute_to_get`: `str` - empty description

 + `names_to_ignore`: `List[str]` - empty description

 + `_type_data`: `str` - empty description

###### Decorators

+ @staticmethod

###### Declared returns: `Dict`

#### Function `Orchestrator.handle`

##### **Arguments**:

 + `message`: `Message` -  message to process

##### **Returns**:

```console

 message if don't have information for processing or incorrect

```

###### Declared returns: `Optional[Message]`

### __init__.py

#### importing flow classes

### exc.py

#### Flow module exceptions

#### Class  `FlowBlockException(Exception)`

`Class custom exception
for wrong type of flow block`

##### Function `FlowBlockException.__init__`

###### **Arguments**:

+ `message`: str

#### Class  `FlowBuilderException(Exception)`

`Class custom exception
for wrong types`

##### Function `FlowBuilderException.__init__`

###### **Arguments**:

+ `message`: str

### flow.py

#### Module with Flow

#### Class  `FlowBlock`

`Block for FlowBuilder`

###### Class variables

+ `obj_block`: unknown = None: none

##### Function `FlowBlock.__init__`

 ``` 
 Init FlowBlock 
 ```

###### **Arguments**:

 + `obj_block`: `unknown` -  type stepBlock

 + `pre_handler_function`: `unknown` - empty description

 + `post_handler_function`: `unknown` - empty description

##### Function `FlowBlock.init_block`

 ``` 
 Method init instance subclass MainBlock 
 ```

###### **Arguments**:

 + `instance_main`: `Flow` - empty description

###### **Returns**:

```console

 object subclass MainBlock

```

####### Declared returns: `Block`

#### Class  `FlowBuilder`

`Flow building class
build chain flow from flow blocks`

##### Function `FlowBuilder.__init__`

 ``` 
 Init FlowBuilder 
 ```

###### **Arguments**:

 + `step`: `FlowBlock` -  first block in flow

##### Function `FlowBuilder.build_flow`

 ``` 
 Build chain flow for StrategyFlow 
 ```

###### **Arguments**:

 + `instance_main`: `Flow` - empty description

####### Declared returns: `Block`

#### Class  `Flow`

`Class for inheritance for a specific flow`

###### Class variables

+ `flow_chain`: unknown = None: none

##### Function `Flow.name_flow`

 ``` 
 Name current flow 
 ```

###### **Returns**:

```console

 name flow

```

####### Decorators

+ @property

##### Function `Flow.steps_flow`

 ``` 
 Steps current flow 
 ```

####### Decorators

+ @property

##### Function `Flow.steps_flow`

 ``` 
 check the set value to property `steps_flow` value 
 ```

###### **Arguments**:

 + `flow`: `FlowBuilder` -  builder flow for current flow

###### **Returns**:

```console

 None or exception

```

####### Decorators

+ @steps_flow.setter

##### Function `Flow.__init__`

 ``` 
 Init Flow 
 ```

##### Function `Flow.to_go_with_the_flow`

 ``` 
 Method that starts flow execution from the first block 
 ```

###### **Arguments**:

 + `message`: `Message` - empty description

###### **Returns**:

```console

 None

```

##### Function `Flow.get_steps`

 ``` 
 Print steps flow 
 ```

####### Declared returns: `str`

### __init__.py

#### import block

### block.py

#### Module with base class blocks

#### Class  `BlockHandler(ABC)`

`The Handler interface declares a method for building a chain of handlers.
It also declares a method to fulfill the request.`

##### Function `BlockHandler.set_next`

 ``` 
 method for adding a new handler 
 ```

###### **Arguments**:

 + `handler`: `BlockHandler` -  object next handler in chain flow

###### **Returns**:

```console

 BlockHandler

```

####### Decorators

+ @abstractmethod

####### Declared returns: `BlockHandler`

##### Function `BlockHandler.handle`

 ``` 
 flow chain management method 
 ```

###### **Arguments**:

 + `message`: `Message` - empty description

###### **Returns**:

```console

 None

```

####### Decorators

+ @abstractmethod

####### Declared returns: `Optional[Exception]`

##### Function `BlockHandler.process`

 ``` 
 method for executing the logic of a given block
in it, only send messages to other services 
 ```

###### **Arguments**:

 + `message`: `Message` -  msg to process

###### **Returns**:

```console

 None

```

####### Decorators

+ @abstractmethod

##### Function `BlockHandler.get_list_flow`

 ``` 
 Method return str steps flow 
 ```

###### **Returns**:

```console

 str

```

####### Decorators

+ @abstractmethod

####### Declared returns: `str`

#### Class  `Block(BlockHandler)`

`The main class for inheriting the blocks that make up the flow of tasks execution`

###### Class variables

+ `_next_handler`: unknown = None: none

+ `_pre_handler_function`: unknown = None: none

+ `_post_handler_function`: unknown = None: none

##### Function `Block.pre_handler_function`

 ``` 
 function which call before send to handler 
 ```

####### Decorators

+ @property

##### Function `Block.post_handler_function`

 ``` 
 function which call after received from source 
 ```

####### Decorators

+ @property

##### Function `Block.name_block`

 ``` 
 Unique name to identify block
for override in subclass   name_block 
 ```

####### Decorators

+ @property

##### Function `Block.__init__`

 ``` 
 Init Block 
 ```

###### **Arguments**:

 + `pre_handler_function`: `Callable` -  function should accept and return objects of type Message
which be run before call method

 + `post_handler_function`: `Callable` -  function should accept and return objects of type Message
which be run after got msg from source

##### Function `Block.set_next`

 ``` 
 Save Next handler after this handler 
 ```

###### **Arguments**:

 + `handler`: `BlockHandler` - empty description

###### **Returns**:

```console

 Optional[BlockHandler, None]

```

####### Declared returns: `Optional[BlockHandler,]`

##### Function `Block.handle`

 ``` 
 Flow chain management method
check step by step 
 ```

###### **Arguments**:

 + `message`: `Message` -  msg to process
in source have name block from which orchestrator get msg

###### **Returns**:

```console

 None

```

##### Function `Block.process`

 ``` 
 Method for executing the logic of a given block
in it, only send messages to other services 
 ```

###### **Arguments**:

 + `message`: `Message` - empty description

##### Function `Block.get_list_flow`

 ``` 
 Method return str flow 
 ```

###### **Returns**:

```console

 str

```

####### Declared returns: `str`

##### Function `Block.pre_handler_function`

###### **Arguments**:

+ `func`: Callable

####### Decorators

+ @pre_handler_function.setter

##### Function `Block.post_handler_function`

###### **Arguments**:

+ `func`: Callable

####### Decorators

+ @post_handler_function.setter

### exc.py

#### Flow exceptions module

#### Class  `FlowException(Exception)`

`Class custom exception
for incorrect type flow`

##### Function `FlowException.__init__`

###### **Arguments**:

+ `message`: str

### __init__.py

#### Importing module

### incorrect.py

#### a module with a strategy for what to do with
incorrect messages and a default solution

#### Class  `StrategyIncorrectMessages(ABC)`

`class strategy for handling messages of wrong structure`

##### Function `StrategyIncorrectMessages.is_process_incorrect_messages`

 ``` 
 boolean parameter whether to process invalid messages
True - process
flow - ignore 
 ```

####### Decorators

+ @property

##### Function `StrategyIncorrectMessages.message_checker`

 ``` 
 Method for validating messages 
 ```

###### **Arguments**:

 + `message`: `Message` -  message to check

###### **Returns**:

```console

 is_correct_message: bool, warning message

```

####### Decorators

+ @abstractmethod

####### Declared returns: `Tuple[bool,Any]`

##### Function `StrategyIncorrectMessages.process_incorrect_message`

 ``` 
 method for handling messages with incorrect structure
save for send report or save to log 
 ```

###### **Arguments**:

 + `message`: `Message` -  message to process

###### **Returns**:

```console

 None

```

####### Decorators

+ @abstractmethod

#### Class  `IgnoreIncorrectMessage(StrategyIncorrectMessages)`

`Default class if no strategy for handling invalid messages is specified`

##### Function `IgnoreIncorrectMessage.is_process_incorrect_messages`

####### Decorators

+ @property

##### Function `IgnoreIncorrectMessage.message_checker`

 ``` 
 consider all messages correct 
 ```

###### **Arguments**:

 + `message`: `Message` -  message to check

####### Declared returns: `Tuple[bool,Any]`

##### Function `IgnoreIncorrectMessage.process_incorrect_message`

###### **Arguments**:

 + `message`: `Message` - empty description

###### **Returns**:

```console

 None

```

## __init__.py

### Importing clases

## custom.py

### Module with custom msg

### Class  `MessageCustom(Message)`

`Class for build custom messages`

#### Function `MessageCustom.__init__`

 ``` 
 Init MessageCustom 
 ```

##### **Arguments**:

 + `body`: `dict` - empty description

 + `header`: `dict` - empty description

## exc.py

## message.py

### Module with Base class for orchestrator operation

### Class  `Message`

`Class for working with a received message from the queue`

##### Class variables

+ `__body` = None: none

+ `__header` = None: none

#### Function `Message.body`

 ``` 
 Property class message - body 
 ```

##### **Returns**:

```console

 dict body: message

```

###### Decorators

+ @property

#### Function `Message.header`

 ``` 
 Property class message - header 
 ```

##### **Returns**:

```console

 dict header: message

```

###### Decorators

+ @property

#### Function `Message.body`

##### **Arguments**:

+ `body`: unknown

###### Decorators

+ @body.setter

#### Function `Message.header`

##### **Arguments**:

+ `header`: unknown

###### Decorators

+ @header.setter

#### Function `Message.__init__`

##### **Arguments**:

+ `body`: dict

+ `header`: dict

#### Function `Message.__str__`

###### Declared returns: `str`

#### Function `Message.print_message`

 ``` 
 Method print message 
 ```

##### **Returns**:

```console

 None

```

#### Function `Message.update_body`

 ``` 
 Method add value to body
if a `key` exists, then the date_to_add will be added by this `key`
if the key doesn't exist then date_to_add must be a dictionary
and the current __body will be updated 
 ```

##### **Arguments**:

 + `date_to_add`: `Union[Dict,Any]` - empty description

 + `key`: `Optional[str]` - empty description

##### **Returns**:

```console

 None

```

#### Function `Message.update_header`

 ``` 
 Method add value to body
if a `key` exists, then the date_to_add will be added by this `key`
if the key doesn't exist then date_to_add must be a dictionary
and the current __header will be updated 
 ```

##### **Arguments**:

 + `date_to_add`: `Union[Dict,Any]` - empty description

 + `key`: `Optional[str]` - empty description

##### **Returns**:

```console

 None

```

#### Function `Message.get_body`

 ``` 
 The method returns the body of the message str or dict for future processing 
 ```

##### **Arguments**:

 + `returned_type_str`: `bool` -  type string may be needed if send to queue

##### **Returns**:

```console

 body in str or dict type

```

###### Declared returns: `Union[str,Dict]`

#### Function `Message.get_header`

 ``` 
 The method returns the header of the message str or dict for future processing 
 ```

##### **Arguments**:

 + `returned_type_str`: `bool` -  type string may be needed if send to rabbit queue

##### **Returns**:

```console

 header in str or dict type

```

###### Declared returns: `Union[str,Dict]`

#### Function `Message.get_source`

###### Declared returns: `str`

#### Function `Message.set_source`

##### **Arguments**:

 + `new_source`: `str` - empty description

## __init__.py

## __init__.py

### Importing

## exc.py

### Service exceptions

### Class  `ServiceException(Exception)`

`Class for Service exceptions`

### Class  `ServiceBlockException(BaseException)`

`Class for exceptions in ServiceBlock`

### Class  `ServiceBuilderException(BaseException)`

`Class for exceptions in BuilderService`

### Class  `NotUniqueCommandError(BaseException)`

`Class error if user add the same commands`

### Class  `UnknownCommandWarning(Warning)`

`Class Warning if handler got msg with incorrect command`

### Class  `DoublePostProcessFunctionDeclaredError(ServiceException)`

`Exception if many default postprocess handlers`

#### Function `DoublePostProcessFunctionDeclaredError.__init__`

### Class  `IncorrectDefaultCommand(ServiceException)`

`among the available commands, there is no default command`

#### Function `IncorrectDefaultCommand.__init__`

##### **Arguments**:

+ `command`: str

+ `list_command`: list

### Class  `EmptyCommandsException(ServiceException)`

`Empty list of commands for service operation`

#### Function `EmptyCommandsException.__init__`

### Class  `CommandHandlerNotFoundException(ServiceException)`

`if not exist handler and not exist default handler`

#### Function `CommandHandlerNotFoundException.__init__`

##### **Arguments**:

+ `command`: str

## service.py

### Module Service with help classes for build service

### Variable assignment

+ `default_logger` = logging.Logger(__name__): object

### Class  `ServiceBlock(object)`

`Class ServiceBlock for ServiceBuilder`

##### Class variables

+ `__process` = None: none

+ `__post_process` = None: none

#### Function `ServiceBlock.process`

 ``` 
 process instance CommandHandlerStrategy 
 ```

###### Decorators

+ @property

#### Function `ServiceBlock.post_process`

 ``` 
 post_process instance CommandHandlerPostStrategy 
 ```

###### Decorators

+ @property

#### Function `ServiceBlock.process`

 ``` 
 process setter 
 ```

##### **Arguments**:

 + `val`: `Union[type,CommandHandlerStrategy]` - empty description

###### Decorators

+ @process.setter

#### Function `ServiceBlock.post_process`

 ``` 
 post_process setter 
 ```

##### **Arguments**:

 + `val`: `Union[type,CommandHandlerPostStrategy]` - empty description

###### Decorators

+ @post_process.setter

#### Function `ServiceBlock.__init__`

 ``` 
 Init ServiceBlock 
 ```

##### **Arguments**:

 + `process`: `Union[type,CommandHandlerStrategy]` - empty description

 + `post_process`: `Union[type,CommandHandlerPostStrategy]` - empty description

### Class  `ServiceBuilder(object)`

`Class for build and aggregate handlers`

##### Class variables

+ `_default_post_process` = None: none

#### Function `ServiceBuilder._check_default_pp`

##### **Arguments**:

+ `default_post_process`: Union[type,CommandHandlerPostStrategy]

###### Decorators

+ @staticmethod

###### Declared returns: `Optional[CommandHandlerPostStrategy]`

#### Function `ServiceBuilder.__init__`

 ``` 
 Init ServiceBuilder 
 ```

#### Function `ServiceBuilder.build`

 ``` 
 Method build dict handler 
 ```

##### **Arguments**:

 + `log`: `logging.Logger` -  log application for set into services

 + `service_instance`: `Service` -  service object

##### **Returns**:

```console

 {'command':{'process': CommandHandlerStrategy,
'post_process': CommandHandlerPostStrategy}

```

###### Declared returns: `Dict[<_ast.Name object at 0x035F0230>:<_ast.Subscript object at 0x035F0250>:]`

### Class  `Service(object)`

`Class Service for handle msg-s from queue`

##### Class variables

+ `_command_field`: unknown = os.getenv('NameCommandInHandler','command'): object

+ `_default_command`: unknown = os.getenv('DefaultCommand','run'): object

+ `_dict_handlers` = dict(): object

+ `_is_run_default`: unknown = False: bool

+ `_service_commands`: unknown = None: none

+ `is_catch_exceptions`: unknown = False: bool

#### Function `Service.service_commands`

 ``` 
 Property _service_commands 
 ```

##### **Returns**:

```console

 ServiceBuilder

```

###### Decorators

+ @property

###### Declared returns: `Optional[ServiceBuilder]`

#### Function `Service.service_commands`

 ``` 
 setter ServiceBuilder 
 ```

##### **Arguments**:

 + `service_builder`: `ServiceBuilder` - empty description

##### **Returns**:

```console

 None

```

###### Decorators

+ @service_commands.setter

#### Function `Service.__init__`

 ``` 
 Init Service 
 ```

##### **Arguments**:

 + `service_builder`: `ServiceBuilder` -  instance builder with handlers command

 + `log`: `logging.Logger` -  logger

 + `is_run_default`: `bool` - empty description

 + `command_field`: `str` - empty description

 + `default_command`: `str` - empty description

 + `is_catch_exceptions`: `bool` - empty description

#### Function `Service._get_handlers`

##### **Arguments**:

+ `msg`: unknown

###### Declared returns: `Tuple[CommandHandlerStrategy,CommandHandlerPostStrategy]`

#### Function `Service.handle`

 ``` 
 Method handle msgs from queue for this service
if only one handler service run this handler
if don't found handler and exist default command 
 ```

##### **Arguments**:

 + `msg`: `Message` - empty description

###### Declared returns: `Optional[Message]`

#### Function `async` `Service.ahandle`

 ``` 
 async Method handle msgs from queue for this service
if only one handler service run this handler
if don't found handler and exist default command 
 ```

##### **Arguments**:

 + `msg`: `Message` - empty description

###### Declared returns: `Optional[Message]`

## to_extends.py

### Module with classes for inheritance.
And the implementation in these classes of the service logic.

### Class  `CommandHandler(ABC)`

`Class with method for all handlers`

##### Class variables

+ `_logger` = None: none

+ `_service_instance` = None: none

#### Function `CommandHandler.logger`

 ``` 
 get logger 
 ```

##### **Returns**:

```console

  logger or None

```

###### Decorators

+ @property

###### Declared returns: `Optional[logger]`

#### Function `CommandHandler.logger`

 ``` 
 method checks the set value 
 ```

##### **Arguments**:

 + `val`: `Any` -  value to set

###### Decorators

+ @logger.setter

#### Function `CommandHandler.set_logger`

 ``` 
 method set to service global logger if not inited 
 ```

##### **Arguments**:

 + `log`: `logging.Logger` -  service logger

##### **Returns**:

```console

 None

```

#### Function `CommandHandler.set_service_instance`

 ``` 
 Added a single scope for sharing data in the service 
 ```

##### **Arguments**:

 + `instance`: `Service` -  service object

#### Function `CommandHandler.set_to_swap_scope`

 ``` 
 Method adds a value to the global scope for access from all services 
 ```

##### **Arguments**:

 + `key`: `str` -  name key

 + `data`: `Any` -  data to add

##### **Returns**:

```console

 bool: is_added_value

```

###### Declared returns: `bool`

#### Function `CommandHandler.get_from_swap_scope`

 ``` 
 Method gets from the global scope a value available for all services 
 ```

##### **Arguments**:

 + `key`: `str` -  name key to get value

##### **Returns**:

```console

 data if exist or None

```

###### Declared returns: `Optional[Any]`

### Class  `CommandHandlerStrategy(CommandHandler,ABC)`

`handler class`

#### Function `CommandHandlerStrategy.target_command`

 ``` 
 this command will determine that the message should be processed by this particular service 
 ```

###### Decorators

+ @property

#### Function `CommandHandlerStrategy.process`

 ``` 
 the main method for executing the logic of this handler, must be overridden in the inheritor 
 ```

##### **Arguments**:

 + `msg`: `Message` -  msg from queue

##### **Returns**:

```console

 MessageQueue or None if return None post handler will not be called

```

###### Decorators

+ @abstractmethod

###### Declared returns: `Message`

#### Function `async` `CommandHandlerStrategy.aprocess`

 ``` 
 the main async method for executing the logic of this handler,
must be overridden in the inheritor 
 ```

##### **Arguments**:

 + `msg`: `Message` -  msg from queue

##### **Returns**:

```console

 MessageQueue or None if return None post handler will not be called

```

###### Decorators

+ @abstractmethod

###### Declared returns: `Message`

### Class  `CommandHandlerPostStrategy(CommandHandler,ABC)`

`Post Process Handler`

#### Function `CommandHandlerPostStrategy.post_process`

 ``` 
 method does post processing
e.g. sending to another queue
, must be overridden in the inheritor 
 ```

##### **Arguments**:

 + `msg`: `Message` - empty description

##### **Returns**:

```console

 None

```

###### Decorators

+ @abstractmethod

#### Function `async` `CommandHandlerPostStrategy.apost_process`

 ``` 
 method does post processing
e.g. sending to another queue
, must be overridden in the inheritor 
 ```

##### **Arguments**:

 + `msg`: `Message` - empty description

##### **Returns**:

```console

 None

```

###### Decorators

+ @abstractmethod