// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from turtle_control_interfaces:srv/Patrol.idl
// generated code does not contain a copyright notice

#ifndef TURTLE_CONTROL_INTERFACES__SRV__DETAIL__PATROL__STRUCT_H_
#define TURTLE_CONTROL_INTERFACES__SRV__DETAIL__PATROL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/Patrol in the package turtle_control_interfaces.
typedef struct turtle_control_interfaces__srv__Patrol_Request
{
  /// 目标x坐标
  float target_x;
  /// 目标y坐标
  float target_y;
} turtle_control_interfaces__srv__Patrol_Request;

// Struct for a sequence of turtle_control_interfaces__srv__Patrol_Request.
typedef struct turtle_control_interfaces__srv__Patrol_Request__Sequence
{
  turtle_control_interfaces__srv__Patrol_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} turtle_control_interfaces__srv__Patrol_Request__Sequence;


// Constants defined in the message

/// Constant 'SUCCESS'.
/**
  * 定义常量，表示成功
 */
enum
{
  turtle_control_interfaces__srv__Patrol_Response__SUCCESS = 1
};

/// Constant 'FAIL'.
/**
  * 定义常量，表示失败
 */
enum
{
  turtle_control_interfaces__srv__Patrol_Response__FAIL = 0
};

/// Struct defined in srv/Patrol in the package turtle_control_interfaces.
typedef struct turtle_control_interfaces__srv__Patrol_Response
{
  /// 处理结果
  int8_t result;
} turtle_control_interfaces__srv__Patrol_Response;

// Struct for a sequence of turtle_control_interfaces__srv__Patrol_Response.
typedef struct turtle_control_interfaces__srv__Patrol_Response__Sequence
{
  turtle_control_interfaces__srv__Patrol_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} turtle_control_interfaces__srv__Patrol_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TURTLE_CONTROL_INTERFACES__SRV__DETAIL__PATROL__STRUCT_H_
