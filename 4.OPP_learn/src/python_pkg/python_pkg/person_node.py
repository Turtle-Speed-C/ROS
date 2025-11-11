import rclpy
from rclpy.node import Node

class PersonNode(Node):
    def __init__(self, node_name:str, name:str, age:int) -> None:
        super().__init__(node_name)
        print('PersonNode 的 __init__方法被调用了')
        self.name=name
        self.age=age

    def eat(self, food_name:str):
        #print(f'my name is {self.name},今年{self.age}岁，我现在正在吃{food_name}')
        self.get_logger().info(f'my name is {self.name},今年{self.age}岁，我现在正在吃{food_name}')


def main():
    rclpy.init()
    node=PersonNode('person_node','lxf',24)
    node.eat('涮羊肉')
    rclpy.spin(node)
    rclpy.shutdown()