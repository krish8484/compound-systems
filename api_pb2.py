# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='api.proto',
  package='api',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\tapi.proto\x12\x03\x61pi\"&\n\x0bTaskRequest\x12\x17\n\x04task\x18\x01 \x01(\x0b\x32\t.api.Task\"+\n\x0cTaskResponse\x12\x1b\n\x06\x66uture\x18\x01 \x01(\x0b\x32\x0b.api.Future\"8\n\x14TaskCompletedRequest\x12\x0e\n\x06taskId\x18\x01 \x01(\t\x12\x10\n\x08workerId\x18\x02 \x01(\t\"4\n\x15TaskCompletedResponse\x12\x1b\n\x06status\x18\x01 \x01(\x0b\x32\x0b.api.Status\")\n\x15RegisterWorkerRequest\x12\x10\n\x08workerId\x18\x01 \x01(\t\"5\n\x16RegisterWorkerResponse\x12\x1b\n\x06status\x18\x01 \x01(\x0b\x32\x0b.api.Status\"/\n\x10GetResultRequest\x12\x1b\n\x06\x66uture\x18\x01 \x01(\x0b\x32\x0b.api.Future\"#\n\x11GetResultResponse\x12\x0e\n\x06result\x18\x01 \x01(\x0c\"@\n\x04Task\x12\x0e\n\x06taskId\x18\x01 \x01(\t\x12\x16\n\x0etaskDefinition\x18\x02 \x01(\t\x12\x10\n\x08taskData\x18\x03 \x01(\x0c\" \n\x06\x46uture\x12\x16\n\x0eresultLocation\x18\x01 \x01(\t\"\x19\n\x06Status\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xda\x01\n\x0cSchedulerApi\x12\x33\n\nSubmitTask\x12\x10.api.TaskRequest\x1a\x11.api.TaskResponse\"\x00\x12H\n\rTaskCompleted\x12\x19.api.TaskCompletedRequest\x1a\x1a.api.TaskCompletedResponse\"\x00\x12K\n\x0eRegisterWorker\x12\x1a.api.RegisterWorkerRequest\x1a\x1b.api.RegisterWorkerResponse\"\x00\x32\x7f\n\tWorkerApi\x12<\n\tGetResult\x12\x15.api.GetResultRequest\x1a\x16.api.GetResultResponse\"\x00\x12\x34\n\x0b\x45xecuteTask\x12\x10.api.TaskRequest\x1a\x11.api.TaskResponse\"\x00\x62\x06proto3'
)




_TASKREQUEST = _descriptor.Descriptor(
  name='TaskRequest',
  full_name='api.TaskRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task', full_name='api.TaskRequest.task', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=56,
)


_TASKRESPONSE = _descriptor.Descriptor(
  name='TaskResponse',
  full_name='api.TaskResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='future', full_name='api.TaskResponse.future', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=58,
  serialized_end=101,
)


_TASKCOMPLETEDREQUEST = _descriptor.Descriptor(
  name='TaskCompletedRequest',
  full_name='api.TaskCompletedRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='taskId', full_name='api.TaskCompletedRequest.taskId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='workerId', full_name='api.TaskCompletedRequest.workerId', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=103,
  serialized_end=159,
)


_TASKCOMPLETEDRESPONSE = _descriptor.Descriptor(
  name='TaskCompletedResponse',
  full_name='api.TaskCompletedResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='api.TaskCompletedResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=161,
  serialized_end=213,
)


_REGISTERWORKERREQUEST = _descriptor.Descriptor(
  name='RegisterWorkerRequest',
  full_name='api.RegisterWorkerRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='workerId', full_name='api.RegisterWorkerRequest.workerId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=215,
  serialized_end=256,
)


_REGISTERWORKERRESPONSE = _descriptor.Descriptor(
  name='RegisterWorkerResponse',
  full_name='api.RegisterWorkerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='api.RegisterWorkerResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=258,
  serialized_end=311,
)


_GETRESULTREQUEST = _descriptor.Descriptor(
  name='GetResultRequest',
  full_name='api.GetResultRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='future', full_name='api.GetResultRequest.future', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=313,
  serialized_end=360,
)


_GETRESULTRESPONSE = _descriptor.Descriptor(
  name='GetResultResponse',
  full_name='api.GetResultResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='api.GetResultResponse.result', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=362,
  serialized_end=397,
)


_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='api.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='taskId', full_name='api.Task.taskId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='taskDefinition', full_name='api.Task.taskDefinition', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='taskData', full_name='api.Task.taskData', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=399,
  serialized_end=463,
)


_FUTURE = _descriptor.Descriptor(
  name='Future',
  full_name='api.Future',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resultLocation', full_name='api.Future.resultLocation', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=465,
  serialized_end=497,
)


_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='api.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='api.Status.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=499,
  serialized_end=524,
)

