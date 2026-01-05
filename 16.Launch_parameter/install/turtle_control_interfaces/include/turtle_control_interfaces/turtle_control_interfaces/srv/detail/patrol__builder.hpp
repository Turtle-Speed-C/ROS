// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from turtle_control_interfaces:srv/Patrol.idl
// generated code does not contain a copyright notice

#ifndef TURTLE_CONTROL_INTERFACES__SRV__DETAIL__PATROL__BUILDER_HPP_
#define TURTLE_CONTROL_INTERFACES__SRV__DETAIL__PATROL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "turtle_control_interfaces/srv/detail/patrol__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace turtle_control_interfaces
{

namespace srv
{

namespace builder
{

class Init_Patrol_Request_target_y
{
public:
  explicit Init_Patrol_Request_target_y(::turtle_control_interfaces::srv::Patrol_Request & msg)
  : msg_(msg)
  {}
  ::turtle_control_interfaces::srv::Patrol_Request target_y(::turtle_control_interfaces::srv::Patrol_Request::_target_y_type arg)
  {
    msg_.target_y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::turtle_control_interfaces::srv::Patrol_Request msg_;
};

class Init_Patrol_Request_target_x
{
public:
  Init_Patrol_Request_target_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Patrol_Request_target_y target_x(::turtle_control_interfaces::srv::Patrol_Request::_target_x_type arg)
  {
    msg_.target_x = std::move(arg);
    return Init_Patrol_Request_target_y(msg_);
  }

private:
  ::turtle_control_interfaces::srv::Patrol_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::turtle_control_interfaces::srv::Patrol_Request>()
{
  return turtle_control_interfaces::srv::builder::Init_Patrol_Request_target_x();
}

}  // namespace turtle_control_interfaces


namespace turtle_control_interfaces
{

namespace srv
{

namespace builder
{

class Init_Patrol_Response_result
{
public:
  Init_Patrol_Response_result()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::turtle_control_interfaces::srv::Patrol_Response result(::turtle_control_interfaces::srv::Patrol_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::turtle_control_interfaces::srv::Patrol_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::turtle_control_interfaces::srv::Patrol_Response>()
{
  return turtle_control_interfaces::srv::builder::Init_Patrol_Response_result();
}

}  // namespace turtle_control_interfaces

#endif  // TURTLE_CONTROL_INTERFACES__SRV__DETAIL__PATROL__BUILDER_HPP_