_TASKREQUEST.fields_by_name['task'].message_type = _TASK
_TASKRESPONSE.fields_by_name['future'].message_type = _FUTURE
_TASKCOMPLETEDRESPONSE.fields_by_name['status'].message_type = _STATUS
_REGISTERWORKERRESPONSE.fields_by_name['status'].message_type = _STATUS
_GETRESULTREQUEST.fields_by_name['future'].message_type = _FUTURE
DESCRIPTOR.message_types_by_name['TaskRequest'] = _TASKREQUEST
DESCRIPTOR.message_types_by_name['TaskResponse'] = _TASKRESPONSE
DESCRIPTOR.message_types_by_name['TaskCompletedRequest'] = _TASKCOMPLETEDREQUEST
DESCRIPTOR.message_types_by_name['TaskCompletedResponse'] = _TASKCOMPLETEDRESPONSE
DESCRIPTOR.message_types_by_name['RegisterWorkerRequest'] = _REGISTERWORKERREQUEST
DESCRIPTOR.message_types_by_name['RegisterWorkerResponse'] = _REGISTERWORKERRESPONSE
DESCRIPTOR.message_types_by_name['GetResultRequest'] = _GETRESULTREQUEST
DESCRIPTOR.message_types_by_name['GetResultResponse'] = _GETRESULTRESPONSE
DESCRIPTOR.message_types_by_name['Task'] = _TASK
DESCRIPTOR.message_types_by_name['Future'] = _FUTURE
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TaskRequest = _reflection.GeneratedProtocolMessageType('TaskRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKREQUEST,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.TaskRequest)
  })
_sym_db.RegisterMessage(TaskRequest)

TaskResponse = _reflection.GeneratedProtocolMessageType('TaskResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKRESPONSE,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.TaskResponse)
  })
_sym_db.RegisterMessage(TaskResponse)

TaskCompletedRequest = _reflection.GeneratedProtocolMessageType('TaskCompletedRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKCOMPLETEDREQUEST,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.TaskCompletedRequest)
  })
_sym_db.RegisterMessage(TaskCompletedRequest)

TaskCompletedResponse = _reflection.GeneratedProtocolMessageType('TaskCompletedResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKCOMPLETEDRESPONSE,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.TaskCompletedResponse)
  })
_sym_db.RegisterMessage(TaskCompletedResponse)

RegisterWorkerRequest = _reflection.GeneratedProtocolMessageType('RegisterWorkerRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERWORKERREQUEST,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.RegisterWorkerRequest)
  })
_sym_db.RegisterMessage(RegisterWorkerRequest)

RegisterWorkerResponse = _reflection.GeneratedProtocolMessageType('RegisterWorkerResponse', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERWORKERRESPONSE,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.RegisterWorkerResponse)
  })
_sym_db.RegisterMessage(RegisterWorkerResponse)

GetResultRequest = _reflection.GeneratedProtocolMessageType('GetResultRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETRESULTREQUEST,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.GetResultRequest)
  })
_sym_db.RegisterMessage(GetResultRequest)

GetResultResponse = _reflection.GeneratedProtocolMessageType('GetResultResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETRESULTRESPONSE,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.GetResultResponse)
  })
_sym_db.RegisterMessage(GetResultResponse)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.Task)
  })
_sym_db.RegisterMessage(Task)

Future = _reflection.GeneratedProtocolMessageType('Future', (_message.Message,), {
  'DESCRIPTOR' : _FUTURE,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.Future)
  })
_sym_db.RegisterMessage(Future)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.Status)
  })
_sym_db.RegisterMessage(Status)



_SCHEDULERAPI = _descriptor.ServiceDescriptor(
  name='SchedulerApi',
  full_name='api.SchedulerApi',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=527,
  serialized_end=745,
  methods=[
  _descriptor.MethodDescriptor(
    name='SubmitTask',
    full_name='api.SchedulerApi.SubmitTask',
    index=0,
    containing_service=None,
    input_type=_TASKREQUEST,
    output_type=_TASKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='TaskCompleted',
    full_name='api.SchedulerApi.TaskCompleted',
    index=1,
    containing_service=None,
    input_type=_TASKCOMPLETEDREQUEST,
    output_type=_TASKCOMPLETEDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RegisterWorker',
    full_name='api.SchedulerApi.RegisterWorker',
    index=2,
    containing_service=None,
    input_type=_REGISTERWORKERREQUEST,
    output_type=_REGISTERWORKERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SCHEDULERAPI)

DESCRIPTOR.services_by_name['SchedulerApi'] = _SCHEDULERAPI


_WORKERAPI = _descriptor.ServiceDescriptor(
  name='WorkerApi',
  full_name='api.WorkerApi',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=747,
  serialized_end=874,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetResult',
    full_name='api.WorkerApi.GetResult',
    index=0,
    containing_service=None,
    input_type=_GETRESULTREQUEST,
    output_type=_GETRESULTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ExecuteTask',
    full_name='api.WorkerApi.ExecuteTask',
    index=1,
    containing_service=None,
    input_type=_TASKREQUEST,
    output_type=_TASKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_WORKERAPI)

DESCRIPTOR.services_by_name['WorkerApi'] = _WORKERAPI

# @@protoc_insertion_point(module_scope)
